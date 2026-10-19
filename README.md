# Alarm Clock / Despertador

This project is an alarm clock/sleep trainer inspired by the MELLA product from littlehippo.

It uses some playful features to help young children create healthy sleep habits.

## Operation

The current time is fetched from the Internet, so a WiFi connection is needed.

The first time it is turned on, it creates a WiFi network. Connecting a browser to this network will bring up a page where you can select and configure your network.

Connecting a browser to the clock after setting up the WiFi will bring up a configuration page where you can:

* select if the alarms will sound on weekends
* select the wake and bed times
* select the alarm sound
* select the snooze time
* select the sound to play when it is bedtime
* select the color and intensity of the LEDs during nighttime

A touch sensor is used to:

* Start the snooze time: long touch (more than 5 seconds) when the alarm is playing
* Stop the alarm: short touch (less than 5 seconds) when the alarm is playing
* Show the about screen: long touch (more than 5 seconds) when the alarm is not playing

A simple manual is available at the *Manual* directory.

## Hardware

The hardware is built around the Supermini ESP32-S3 board. The display is a round color LCD Display. A LED Ring and a MP3 player module are used for color and sounds.

See the *Hardware* directory for more details.

## Software

The software was developed in MicroPython.

See the *Software* directory for more details.

## Case

The case was designed with OpenSCAD and 3D printed.

See the *Case* directory for more details.

