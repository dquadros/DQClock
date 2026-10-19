# DQClock Software

The Software was developed using MicroPython and relays on two modules:

* PHEW (Python HTTP Endpoint Wrangler) comes from the Twirly project by veebch (https://github.com/veebch/twirly). I made a few changes, most related to the differences between ESP32 and Pico W networking.
* GC9A01py (the display drivers) was written by Russ Hughes (https://github.com/russhughes/gc9a01py). I added a crude ellipse drawing method.

My code is organized in a few modules:

* alarmclock.py is the main program and should be stored in the Supermini as main.py
* CfgClock.py deals with the clock configuration data
* clock.py has the alarm clock logic
* LedRing.py contols the LED ring (using the builtin NeoPixel module)
* mp3.py has the code to play sounds stored in the SD card in the mp3 module
* WiFiManager.py Takes care of WiFi Configuration and Connection

The sounds on the SD card were found in the Internet, I am not putting them in this repository due to copyright concerns. The files should be named 0001 to 008 and stores in a mp3 directory in the SD:

0001 beep
0002 rooster
0003 alarm sound
0004 not used for now
0005 lullaby
0006 gameover
0007 not used for now
0008 sweetdreams

