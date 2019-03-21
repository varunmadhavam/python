from hex import hex
from dataqueue import dataqueue
from serialdatahandler import goavrserial
import threading
from time import sleep
#hexdata = hex("/home/varun/coding/c/avr/blinky/bin/blinky.hex")
#print(hexdata.readhex())

serialdataqueue = dataqueue(50)
stopping = threading.Event()
goavrserial.getserialportlist()
serialadapter = goavrserial('/dev/ttyACM0',57600,serialdataqueue,stopping)
serialadapter.run()
sleep(2)
serialadapter.writeserialdata(b'\x91')
sleep(2)
stopping.set()
barray=serialdataqueue.getdata(2)
print(barray)
