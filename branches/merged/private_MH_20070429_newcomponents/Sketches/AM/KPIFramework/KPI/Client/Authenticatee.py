import struct
import Axon
from KPI.Crypto import xtea


class Authenticatee(Axon.Component.component):
    Inboxes = {"inbox" : "authentication and data packets"}
    Outboxes = {"outbox" : "authentication",
                "encout" : "encrypted data packets",
                "notifykey" : "notify key"}

    def __init__(self, kpiuser):
      super(Authenticatee,self).__init__()
      self.kpiuser = kpiuser
   
    
    def main(self):
        userid = self.kpiuser.getID()
        data = xtea.xtea_encrypt(self.kpiuser.getRootKey(),
                                 struct.pack('!2L',0, userid))
        print "encrypting user id with user key", self.kpiuser.getID(), self.kpiuser.getRootKey()
        self.send(data, "outbox")
        yield 1

        while not self.dataReady("inbox"):
            yield 1
        data = self.recv("inbox")
        temp = xtea.xtea_decrypt(self.kpiuser.getUserKey(), data)
        padding, challenge = struct.unpack('!2L',temp)
        response = challenge+1
        print "received challenge",challenge
        print "sending response", response
        data = xtea.xtea_encrypt(self.kpiuser.getUserKey(),
                                 struct.pack('!2L',0, response))
        
        
        self.send(data, "outbox")
        yield 1
        while not self.dataReady("inbox"):
            yield 1
        data = self.recv("inbox")
        if data == "SUCCESS":
            print "authentication success"
        else:
            print "authenication failure"
            return

        #decode data
        while 1:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                print "decoder", data
                if data.startswith("KEY"):
                    index = len("KEY")
                    #get the ID
                    padding,ID = struct.unpack("!2L", data[index:index+8])
                    print "****ID****", ID
                    key = ""
                    try:
                        key = self.kpiuser.getKey(ID)
                    except KeyError:
                        pass #the key is not for me

                    if key != "":
                        enckey = data[index+8:len(data)]
                        part1 = xtea.xtea_decrypt(key, enckey[:8])
                        part2 = xtea.xtea_decrypt(key, enckey[8:16])
                        sessionkey = part1 + part2
                        print "decoded key", sessionkey
                        self.send(sessionkey, "notifykey")
                else:
                    data = data[len("DAT"):len(data)]
                    print "decoded data", data
                    self.send(data, "encout")
            yield 1
