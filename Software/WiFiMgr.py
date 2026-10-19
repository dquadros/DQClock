'''
WiFi Manager

Takes care of WiFi Configuration and Connection
'''

from phew import reset_wlan, access_point, connect_to_wifi, is_connected_to_wifi, dns, server
from phew.template import render_template
from CfgClock import cfg_clock
import network
import json
import machine
import os
import utime
import _thread
import sys

AP_NAME = "dqclock"
AP_DOMAIN = "dqclock.net"
AP_TEMPLATE_PATH = "ap_templates"
APP_TEMPLATE_PATH = "app_templates"

WIFI_FILE = "wifi.json"
WIFI_MAX_ATTEMPTS = 3



def reduce_log():
    # Try to reduce logging to save memory (if supported)
    try:
        import phew.logging
        if hasattr(phew.logging, 'LOG_WARN'):
            phew.logging.LOG_LEVEL = phew.logging.LOG_WARN
        elif hasattr(phew.logging, 'WARN'):
            phew.logging.LOG_LEVEL = phew.logging.WARN
    except:
        pass  # If logging config fails, continue anyway

def machine_reset():
    utime.sleep(1)
    print("Resetting...")
    machine.reset()

def wifi_setup_mode():
    print("Entering WiFi setup mode...")

    def ap_index(request):
        if request.headers.get("host").lower() != AP_DOMAIN.lower():
            return render_template(
                f"{AP_TEMPLATE_PATH}/redirect.html", domain=AP_DOMAIN.lower()
            )

        return render_template(f"{AP_TEMPLATE_PATH}/index.html")

    def ap_configure(request):
        print("Saving wifi credentials...")

        with open(WIFI_FILE, "w") as f:
            json.dump(request.form, f)
            f.close()

        # Schedule reboot to attempt connection with new credentials
        _thread.start_new_thread(machine_reset, ())
        return render_template(
            f"{AP_TEMPLATE_PATH}/configured.html", ssid=request.form["ssid"]
        )

    def ap_catch_all(request):
        if request.headers.get("host") != AP_DOMAIN:
            return render_template(
                f"{AP_TEMPLATE_PATH}/redirect.html", domain=AP_DOMAIN
            )

        return "Not found.", 404

    server.add_route("/", handler=ap_index, methods=["GET"])
    server.add_route("/configure", handler=ap_configure, methods=["POST"])
    server.set_callback(ap_catch_all)

    ap = access_point(AP_NAME)
    ip = ap.ifconfig()[0]
    dns.run_catchall(ip)

def set_hostname():
    hostname_set = False
    try:
        network.hostname("dqclock")
        hostname_set = True
        print(f"Hostname set to {network.hostname()}")
    except Exception as e:
        print(f"ERROR: Hostname setup error: {e}")
    
    if not hostname_set:
        print("WARNING: No hostname configured - use IP address directly")

