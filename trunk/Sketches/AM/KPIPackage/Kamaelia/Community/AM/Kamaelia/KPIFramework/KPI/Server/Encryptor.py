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
Encryptor encrypts the data with the key provided 

TODO
to be able plugin different data integrity algorithms 
"""

import Axon
import struct
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Crypto import xtea

class Encryptor(Axon.Component.component):
    Inboxes = {"inbox" : "data packets",
               "keyevent": "key for encryption",
               "control" : "receive shutdown messages"}
    Outboxes = {"outbox" : "encrypted data packets",
                "signal" : "pass shutdown messages"}

    def __init__(self,key="\0"):
        super(Encryptor,self).__init__()
        self.key = key


    def main(self):
        blocksize = 8 # to do generalize padding and breaking in to blocks
        fmtstr = '!'+ str(blocksize) +'s'
        MAGIC_STRING = blocksize * chr(0x80)
        while 1:
            yield 1

            if self.dataReady("keyevent"):
                self.key = self.recv("keyevent")
                #print "key recieved at the encryptor",self.key

            if self.dataReady("inbox"):
                data = self.recv("inbox")
                if self.key == "\0":
                    continue
                enc = ''
                i = 0
                #do padding if less than block size
                #Pad with 0x80 followed by zero (null) bytes
                datalen = len(data)
                if datalen > blocksize:
                    for i in range(0, datalen-blocksize, blocksize):
                        block = data[i:i+blocksize]
                        enc = enc + xtea.xtea_encrypt(self.key,block)
                    i = i + blocksize
                #get the last 8 bytes
                block = data[i:datalen]
                if len(block) == blocksize:
                    enc = enc + xtea.xtea_encrypt(self.key,block)
                    if block.find(chr(0x80)) != -1:
                        enc = enc + xtea.xtea_encrypt(self.key,MAGIC_STRING)
                else:
                    block = struct.pack(fmtstr, block + chr(0x80))
                    enc = enc + xtea.xtea_encrypt(self.key,block)
                self.send(enc, "outbox")
