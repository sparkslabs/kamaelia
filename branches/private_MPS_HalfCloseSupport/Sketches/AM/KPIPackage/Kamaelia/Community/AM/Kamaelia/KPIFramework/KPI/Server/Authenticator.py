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
========================
Authenticator Component
========================
Authenticator is server side component of authentication. After
successful authentication, the process acts as a passthrough
for encrypted (data+session packets)

How does it work ?
------------------
The authentication process is based on the Needham-Scroeder protocol.
Authentication Sequence
1. The Authenticatee sends its Userid encrypted with root key.
2. The Authenticator obtains userid by decrypting the data received and
   looks up for the key corresponding to the user id. 
3. The Authenticator generates a random number, encrypts it
   with a user's key and sends it to the authenticatee.
4. The Authenticatee decrypts it, increments it by 1 and sends it back
   to the Authenticator. 
5. The Authenticator verifies if the number recieved is indeed the original
   number incremented by 1.
6. Authenticator sends SUCCESS Message
7. Authenticator waits for Authenticatee to send OK acknowledgement
8. After receiving acknowledgement, it sends new userid message to
   "notifyuser" outbox
9. It then subscribes to DataManagement backplane
10. It links its outbox with DataManagement subscribes outbox there by
   the encrypted (data + session keys) acting as passthrough
"""

#TODO:
#currently uses xtea as the encryption algorithm for challenge response
#communication. need to refactor to be able to plugin various ciphers
#Should be able to extend and override new authentication mechanisms

import Axon
import struct
import random
from Kamaelia.Util.Backplane import subscribeTo
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Crypto import xtea

class Authenticator(Axon.Component.component):
    """\   Authenticator(kpidb) -> new Authenticator component
    Handles authentication and acts as passthru for data traffic
    Keyword arguments:
    - kpidb    -- uses KPIDB instance for looking up user key from DB
    """
    
    Inboxes = {"inbox" : "receiving authentication packets",
               "control" : "receive shutdown messages"}
    Outboxes = {"outbox" : "sending authentication and data packets",
                "notifyuser" : "notify new user",
                "signal" : "pass shutdown messages"}

    def __init__(self, kpidb):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Authenticator,self).__init__()
        self.kpidb = kpidb

    def main(self):
        kpidb = self.kpidb
        while not self.dataReady("inbox"):
            yield 1
        data = self.recv("inbox")
        #got userid
        padding,userid = struct.unpack('!2L',
                    xtea.xtea_decrypt(kpidb.getRootKey(),data))

        #check if the user is valid
        if kpidb.isValidUser(userid) == False:
            #print "Invalid UserID" # todo shutdown
            return

        #generate a random number and encrypt it with user's key
        challenge = random.getrandbits(32)
        temp = struct.pack('!2L',0, challenge)
        #look up user key from key database
        userkey = kpidb.getKPIKeys().getKey(userid)
        data = xtea.xtea_encrypt(userkey, temp)
        #print data, challenge, userkey
        self.send(data, "outbox")
        yield 1
        while not self.dataReady("inbox"):
            yield 1
        #got response to challenge
        data = self.recv("inbox")
        temp = xtea.xtea_decrypt(userkey,data)
        padding, response = struct.unpack('!2L', temp)
        #validate response
        if response == challenge + 1:
            self.send("SUCCESS", "outbox")
            yield 1
        else:
            #print "authenication failure"
            return # shutdown

        #got OK ack
        while not self.dataReady("inbox"):
            yield 1
        data = self.recv("inbox")
        if data == "OK":
            #print "received ack from client"
            pass
        else:
            return #shutdown
            


        #notify new user
        self.send(userid, "notifyuser")

        #subscribe to DataManagement backplane
        subscriber = subscribeTo("DataManagement")
        #make authenticator passthrough the data from DataManagement backplane
        self.link( (subscriber, "outbox"), (self, "outbox"), passthrough=2)
        subscriber.activate()
        yield 1

        while 1:
            yield 1
