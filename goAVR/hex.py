class hex:
    def __init__(self,hexfile):
        self.hexfile=hexfile
        self.isFirstLine=1
        self.hexstring=""

    def readhex(self):
        with open(self.hexfile) as f:
            for line in f:
                if line[0:1] != ':':
                    print("error..ivalid start of line")
                    break
                else:
                    if line[7:9] == "01":
                        break
                    elif line[7:9] == "00":
                        self.hexstring+=line[9:len(line)-3]
                        if self.isFirstLine == 1:
                            self.isFirstLine = 0
                            if line[3:7] != "0000":
                                print("error...start address not 0000..function not implemented")
                                break
                    else:
                        print("Unhandled record type in hex file.")
                        break
        return(bytes(bytearray.fromhex(self.hexstring)))