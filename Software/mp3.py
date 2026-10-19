'''
Simple class to drive MP3 module
Uses only two pins for communication
- TX    UART output in microcontroller, input in MP3 module
- BUSY  busy signal from MP2 module (through resistive divider)
'''

from machine import Pin
from machine import UART
from time import sleep, ticks_ms


class MP3:
    
    def send_cmd(self, cmd, param):
        ''' Send a command to MP3 module '''
        pkt = bytearray(10)
        pkt[0] = 0x7E  # Packet start
        pkt[1] = 0xFF  # Protocol version
        pkt[2] = 6     # Packet length
        pkt[3] = cmd
        pkt[4] = 0
        pkt[5] = param >> 8
        pkt[6] = param & 0xFF
        chk = 0
        for i in range(6):
            chk += pkt[i+1]
        chk = (-chk) & 0xFFFF
        pkt[7] = (chk >> 8) & 0xFF
        pkt[8] = chk & 0xFF
        pkt[9] = 0xEF  # Packet end
        self.uart.write(pkt)

    def __init__(self,pinTx,pinBusy):
        ''' Initialization '''
        self.uart = UART(1, baudrate=9600, tx=pinTx)
        self.busy = Pin(pinBusy, Pin.IN)
        self.send_cmd(0x07, 1)  # pop equalization
        sleep(0.2)
        self.send_cmd(0x06, 25)	# volume
        sleep(0.2)

    def isPlaying(self):
        return self.busy.value() == 0

    def play(self, fileno):
        '''
        Start playing a file
        fileno selects file (1 to 9999)
        Files must be in /mp3 directory in the SD
          and named 0001.mp3 to 9999.mp3
        '''
        timeout = ticks_ms()+2000
        while self.isPlaying() and (ticks_ms() < timeout):
            sleep(0.01) # wait for end of previous sound
        self.send_cmd(0x12, fileno)
        timeout = ticks_ms()+2000
        while not self.isPlaying() and (ticks_ms() < timeout):
            sleep(0.01) # wait for sound to start
        
    def stop(self):
        '''
        Stop playing
        '''
        if self.isPlaying():
            self.send_cmd(0x16, 0)
            timeout = ticks_ms()+2000
            while self.isPlaying() and (ticks_ms() < timeout):
                sleep(0.01) # wait for sound to stop


if __name__ == "__main__":
    mp3 = MP3(8, 9)
    mp3.play(3)
    print('start')
    while mp3.isPlaying():
        sleep(0.01)
    print('end')

    