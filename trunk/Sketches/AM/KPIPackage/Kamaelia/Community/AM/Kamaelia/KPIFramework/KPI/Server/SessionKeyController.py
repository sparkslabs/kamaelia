#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
# -------------------------------------------------------------------------
#
"""
=======================
Session Key Controller
=======================
SessionKeyController is the core component of KPIFramework that handles
rekeying. SessionKeyController accepts key change triggers, generates a
new session key and communicates it to all the clients using common keys
shared by the active recipients. The commonkeys are determined by
the Logical Key Hierarchy algorithm.

How it works?
-------------
The component recieves the userid of the new user on the "userevent" inbox.
It generates a new session key. The new session key is encrypted with the
common keys and sent on the outbox to be transmitted to all the clients.
It is sent as clear text on  "notifykey" outbox so that the encryptor
can encrypt the plaintext content with it.
"""

import Axon
import random
import md5
import struct
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Crypto import xtea

class SessionKeyController(Axon.Component.component):
    """\   SessionKeyController(kpikeys) -> new SessionKeyController component
    Generates session keys and notifies all authenticated users
    Keyword arguments:
    - kpikeys    -- DB instance for obtaining common keys
    """    
    Inboxes = {"userevent" : "new user event",
               "control" : "receive shutdown messages"}
    Outboxes = {"outbox" : "encrypted session key packets",
                "notifykey" : "notify key",
                "signal" : "pass shutdown messages"}


    def __init__(self, kpikeys):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(SessionKeyController,self).__init__()
        self.kpikeys = kpikeys


    def main(self):
        kpikeys = self.kpikeys
        users = []

        while 1:
            while not self.dataReady("userevent"):
                yield 1

            userid = self.recv("userevent")
            #to avoid duplicate entries
            try:
                users.index(userid)
            except ValueError:
                users.append(userid)
                users.sort()

            #obtain common keys
            idkeymap = kpikeys.getCommonKeys(users)
            sessionKey = self.getSessionKey()

            #notify the session key
            self.send(sessionKey, "notifykey")

            #encrypt the session key with common keys
            for ID, key in idkeymap.iteritems():
                #packet structure - 8 bytes of ID and
                #16 bytes of encrypted session key
                idstr = struct.pack("!2L", 0, ID)
                cipher = xtea.xtea_encrypt(key, sessionKey[:8])
                cipher = cipher + xtea.xtea_encrypt(key, sessionKey[8:16])
                data = idstr + cipher
                self.send(data, "outbox")
            yield 1


    #sessionkey is a MD5 hash of four random numbers
    def getSessionKey(self):
        r1 = random.getrandbits(32)
        r2 = random.getrandbits(32)
        r3 = random.getrandbits(32)
        r4 = random.getrandbits(32)
        m = md5.new()
        m.update(struct.pack("!4L", r1, r3, r4, r2))
        return m.digest() 
