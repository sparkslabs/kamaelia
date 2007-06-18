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
