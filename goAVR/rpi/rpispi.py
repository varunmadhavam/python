import spidev
import RPi.GPIO as GPIO
from time import sleep

class rpispi:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.reset=2    
        GPIO.setup(self.reset,GPIO.OUT)
        self.spi=spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz = 6000000
            
    def toggle_reset(self):
        GPIO.output(self.reset,GPIO.HIGH)
        sleep(.02)
        GPIO.output(self.reset,GPIO.LOW)

    def unhold_reset(self):
        GPIO.output(self.reset,GPIO.HIGH)
    
    def hold_reset(self):
        GPIO.output(self.reset,GPIO.LOW)
    
    def spi_transfer(self,fourbytes):
        return self.spi.xfer(fourbytes)