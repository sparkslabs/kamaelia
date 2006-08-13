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
Authenticatee is client side component of authentication
After successful authentication, it acts as pass through for
the encrypted data. It decodes all key packets and data packets
and notifies the decryptor

TODO:
currently uses xtea as the encryption algorithm for challenge response
communication with authenticator. need to refactor to be able to plugin
different encryption algos

separate authenticatee and passthrough decoder into two components.
make authenticatee signal about the authentication status

Should be able to extend and override new authentication mechanisms
"""

import struct
import Axon
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Crypto import xtea


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
                print "decoder", data

                buffer = buffer + data
                if mode == READ_HEADER :
                    if len(buffer) >= HEADER_SIZE:
                        mode = READ_BODY
                        header = buffer[:HEADER_SIZE]
                        packetType, data2read = struct.unpack("!2L", header)
                        body = buffer[HEADER_SIZE:data2read]
                        print "packet type->", hex(packetType)
                        print "data 2 read", data2read
                        #read all the data
                        if data2read <= len(body):
                            mode = READ_HEADER
                            if packetType == KEY:
                                padding,ID = struct.unpack("!2L", body[:8])
                                print "****ID****", ID
                                try:
                                    key = self.kpiuser.getKey(ID)
                                    enckey = body[8:data2read]
                                    print "size of enckey", len(enckey)
                                    part1 = xtea.xtea_decrypt(key, enckey[:8])
                                    part2 = xtea.xtea_decrypt(key, enckey[8:16])
                                    sessionkey = part1 + part2
                                    print "decoded key", sessionkey
                                    self.send(sessionkey, "notifykey")
                                except KeyError:
                                    pass #the key is not for me
                            elif packetType == DATA:
                                print "decoded data", body
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
                            padding,ID = struct.unpack("!2L", body[:8])
                            print "****ID****", ID
                            try:
                                key = self.kpiuser.getKey(ID)
                                enckey = body[8:data2read]
                                part1 = xtea.xtea_decrypt(key, enckey[:8])
                                part2 = xtea.xtea_decrypt(key, enckey[8:16])
                                sessionkey = part1 + part2
                                print "decoded key", sessionkey
                                self.send(sessionkey, "notifykey")
                            except KeyError:
                                pass #the key is not for me
                        elif packetType == DATA:
                            print "decoded data", body
                            self.send(body, "encout")
                        # remove the data read
                        buffer = buffer[data2read:len(buffer)]
            yield 1
