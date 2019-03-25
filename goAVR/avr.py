from struct import *
from time import sleep
class avr:
    def __init__(self,chipname,chipcode,wordsize_flash,wordsize_eeprom,flash_size,eeprom_size,twd_fuse,twd_flash,twd_eeprom,twd_erase,serialport,dataqueue,hex):
        self.chipname=chipname
        self.chipcode=chipcode
        self.wordsize_flash=wordsize_flash
        self.wordsize_eeprom=wordsize_eeprom
        self.flash_size=flash_size
        self.eeprom_size=eeprom_size
        self.twd_fuse=twd_fuse
        self.twd_flash=twd_flash
        self.twd_eeprom=twd_eeprom
        self.twd_erase=twd_erase
        self.serialport=serialport
        self.dataqueue=dataqueue
        self.hex=hex

    def enable_programming(self):
        self.serialport.writeserialdata(b'\x91')
        data=self.dataqueue.getdata(2)
        if bytes([data[0]]) == b'\x00':
            if bytes([data[1]]) == b'\x02':
                return True
            else:
                print("Error : Unexpected return code")
                return False
        elif bytes([data[0]]) == b'\x01':
            print("Error : Sync error")
            return False
        else:
            print("Error : Unexpected byte recieved while trying to intialize programming mode")
            print(bytes([data[0]]))
            print(b'\x00')
            return False
        print("Queue after enable programming : "+str(self.dataqueue.qsize()))
    
    def leave_programming(self):
        self.serialport.writeserialdata(b'\x92')
        data=self.dataqueue.getdata(2)
        if bytes([data[0]]) == b'\x00':
            if bytes([data[1]]) == b'\x03':
                return True
            else:
                print("Error : Unexpected return code")
                return False
        elif bytes([data[0]]) == b'\x01':
            print("Error while leaving programming mode")
            return False
        else:
            return False

    def read_signature(self):
        self.serialport.writeserialdata(b'\x93')
        data=self.dataqueue.getdata(3)
        return data

    def write_flash(self):
        self.serialport.writeserialdata(b'\x98')
        self.serialport.writeserialdata(bytes(pack(">B",self.wordsize_flash)))
        self.serialport.writeserialdata(bytes(pack(">B",self.twd_flash)))
        self.serialport.writeserialdata(b'\x00')
        self.serialport.writeserialdata(b'\x00')
        program=self.hex.readhex()
        if(len(program)>self.flash_size):
            print("error....program size more than flash size")
            return
        self.serialport.writeserialdata(bytes(pack(">B",len(program)>>8)))
        self.serialport.writeserialdata(bytes(pack(">B",len(program)&0xff)))
        k=0
        j=0
        while k <= (len(program)-2):
            print("k is "+str(k))
            self.serialport.writeserialdata(bytes(pack(">B",program[k])))
            self.serialport.writeserialdata(bytes(pack(">B",program[k+1])))
            k+=2
            if((k%(self.wordsize_flash*2))==0):
                print("k waiting for data is "+str(k))
                retcode=self.dataqueue.getdata(1)
                if not (bytes([retcode[0]]) == b'\x80'):
                   print("error unidentified sync token recieved.")
                   break
                else:
                    print("reached a page buffer..continueing")
        print("waiting for last sycn byte")
        retcode=self.dataqueue.getdata(1)
        if not (bytes([retcode[0]]) == b'\x88'):
                   print("error unidentified sync token recieved.")