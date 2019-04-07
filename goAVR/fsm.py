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
    
    def write_flash(self):
        if self.avr.enable_programming():
            if self.avr.chip_erase():
                sleep(self.avr.twd_erase/1000)
                self.avr.leave_programming()
                if self.avr.enable_programming():
                    self.avr.write_flash()
                    self.avr.leave_programming()
                else:
                    print("error entering programming mode after chip erase")
            else:
                print("error erasing chip")
        else:
            print("Could not enter programming mode")

    def read_flash(self):
        if self.avr.enable_programming():
            self.avr.read_flash()
        else:
            print("Could not enter programming mode")


    def run(self):
        if self.mode == 0 :
            self.write_flash()
        elif self.mode == 1 :
            self.read_chipid()
        elif self.mode == 2:
            self.read_flash()
        else:
            print("Unknow mode")