from hex import hex
from dataqueue import dataqueue
from serialdatahandler import goavrserial
from fsm import fsm
from avr import avr
import threading
from time import sleep
#hexdata = hex("/home/varun/coding/c/avr/blinky/bin/blinky.hex")
#print(hexdata.readhex())

serialdataqueue = dataqueue(50)
stopping = threading.Event()
goavrserial.getserialportlist()
serialadapter = goavrserial('/dev/ttyACM0',57600,serialdataqueue,stopping)
chip=avr(0,0,0,0,0,0,0,0,0,0,serialadapter,serialdataqueue)
mode=fsm(1,chip)
serialadapter.run()
sleep(2)
mode.run()
sleep(2)
stopping.set()
