import queue
class dataqueue:
    def __init__(self,xsize):
        self.serialdata=queue.Queue(maxsize=xsize)
    def getdata(self,bytecount,timeout=10):
        arr = bytearray()
        #for x in range(0,bytecount):
        #   arr.append(self.serialdata.get(True,timeout))
        i=0
        while i < bytecount:
            try:
                arr.append(self.serialdata.get(True,timeout))
            except queue.Empty:
                print("empty queue continueing")
                continue
            i+=1
        
        return arr

    def putdata(self,abyte):
        self.serialdata.put(abyte)
    
    def qsize(self):
        return self.serialdata.qsize()
