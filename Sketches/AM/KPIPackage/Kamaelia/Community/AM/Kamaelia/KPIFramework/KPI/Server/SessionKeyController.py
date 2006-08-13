#!/usr/bin/env python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
#
"""
SessionKeyController accepts key change triggers, generates a new session key
and communicates it to all the clients using common keys it shares with the
selected recipients. The actual keys that will be used are determined by the
Logical Key Hierarchy algorithm.
"""
import Axon
import random
import md5
import struct
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Crypto import xtea

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
           print "SC->sessionkey", sessionKey

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
