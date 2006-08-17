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
Authenticator is server side component of authentication
After successful authentication, it notifies the key management
backplane about the arrival of a new user. It also registers to data
backplane to receive data. It acts as passthrough for the encrypted
(data + session keys)

The authentication process is based on the Needham-Scroeder protocol.
The authenticatee sends it userid encrypted with common key. The authenticator
looks up for the key corresponding to the user id. The authenticator generates
a random number, encrypts it with a user's key and sends it to the
authenticatee. The authenticatee decrypts it, increments it by 1 and sends
it back to the authenticator. The authenticator verifies if the number
recieved is indeed the original number incremented by 1. If so the
authentication process is successful.


TODO:
currently uses xtea as the encryption algorithm for challenge response
communication. need to refactor to be able to plugin different encryption
algos
Should be able to extend and override new authentication mechanisms
"""
import Axon
import struct
import random
from Kamaelia.Util.Backplane import subscribeTo
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Crypto import xtea

class Authenticator(Axon.Component.component):
    Inboxes = {"inbox" : "authentication and data packets",
               "control" : "receive shutdown messages"}
    Outboxes = {"outbox" : "authentication",
                "notifyuser" : "user notification",
                "signal" : "pass shutdown messages"}

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
        #print "Authenticator received userid:", userid
        if kpidb.isValidUser(userid) == False:
            #print "Invalid UserID" # todo shutdown
            return

        challenge = random.getrandbits(32)
        temp = struct.pack('!2L',0, challenge)
        userkey = kpidb.getKPIKeys().getKey(userid)
        data = xtea.xtea_encrypt(userkey, temp)
        #print data, challenge, userkey
        self.send(data, "outbox")
        yield 1
        while not self.dataReady("inbox"):
            yield 1
        data = self.recv("inbox")
        temp = xtea.xtea_decrypt(userkey,data)
        padding, response = struct.unpack('!2L', temp)
        #print data, response
        if response == challenge + 1:
            self.send("SUCCESS", "outbox")
            yield 1
        else:
            #print "authenication failure"
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
