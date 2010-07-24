# -*- coding: utf-8 -*-
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
