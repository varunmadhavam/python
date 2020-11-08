import sys
import spidev
import RPi.GPIO as GPIO
from time import sleep

def enterprogramming(reset,spi):
    GPIO.output(reset,GPIO.HIGH)
    sleep(1/1000) #must be given positive pulse of at least two CPU clock cycles duration after SCK has been set to “0”. 1ms is order of magnitudes more than what is required at 16Mhz.
    GPIO.output(reset,GPIO.LOW)
    sleep(20/1000) #after pulling Reset low, wait at least 20ms before issuing the first command
    x=spi.xfer([0xAC,0x53,0x00,0x00])
    print(hex(x[0])," ",hex(x[1])," ",hex(x[2])," ",hex(x[3]))

def pulsereset(reset):
    GPIO.output(reset,GPIO.HIGH)
    sleep(1/1000)
    GPIO.output(reset,GPIO.LOW)

def chipid(spi):
    x=spi.xfer([0x30,0x00,0x00,0x00])
    print(hex(x[0])," ",hex(x[1])," ",hex(x[2])," ",hex(x[3]))
    x=spi.xfer([0x30,0x00,0x01,0x00])
    print(hex(x[0])," ",hex(x[1])," ",hex(x[2])," ",hex(x[3]))
    x=spi.xfer([0x30,0x00,0x02,0x00])
    print(hex(x[0])," ",hex(x[1])," ",hex(x[2])," ",hex(x[3]))

def chiperase(spi):
    twd_erase=9 #wait after chip erase in ms
    x=spi.xfer([0xAC,0x80,0x00,0x00])
    print(hex(x[0])," ",hex(x[1])," ",hex(x[2])," ",hex(x[3]))
    sleep(twd_erase/1000) #wait after chip erase.

def readhex(filename):
    hexstring=""
    with open(filename) as f:
        for line in f:
            if line[7:9] == "01": #end of file marker.
                break
            else:
                hexstring+=line[9:len(line)-3] #else append the data to the data string.
    return bytearray.fromhex(hexstring) #convert the hextring to a byte array and return.

def loadhex(program,spi):
    pagesize_flash=64 #flash page size of the chip in words
    twd_flash=4.5 #wait after write flash page in ms
    i=0 #track pages within the flash
    j=0 #track words within the flash page buffer
    k=0 #track the binary to be programmed
    spi.xfer([0x4D,0x00,0x00,0x00]) #load the extended address byte with 0 as we have only 256 pages.
    while k <= (len(program)-2):
        spi.xfer([0x40,0x00,j,program[k]]) #write the lowbyte of the jth word in ith page
        spi.xfer([0x48,0x00,j,program[k+1]]) #write the highbyte of the jth word in the ith page
        k=k+2 #+2 as we are handling 2 bytes every iteration since each word is 2 bytes.
        j=j+1
        if((k%(pagesize_flash*2))==0): # if true we have filled the page buffer. We can load it to page i.
            spi.xfer([0x4c,i>>8,i,0x00]) #load the current page buffer to page i.
            sleep(twd_flash/1000)
            j=0 #make the pointer to the flash page buffer to point to the start again.
            i=i+pagesize_flash #incremnet the fla
    if j > 0:
        spi.xfer([0x4c,i>>8,i,0x00])
        sleep(twd_flash/1000)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
reset=2; #GPIO pin to control the reset pin of the device.
GPIO.setup(reset,GPIO.OUT)
GPIO.output(reset,GPIO.LOW)
spi=spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=2000000 #The minimum low and high periods for the Serial Clock (SCK) input are defined as follows
                         #Low:  2 CPU clock cycles for fck < 12MHz, 3 CPU clock cycles for fck >= 12MHz
                         #High: 2 CPU clock cycles for fck < 12MHz, 3 CPU clock cycles for fck >= 12MHz
                         # We are running at 16MHZ, so 3 clock high and 3 clock low means f/6 = 12/6 = 2Mhz 

enterprogramming(reset,spi) #put the chip in programming mode.
chipid(spi) #prints the chip identification signatures.
chiperase(spi) #erase chip is madatory before flash upload.
pulsereset(reset) #pulse the reset pin to leave chip erase cycle.
enterprogramming(reset,spi) #enter programming mode again
loadhex(readhex(sys.argv[1]),spi) #load the binary to the device.

GPIO.output(reset,GPIO.HIGH) #Set the reset pin high to enable the device.
