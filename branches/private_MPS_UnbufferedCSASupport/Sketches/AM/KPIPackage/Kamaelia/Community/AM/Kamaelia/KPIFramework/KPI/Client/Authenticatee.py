#!/usr/bin/env python
#
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
=========================
Authenticatee Component
=========================
Authenticatee is client side component of authentication. After successful
authentication, it depacketizes the data and key packets

How it works ?
--------------
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
7. Authenticatee sends back "OK" ack
8. After succesful authentication, Authenticatee reads incoming packet's
   header. if it is key packet, it decrypts and sends to "notifykey" outbox
9. If its data packet, it sends data to "encout" outbox
10. Note: Authenticator takes care of packets of different sizes. 
"""

#TODO:
#currently uses xtea as the encryption algorithm for challenge response
#communication with authenticator. need to refactor to be able to plugin
#various ciphers
#separate authenticatee and depackizer into two components.
#Should be able to extend and override new authentication mechanisms

import struct
import Axon
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Crypto import xtea


class Authenticatee(Axon.Component.component):
    """\   Authenticator(kpiuser) -> new Authenticatee component
    Handles authentication and depacketizing
    Keyword arguments:
    - kpiuser    -- uses KPIUser instance for looking up user
                    key from client config file
    """
    Inboxes = {"inbox" : "authentication and data packets",
               "control" : "receive shutdown messages"}
    Outboxes = {"outbox" : "authentication",
                "encout" : "encrypted data packets",
                "notifykey" : "notify key",
               "signal" : "pass shutdown messages"}

    def __init__(self, kpiuser):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Authenticatee,self).__init__()
        self.kpiuser = kpiuser

    def main(self):
        #encrypt user id with root key
        userid = self.kpiuser.getID()
        data = xtea.xtea_encrypt(self.kpiuser.getRootKey(),
                                 struct.pack('!2L',0, userid))
        self.send(data, "outbox")
        yield 1

        while not self.dataReady("inbox"):
            yield 1
        data = self.recv("inbox")
        #receive challenge
        temp = xtea.xtea_decrypt(self.kpiuser.getUserKey(), data)
        padding, challenge = struct.unpack('!2L',temp)
        response = challenge+1

        #sending response encrypted with my key
        data = xtea.xtea_encrypt(self.kpiuser.getUserKey(),
                                 struct.pack('!2L',0, response))
        
        
        self.send(data, "outbox")
        yield 1
        while not self.dataReady("inbox"):
            yield 1
        data = self.recv("inbox")
        if data == "SUCCESS":
            #print "authentication success"
            pass
        else:
            #print "authenication failure"
            return #shutdown

        #Send OK ack to authenticator
        self.send("OK", "outbox")
        yield 1

        #decode data
        #the depacketizer has to modes
        #reading header or reading body
        buffer = ''
        KEY = 0x20        
        DATA = 0x30
        READ_HEADER = 1
        READ_BODY = 2
        HEADER_LEN = 8
        mode = READ_HEADER
        HEADER_SIZE = 8
        while 1:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                buffer = buffer + data
                if mode == READ_HEADER :
                    if len(buffer) >= HEADER_SIZE:
                        mode = READ_BODY
                        header = buffer[:HEADER_SIZE]
                        packetType, data2read = struct.unpack("!2L", header)
                        #Bug fix - previously was reading less
                        #data from buffer -> body = buffer[HEADER_SIZE:data2read]
                        #this caused the client to be slower in receiving data
                        body = buffer[HEADER_SIZE:HEADER_SIZE+data2read]
                        #read the body
                        if data2read <= len(body):
                            mode = READ_HEADER
                            if packetType == KEY:
                                #key packet structure
                                #8 bytes  - key ID with which session key was encrypted
                                #16 bytes of encrypted session key
                                padding,ID = struct.unpack("!2L", body[:8])
                                try:
                                    key = self.kpiuser.getKey(ID)
                                    #i have the key for the ID
                                    enckey = body[8:data2read]
                                    part1 = xtea.xtea_decrypt(key, enckey[:8])
                                    part2 = xtea.xtea_decrypt(key, enckey[8:16])
                                    sessionkey = part1 + part2
                                    self.send(sessionkey, "notifykey")
                                except KeyError:
                                    pass #the key is not for me
                            elif packetType == DATA:
                                #print "decoded data", body
                                self.send(body, "encout")
                            # remove the header + data read
                            buffer = buffer[(data2read+HEADER_SIZE):len(buffer)]
                        else:
                            #remove header
                            buffer = buffer[HEADER_SIZE:len(buffer)]
                elif mode == READ_BODY:
                    body = buffer[:data2read]
                    #data2read = data2read - len(buffer)
                    #read all the data
                    if data2read <= len(body):
                        mode = READ_HEADER
                        if packetType == KEY:
                            #key packet structure
                            #8 bytes  - key ID with which session key was encrypted
                            #16 bytes of encrypted session key                            
                            padding,ID = struct.unpack("!2L", body[:8])
                            try:
                                key = self.kpiuser.getKey(ID)
                                enckey = body[8:data2read]
                                part1 = xtea.xtea_decrypt(key, enckey[:8])
                                part2 = xtea.xtea_decrypt(key, enckey[8:16])
                                sessionkey = part1 + part2
                                self.send(sessionkey, "notifykey")
                            except KeyError:
                                pass #the key is not for me
                        elif packetType == DATA:
                            self.send(body, "encout")
                        # remove the data read
                        buffer = buffer[data2read:len(buffer)]
            yield 1
