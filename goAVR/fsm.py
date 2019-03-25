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
            self.avr.write_flash()
            self.avr.leave_programming()
        else:
            print("Could not enter programming mode")

    def run(self):
        if self.mode == 0 :
            self.write_flash()
        elif self.mode == 1 :
            self.read_chipid()
        else:
            print("Unknow mode")