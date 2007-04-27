import Axon
import struct
from KPI.Crypto import xtea

class Encryptor(Axon.Component.component):
   Inboxes = {"inbox" : "data packets", "keyevent": "key for encryption", "control": "shutdown handling"}
   Outboxes = {"outbox" : "encrypted data packets", "signal": "shut handling"}    
   def __init__(self):
      super(Encryptor,self).__init__()
      self.key = "\0"

   def main(self):
    blocksize = 8 # to do generalize padding and breaking in to blocks
    fmtstr = '!'+ str(blocksize) +'s'
    MAGIC_STRING = blocksize * chr(0x80) 
    while 1:
      yield 1
      if self.dataReady("control"):
          data = self.recv("control")
          if data == "SHUTDOWN":
              self.send(data, "signal")
              print "encryptor shutdown"
              break
              
      if self.dataReady("keyevent"):
	    self.key = self.recv("keyevent")
	    #print "key recieved at the encryptor",self.key
	    
      if self.dataReady("inbox") and self.key != "\0":
            data = self.recv("inbox")
            enc = ''
            i = 0
            #do padding if less than block size
            #Pad with 0x80 followed by zero (null) bytes
            datalen = len(data)
            if datalen > blocksize:
                for i in range(0, datalen-blocksize, blocksize):
                    block = data[i:i+blocksize]
                    enc = enc + xtea.xtea_encrypt(self.key,block)
                i = i + blocksize
            #get the last 8 bytes
            block = data[i:datalen]
            if len(block) == blocksize:
                enc = enc + xtea.xtea_encrypt(self.key,block)
                if block.find(chr(0x80)) != -1:
                    enc = enc + xtea.xtea_encrypt(self.key,MAGIC_STRING)
            else:
                block = struct.pack(fmtstr, block + chr(0x80))
                enc = enc + xtea.xtea_encrypt(self.key,block)
            self.send(enc, "outbox")

