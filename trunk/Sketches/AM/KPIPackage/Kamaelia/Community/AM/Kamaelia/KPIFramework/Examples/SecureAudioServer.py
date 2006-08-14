from AudioLib import *
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.SimpleServerComponent import SimpleServer as _SimpleServer
from Kamaelia.Internet.TCPClient import TCPClient as _TCPClient
from Kamaelia.Util.Backplane import *
from Kamaelia.Util.Graphline import *





import struct
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Crypto import xtea

class Encryptor(Axon.Component.component):
    def __init__(self, key):
        super(Encryptor,self).__init__()
        self.key = key
        


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

            if self.dataReady("inbox"):
                data = self.recv("inbox")
                if self.key == "\0":
                    continue
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





def clientconnector():
    return subscribeTo("AudioServer")

Backplane("AudioServer").activate()
server=_SimpleServer(protocol=clientconnector, port=1256).activate()
pipeline(AudioSource(100000),
         AudioEncoder('mp3'),
         Encryptor("1234567890123456"),         
         publishTo("AudioServer")
        ).run()




