from hex import hex
from libserial.dataqueue import dataqueue
from libserial.serialdatahandler import goavrserial
from fsm import fsm
from arduino.arduinoavr import arduinoavr
from rpi.rpiavr import rpiavr
import threading
from time import sleep
import sys

if  len (sys.argv) != 3 :
    print("Not all parameters passed in command line")
    sys.exit (1)

hexdata = hex("/home/varun/coding/c/avr/blinky8/bin/blinky8.hex")
#hexdata = hex("/home/varun/coding/c/avr/goAvrC/bin/goAvrC.hex")

if sys.argv[1] == "arduino":
    serialdataqueue = dataqueue(50)
    stopping = threading.Event()
    goavrserial.getserialportlist()
    serialadapter = goavrserial('/dev/ttyUSB0',9600,serialdataqueue,stopping)
    chip=arduinoavr(0,0,32,0,8192,0,0,20,0,10,serialadapter,serialdataqueue,hexdata)
    mode=fsm(0,chip)
    serialadapter.run()
    sleep(4)
    mode.run()
    sleep(2)
    stopping.set()

elif sys.argv[1] == "rpi":
    chip=rpiavr(0,0,32,0,8192,0,0,20,0,10,hexdata)
    mode=fsm(2,chip)
    mode.run()

else:
    print("Unsupported programming mode")
