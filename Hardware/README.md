# Alarm Clock Hardware

## Components

* ESP32-S3 supermini board: this can probably be replaced by any other microcontroller board with the required I/O and WiFi capability (some software changes may be needed).
* Round color LCD Display (with GC9A01 controller): may be an overkill for this project but looks really nice. You could use a simpler monochrome OLED display by replacing the display code and switching from SPI to I2C.
* RGB LED (WS2812B) ring (with 12 LEDs): I selected a model that fits outside the display; you could use a discrete RGB LED.
* Touch sensor: a button could be used instead.
* DFRobot DFPlayer Mini: a small MP3 player module. You could make simpler sounds with a buzzer, but the ability to play complex sounds and songs makes the clock more playful. The sounds and songs are stored on a microSD card; see the software documentation for the file names.
* Small speaker: connect directly to the MP3 module

## Connections

The picture below shows how the components are interconnected. I use a mix of pin connectors and solder; use whatever technique you prefer.

![DQClock Circuit](/circuit.png)


