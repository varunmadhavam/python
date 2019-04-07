from struct import *
from time import sleep
from rpi.rpispi import rpispi
class rpiavr:
    def __init__(self,chipname,chipcode,wordsize_flash,wordsize_eeprom,flash_size,eeprom_size,twd_fuse,twd_flash,twd_eeprom,twd_erase,hex):
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
        self.hex=hex
        self.spi=rpispi()

    def enable_programming(self):
        self.spi.toggle_reset()
        res=self.spi.spi_transfer([0xAC,0x53,0x00,0x00])

        if res[2] == 83: #0x53
            print("Programming mode entered successfully")
            return True
        else:
            print("Error : Unexpected byte recieved while trying to intialize programming mode")
            return False

    def leave_programming(self):
        print("Leaving Programming Mode")
        self.spi.unhold_reset()
        return True

    def read_signature(self):
        arr = bytearray()
        res=self.spi.spi_transfer([0x30,0x00,0x00,0x00])
        arr.append(res[3])
        res=self.spi.spi_transfer([0x30,0x00,0x01,0x00])
        arr.append(res[3])
        res=self.spi.spi_transfer([0x30,0x00,0x02,0x00])
        arr.append(res[3])
        return arr

    def chip_erase(self):
        self.serialport.writeserialdata(b'\x94')
        data=self.dataqueue.getdata(2)
        if bytes([data[0]]) == b'\x00':
            if bytes([data[1]]) == b'\x94':
                return True
            else:
                print("Error : Unexpected return code")
                return False
        else:
            print("error while erasing chip")
            return False


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
            retcode=self.dataqueue.getdata(1)
            if (bytes([retcode[0]]) == b'\x98'):
                continue
            else:
                print("Error Not recieved sysnc after writing 2 bytes of flash")
                break
        print("waiting for last sycn byte")
        retcode=self.dataqueue.getdata(1)
        if not (bytes([retcode[0]]) == b'\x88'):
                   print("error unidentified sync token recieved.")

    def read_flash(self):
        self.serialport.writeserialdata(b'\x97')
        self.serialport.writeserialdata(bytes(pack(">B",self.flash_size>>8)))
        self.serialport.writeserialdata(bytes(pack(">B",self.flash_size&0xff)))
        arr = bytearray()
        for x in range(1,self.flash_size):
            #arr.append(bytes([self.dataqueue.getdata(1)]))
            print(self.dataqueue.getdata(1))
        #print(arr)