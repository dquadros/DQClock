'''
Control the RGB LED Ring
'''
from machine import Pin
from neopixel import NeoPixel
import uasyncio

RING_PIN = 13
NLEDS = 12
LED_ORDER = (6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5)

class LED_RING:
    
    OFF = const(0)
    ON = const(1)
    FADE = const(2)
    BOUNCE = const(3)
    
    def clear(self):
        self._ring.fill((0,0,0))
        self._ring.write()

    def __init__(self):
        self._ring = NeoPixel(Pin(RING_PIN),NLEDS)
        self.clear()
        self._animate = uasyncio.Event()
        self._finished = uasyncio.Event()
        self._finished.set()
        self._mode = LED_RING.OFF
        self._color = (0,0,0)
        self._count = 1
    
    def start(self, mode, color=(0,0,0), count=1):
        self._mode = mode
        self._color = list(color)
        self._count = count
        self._finished.clear()
        self._animate.set()
        
    def isIdle(self):
        return self._finished.is_set()
    
    async def waitIdle(self):
        await self._finished.wait()
    
    async def update(self):
        while True:
            await self._animate.wait()
            self._animate.clear()
            if self._mode == LED_RING.OFF:
                self.clear()
            elif self._mode == LED_RING.ON:
                self._ring.fill(self._color)
                self._ring.write()
            elif self._mode == LED_RING.FADE:
                while True:
                    print(self._color)
                    self._ring.fill(self._color)
                    self._ring.write()
                    if sum(self._color) == 0:
                        break
                    await uasyncio.sleep_ms(150)
                    for i in range(3):
                        if self._color[i] > 7:
                            self._color[i] -= 7
                        else:
                            self._color[i] = 0
            elif self._mode == LED_RING.BOUNCE:
                self.clear()
                for _ in range(self._count):
                    for i in range(NLEDS):
                        self._ring[LED_ORDER[i]] = self._color
                        self._ring.write()
                        await uasyncio.sleep_ms(100)
                        self._ring[LED_ORDER[i]] = (0, 0, 0)
                    for i in range(NLEDS-2, 0, -1):
                        self._ring[LED_ORDER[i]] = self._color
                        self._ring.write()
                        await uasyncio.sleep_ms(100)
                        self._ring[LED_ORDER[i]] = (0, 0, 0)
                self.clear()
            self._finished.set()
        
if __name__ == "__main__":

    ring = LED_RING()
    
    async def test():
        while (True):
            await uasyncio.sleep(2)
            ring.start(LED_RING.ON, (127, 0, 0))
            await uasyncio.sleep(2)
            ring.start(LED_RING.FADE, (127, 63, 63))
            await ring.waitIdle()
            await uasyncio.sleep(1)
            ring.start(LED_RING.BOUNCE, (127, 0, 0), 3)
            await ring.waitIdle()
            await uasyncio.sleep(1)
            ring.start(LED_RING.OFF)
        
    loop = uasyncio.get_event_loop()
    loop.create_task(ring.update())
    loop.create_task(test())
    loop.run_forever()
    