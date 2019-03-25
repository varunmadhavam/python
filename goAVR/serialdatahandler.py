import serial
import threading
import serial.tools.list_ports
from time import sleep

class goavrserial:
    @staticmethod
    def getserialportlist():
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            #print("{}: {} [{}]".format(port, desc, hwid))
            print(port+":"+desc)

    def __init__(self, port, baud, dataqueue, event):
        self.ser = serial.Serial(port=port, baudrate=baud,timeout=0)
        self.queue=dataqueue
        self.stop=event

    def readserialdata(self):
        while not self.stop.is_set():
            data = self.ser.read(9999)
            if len(data) > 0:
                for x in range(0,len(data)):
                    self.queue.putdata(data[x])
                    print("put data in queue : "+str(data[x]))

    def writeserialdata(self, arrayofbytes):
        print("wrting data : "+str(arrayofbytes))
        self.ser.write(arrayofbytes)

    def run(self):
        t=threading.Thread(target=self.readserialdata)
        t.start()
    




