import queue
class dataqueue:
    def __init__(self,xsize):
        self.serialdata=queue.Queue(maxsize=xsize)
    def getdata(self,bytecount,timeout=10):
        arr = bytearray()
        for x in range(0,bytecount):
            arr.append(self.serialdata.get(True,timeout))
        return arr

    def putdata(self,abyte):
        self.serialdata.put(abyte)
