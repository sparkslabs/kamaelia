import Axon
import random
import md5
import struct
from KPI.Crypto import xtea

class SessionKeyController(Axon.Component.component):
   Inboxes = {"userevent" : "new user event"}
   Outboxes = {"outbox" : "encrypted session key packets",
                "notifykey" : "notify key"}

   def __init__(self, kpikeys):
       super(SessionKeyController,self).__init__()
       self.kpikeys = kpikeys


   def main(self):
       kpikeys = self.kpikeys
       users = []
       
       while 1:
           while not self.dataReady("userevent"):
               yield 1
           print "SC sending a key"
           userid = self.recv("userevent")
           #to avoid duplicate entries
           try:
               users.index(userid)
           except ValueError:
               users.append(userid)
               users.sort()
           #todo to send in a format
           idkeymap = kpikeys.getCommonKeys(users)
           sessionKey = self.getSessionKey()
           print "idkeymap", idkeymap

           #encrypt the the session key with common keys
           for ID, key in idkeymap.iteritems():
               idstr = struct.pack("!2L", 0, ID)
               print "id,key", ID,len(key)
               cipher = xtea.xtea_encrypt(key, sessionKey[:8])
               cipher = cipher + xtea.xtea_encrypt(key, sessionKey[8:16])
               data = idstr + cipher
               self.send(data, "outbox")

           self.send(sessionKey, "notifykey")
           yield 1

   def getSessionKey(self):
       r1 = random.getrandbits(32)
       r2 = random.getrandbits(32)
       r3 = random.getrandbits(32)
       r4 = random.getrandbits(32)
       m = md5.new()
       m.update(struct.pack("!4L", r1, r3, r4, r2))
       return m.digest() 
