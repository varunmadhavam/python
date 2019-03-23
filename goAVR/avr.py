class avr:
    def __init__(self,chipname,chipcode,wordsize_flash,wordsize_eeprom,flash_size,eeprom_size,twd_fuse,twd_flash,twd_eeprom,twd_erase,serialport,dataqueue):
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
            print("Error : Unexpected byte recieved while trying to leave programming mode")
            return False

    def read_signature(self):
        self.serialport.writeserialdata(b'\x93')
        data=self.dataqueue.getdata(3)
        return data

    