def application_mode():
    print("Entering application mode.")
    
    # Get current IP address with retry logic
    wlan = network.WLAN(network.STA_IF)
    ip_address = None
    for attempt in range(3):
        try:
            ip_address = wlan.ifconfig()[0]
            if ip_address and ip_address != '0.0.0.0':
                break
        except Exception as e:
            print(f"Network interface error (attempt {attempt+1}): {e}")
            if attempt < 2:
                import utime
                utime.sleep(2)  # Wait before retry
    
    if not ip_address or ip_address == '0.0.0.0':
        print("ERROR: Could not get valid IP address - network may be unstable")
        ip_address = "unknown"
    
    # Print connection information
    print("\n" + "=" * 50)
    print("DQCLOCK WEB INTERFACE READY")
    print("=" * 50)
    if ip_address != "unknown":
        print(f"Primary: http://dqclock.local")
        print(f"Backup:  http://{ip_address}")
        try:
            ssid = wlan.config('ssid')
            print(f"Network: {ssid}")
        except:
            print("Network: Connected (SSID unavailable)")
        print("\nAccess Methods:")
        print("1. http://dqclock.local")
        print(f"2. http://{ip_address} (direct IP)")
    else:
        print("WARNING: Network interface unstable")
        print("May need device restart")
    print("=" * 50)
    print("Web interface starting...")
    print("=" * 50 + "\n")
    
    def app_index(request):
        try:
            print(f"DEBUG: Serving index page from {APP_TEMPLATE_PATH}/index.html")
            return render_template(f"{APP_TEMPLATE_PATH}/index.html",
                    weekend="checked" if cfg_clock["weekend"] else "",
                    wake_time=cfg_clock["wake_time"], wake_sound=cfg_clock["wake_sound"],
                    sleep_time=cfg_clock["sleep_time"], sleep_sound=cfg_clock["sleep_sound"],
                    night_color=cfg_clock["night_color"], night_bright=cfg_clock["night_bright"],
                    snooze=cfg_clock["snooze"])
        except Exception as e:
            print(f"ERROR: Failed to render index template: {e}")
            return f"Template error: {e}"

    def app_configure(request):
        print("Saving configuration...")
        cfg_clock['weekend'] = request.form.get('weekend','off').lower() == 'on'
        cfg_clock['wake_time'] = request.form['wake_time']
        cfg_clock['wake_sound'] = request.form['wake_sound']
        cfg_clock['sleep_time'] = request.form['sleep_time']
        cfg_clock['sleep_sound'] = request.form['sleep_sound']
        cfg_clock['snooze'] = request.form['snooze']
        cfg_clock['night_color'] = request.form['night_color']
        cfg_clock['night_bright'] = request.form['night_bright']
        cfg_clock.save()

        # Schedule reboot to use new configuration
        _thread.start_new_thread(machine_reset, ())
        
        return render_template(
            f"{APP_TEMPLATE_PATH}/configured.html"
        )

    def app_catch_all(request):
        # For any unmatched route, serve the main page (DNS catchall behavior)
        try:
            print(f"DEBUG: Catch-all serving index for: {request.path}")
            return render_template(f"{APP_TEMPLATE_PATH}/index.html")
        except Exception as e:
            print(f"ERROR: Catch-all template error: {e}")
            return f"Catch-all template error: {e}"

    server.add_route("/", handler=app_index, methods=["GET"])
    server.add_route("/configure", handler=app_configure, methods=["POST"])
    server.set_callback(app_catch_all)
    
    print("Application mode routes configured")


def wifi_start():
    reduce_log()
    reset_wlan()
    try:
        os.stat(WIFI_FILE)

        # File was found, attempt to connect to wifi...
        with open(WIFI_FILE) as f:
            wifi_current_attempt = 1
            wifi_credentials = json.load(f)

            set_hostname()
            
            while wifi_current_attempt < WIFI_MAX_ATTEMPTS:
                print(f"WiFi connection attempt {wifi_current_attempt}/{WIFI_MAX_ATTEMPTS}")
                ip_address = connect_to_wifi(
                    wifi_credentials["ssid"], wifi_credentials["password"]
                )

                if is_connected_to_wifi():
                    print(f"Connected to wifi, IP address {ip_address}")
                    utime.sleep(3)
                    break
                else:
                    wifi_current_attempt += 1
                    if wifi_current_attempt < WIFI_MAX_ATTEMPTS:
                        utime.sleep(5)

            if is_connected_to_wifi():
                print("Starting application mode...")
                application_mode()
                return True, ip_address
            else:
                # Bad configuration, delete the credentials file, reboot
                # into setup mode to get new credentials from the user.
                print("Bad wifi connection!")
                print(wifi_credentials)
                os.remove(WIFI_FILE)
                machine_reset()

    except Exception as e:
        # Either no wifi configuration file found, or something went wrong,
        # so go into setup mode.
        print(e)
        wifi_setup_mode()
        return False, ''
