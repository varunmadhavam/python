from struct import *
from time import sleep
from rpi.rpispi import rpispi
class rpiavr:
    def __init__(self,chipname,chipcode,pagesize_flash,pagesize_eeprom,flash_size,eeprom_size,twd_fuse,twd_flash,twd_eeprom,twd_erase,hex):
        self.chipname=chipname
        self.chipcode=chipcode
        self.pagesize_flash=pagesize_flash
        self.pagesize_eeprom=pagesize_eeprom
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
        sleep(1)
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
        self.spi.spi_transfer([0xAC,0x80,0x00,0x00])
        return True


    def write_flash(self,startaddress):
        program=self.hex.readhex()
        if(len(program)>self.flash_size):
            print("error....program size more than flash size")
            return
        k=0
        j=0
        i=0
        while k <= (len(program)-2):
            self.spi.spi_transfer([0x40,0x00,int.from_bytes(pack(">B",j&0xff),"little"),int.from_bytes(pack(">B",program[k]),"little")])
            self.spi.spi_transfer([0x48,0x00,int.from_bytes(pack(">B",j&0xff),"little"),int.from_bytes(pack(">B",program[k+1]),"little")])
            k+=2
            j=j+1
            if((k%(self.pagesize_flash*2))==0):
                sleep(self.twd_flash/1000)
                self.spi.spi_transfer([0x4C,int.from_bytes(pack(">B",i>>8),"little"),int.from_bytes(pack(">B",i&0xff),"little"),0x00])
                sleep(self.twd_flash/1000)
                j=0
                i=i+self.pagesize_flash
        if j < self.pagesize_flash and j > 0 :
                self.spi.spi_transfer([0x4C,int.from_bytes(pack(">B",i>>8),"little"),int.from_bytes(pack(">B",i&0xff),"little"),0x00])
                sleep(self.twd_flash/1000)


    def read_flash(self):
        arr = bytearray()
        for x in range(0,int((self.flash_size/2))):
            arr.append(self.spi.spi_transfer([0x28,int.from_bytes(pack(">B",x>>8),"little"),int.from_bytes(pack(">B",x&0xff),"little"),0x00])[3])
            arr.append(self.spi.spi_transfer([0x20,int.from_bytes(pack(">B",x>>8),"little"),int.from_bytes(pack(">B",x&0xff),"little"),0x00])[3])
        return arr