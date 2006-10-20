import Axon
import struct
import random
from Kamaelia.Util.Backplane import subscribeTo
from KPI.Crypto import xtea

class Authenticator(Axon.Component.component):
    Inboxes = {"inbox" : "authentication and data packets"}
    Outboxes = {"outbox" : "authentication",
                "notifyuser" : "user notification"}

    def __init__(self, kpidb):
      super(Authenticator,self).__init__()
      self.kpidb = kpidb

    
    def main(self):
        kpidb = self.kpidb
        while not self.dataReady("inbox"):
            yield 1
        data = self.recv("inbox")
        padding,userid = struct.unpack('!2L',
                xtea.xtea_decrypt(kpidb.getRootKey(),data))
        print "Authenticator received userid:", userid
        if kpidb.isValidUser(userid) == False:
            print "Invalid UserID" # todo shutdown
            return

        challenge = random.getrandbits(32)
        temp = struct.pack('!2L',0, challenge)
        userkey = kpidb.getKPIKeys().getKey(userid)
        data = xtea.xtea_encrypt(userkey, temp)
        print data, challenge, userkey
        self.send(data, "outbox")
        yield 1
        while not self.dataReady("inbox"):
            yield 1
        data = self.recv("inbox")
        temp = xtea.xtea_decrypt(userkey,data)
        padding, response = struct.unpack('!2L', temp)
	print data, response
	if response == challenge + 1:
            self.send("SUCCESS", "outbox")
            yield 1
        else:
            print "authenication failure"
            return # shutdown

        #new user added 
        self.send(userid, "notifyuser")

        #subscribe to data Management back plane
        subscriber = subscribeTo("DataManagement")
        self.link( (subscriber, "outbox"), (self, "outbox"), passthrough=2)
        subscriber.activate()
        yield 1

        while 1:
            yield 1
