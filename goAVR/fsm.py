from time import sleep
class fsm:
    def __init__(self,mode,avr):
        self.mode=mode
        self.avr=avr
    
    def read_chipid(self):
        if self.avr.enable_programming():
            print(self.avr.read_signature())
            self.avr.leave_programming()
        else:
            print("Could not enter programming mode")
            self.avr.leave_programming()
    
    def write_flash(self,startaddress):
        if self.avr.enable_programming():
            sleep(self.avr.twd_flash/1000)
            self.avr.write_flash(startaddress)
            self.avr.leave_programming()
            print("Successfully uploaded flash")
        else:
            print("error entering programming mode")
            self.avr.leave_programming()

    def read_flash(self):
        if self.avr.enable_programming():
            print(self.avr.read_flash())
            self.avr.leave_programming()
        else:
            print("Could not enter programming mode")
            self.avr.leave_programming()

    def erase_chip(self):
        if self.avr.enable_programming():
            print("chip erase cycle initiated")
            if self.avr.chip_erase():
                sleep(self.avr.twd_erase/1000)
                print("chip erased successfully")
                self.avr.leave_programming()
                return True
            else:
                print("Error erasing chip")
                self.avr.leave_programming()
                return False
        else:
            print("Could not enter programming mode")
            self.avr.leave_programming()
            return False


    def run(self):
        if self.mode == 0 :
            if self.erase_chip():
                print("flash erased. Trying to upload flash")
                self.write_flash(0)
            else:
                print("error trying to erase flash")
        elif self.mode == 1 :
            self.read_chipid()
        elif self.mode == 2:
            self.read_flash()
        elif self.mode == 3:
            self.erase_chip()
        else:
            print("Unknow mode")