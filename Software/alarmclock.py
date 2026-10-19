'''
DQClock - Alarm Clock and Sleep Trainer
Daniel Quadros - Oct/26
'''

from machine import Pin, SPI
import gc9a01py as gc9a01
from mp3 import MP3
from clock import CLOCK
from LedRing import LED_RING
from CfgClock import cfg_clock

from fonts import vga1_16x32 as font

from WiFiMgr import wifi_start
from phew import server

import ntptime
import time
import uasyncio
import utime

VERSION = "0.2"

COLORS = [ (1,0,0), (0,1,0), (1,1,0) ]

ip_address = ''

def init():
    '''Hardware initialization'''
    global ring, mp3,tft,button
    button = Pin(12, Pin.IN)
    ring = LED_RING()
    mp3 = MP3(8, 9)
    spi = SPI(2, baudrate=60000000, sck=Pin(7), mosi=Pin(6))
    tft = gc9a01.GC9A01(
        spi,
        dc=Pin(5, Pin.OUT),
        cs=Pin(5, Pin.OUT),
        reset=Pin(2, Pin.OUT),
        rotation=0)
    tft.fill(gc9a01.BLACK)
    
def about():
    tft.fill(gc9a01.BLACK)
    tft.text(font, f"DQClock v{VERSION}",
                 15, 70, gc9a01.RED, gc9a01.BLACK)
    parts = ip_address.split('.')
    tft.text(font, "IP:", 30, 120, gc9a01.RED, gc9a01.BLACK)
    tft.text(font, f"{parts[0]}.{parts[1]}", 80, 120, gc9a01.RED, gc9a01.BLACK)
    tft.text(font, f"{parts[2]}.{parts[3]}", 80, 160, gc9a01.RED, gc9a01.BLACK)
 
def infoConfig():
    tft.fill(gc9a01.BLACK)
    tft.text(font, f"DQClock v{VERSION}",
                 15, 70, gc9a01.RED, gc9a01.BLACK)
    tft.text(font, "Connect to", 30, 120, gc9a01.RED, gc9a01.BLACK)
    tft.text(font, "WiFi dqclock", 30, 150, gc9a01.RED, gc9a01.BLACK)
 
EYE_COLOR = gc9a01.color565(250,255,173)

def round_eyes(): 
    tft.fill_rect(54, 60, 52, 42, gc9a01.BLACK)
    tft.fill_rect(132, 60, 52, 42, gc9a01.BLACK)
    tft.fill_ellipse(80, 80, 26, 20, EYE_COLOR)
    tft.fill_ellipse(82, 80, 8, 8, gc9a01.BLACK)
    tft.fill_ellipse(158, 80, 26, 20, EYE_COLOR)
    tft.fill_ellipse(156, 80, 8, 8, gc9a01.BLACK)

def closed_eyes():
    tft.fill_rect(54, 60, 52, 42, gc9a01.BLACK)
    tft.fill_rect(132, 60, 52, 42, gc9a01.BLACK)
    tft.fill_rect(55, 79, 52, 3, EYE_COLOR)
    tft.fill_rect(132, 79, 52, 3, EYE_COLOR)

def alert_eyes():
    tft.fill_rect(54, 60, 52, 42, gc9a01.BLACK)
    tft.fill_rect(132, 60, 52, 42, gc9a01.BLACK)
    tft.fill_ellipse(80, 80, 26, 20, gc9a01.RED)
    tft.fill_ellipse(80, 82, 10, 10, gc9a01.BLACK)
    tft.fill_ellipse(158, 80, 26, 20, gc9a01.RED)
    tft.fill_ellipse(158, 82, 10, 10, gc9a01.BLACK)
    tft.fill_rect(54, 60, 52, 10, gc9a01.BLACK)
    tft.fill_rect(132, 60, 52, 10, gc9a01.BLACK)

def initTime():
    '''Get current time from the internet'''
    try:
        ntptime.settime()
    except:
        pass

def get_local_time(utc_offset_hours=-3):
    offset_seconds = utc_offset_hours * 3600
    local_timestamp = time.time() + offset_seconds
    return time.localtime(local_timestamp)

async def alarm_clock():
    # button initialization
    button_pressed = False
    when_pressed = -1
    button_press = 0
    
    # alarm initialization
    initTime()
    now = get_local_time()
    clock = CLOCK(cfg_clock, now)
    prev_hour = now[3]
    
    # led ring initialization
    leds = 'OFF'
    bright = int(cfg_clock['night_bright']) << 3
    night_color = tuple(x*bright for x in COLORS[int(cfg_clock['night_color'])])
    
    # main clock loop
    while True:
        # synchronize clock every hour
        now = get_local_time()
        if now[3] != prev_hour:
            initTime()
            prev_hour = now[3]

        # check alarm
        op, sound = clock.checkAlarm(now)
        if op =='stop':
            mp3.stop()
        elif op == 'play':
            mp3.play(sound)

        # update LED RING / eyes
        if clock.isAlarmOn():
            if leds != 'flashing':
                leds = 'flashing'
                alert_eyes()
            if ring.isIdle():
                ring.start(LED_RING.BOUNCE, (127,0,0))
        else:
            new_leds = 'night' if (now[3] < 6) or (now[3] > 19) else 'day'
            if new_leds != leds:
                leds = new_leds
                ring.start(LED_RING.ON, night_color if leds == 'night' else (0,127,127))
                if leds == 'night':
                    closed_eyes()
                else:
                    round_eyes()

        # update button status
        if button_pressed:
            if button.value() == 0:
                button_pressed = False
                time_pressed = time.time() - when_pressed
                button_press = 2 if time_pressed > 7 else 1
        elif button.value() == 1:
            button_pressed = True
            when_pressed = time.time()

        # process button press
        if button_press:
            if button_press == 1:
                # short press
                if clock.isAlarmOn():
                    mp3.stop()
                    clock.endAlarm(now)
            else:
                # long press
                if clock.isAlarmOn():
                    mp3.stop()
                    clock.endAlarm(now)
                    clock.snooze(now)
                else:
                    about();
                    await uasyncio.sleep_ms(3000)
                    tft.fill(gc9a01.BLACK)
                    leds = ""
            button_press = 0
        
        # Update hour on screen
        tft.text(font, f"{now[3]:02d}:{now[4]:02d}:{now[5]:02d}",
                 60, 170, gc9a01.BLUE, gc9a01.BLACK)
        
        # Wait half a second
        await uasyncio.sleep_ms(500)

# Main program
init()
print(cfg_clock)
wifi_ok, ip_address = wifi_start()
if wifi_ok:
    about()
    time.sleep(3)
    tft.fill(gc9a01.BLACK)
    print("Activating clock")
    loop = uasyncio.get_event_loop()
    loop.create_task(ring.update())
    loop.create_task(alarm_clock())
else:
    infoConfig()
    
# Start the web server...
print("Starting web server...")
try:
    server.run()
finally:
    print("Server stopped")
