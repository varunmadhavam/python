from hex import hex
from dataqueue import dataqueue
from serialdatahandler import goavrserial
from fsm import fsm
from avr import avr
import threading
from time import sleep

hexdata = hex("/home/varun/coding/c/avr/blinky8/bin/blinky8.hex")
serialdataqueue = dataqueue(50)
stopping = threading.Event()
goavrserial.getserialportlist()
serialadapter = goavrserial('/dev/ttyACM0',9600,serialdataqueue,stopping)
chip=avr(0,0,32,0,8192,0,0,20,0,0,serialadapter,serialdataqueue,hexdata)
mode=fsm(0,chip)
serialadapter.run()
sleep(2)
mode.run()
sleep(2)
stopping.set()


avrdude -c usbasp -p m8 -u -U flash:w:io.hex