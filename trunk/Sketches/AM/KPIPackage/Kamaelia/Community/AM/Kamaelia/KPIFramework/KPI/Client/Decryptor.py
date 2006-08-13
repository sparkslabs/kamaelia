#!/usr/bin/env python2.3
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""
Decryptor decrypts the cipher data with the key provided 

TODO
to be able plugin different data integrity algorithms 
"""

import Axon
import struct
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Crypto import xtea

class Decryptor(Axon.Component.component):
    Inboxes = {"inbox" : "encrypted data packets",
               "keyevent": "key for decryption",
               "control": "shutdown handling"}
    Outboxes = {"outbox" : "decrypted data packets",
                "signal": "shutdown handling"}

    def __init__(self):
        super(Decryptor,self).__init__()
        self.key = "\0"

    def main(self):
        blocksize = 8
        MAGIC_STRING = blocksize * chr(0x80)
        while 1:
            yield 1

            if self.dataReady("keyevent"):
                self.key = self.recv("keyevent")
                #print "key recieved at the decryptor",self.key

            if self.dataReady("inbox") and self.key != "\0":
                data = self.recv("inbox")
                dec = ''
                pad = True
                datalen = len(data)
                #Unpad last byte with 0x80 followed by zero (null) bytes
                if datalen > blocksize:
                    k = 0
                    if datalen > 2*blocksize:
                        for i in range(0, datalen - 2*blocksize, blocksize):
                            block = data[i:i+blocksize]
                            dec = dec + xtea.xtea_decrypt(self.key,block)
                        k = i + blocksize
                    block1 = xtea.xtea_decrypt(self.key,data[k:k+blocksize])
                    block2 = xtea.xtea_decrypt(self.key,data[k+blocksize:datalen])
                    dec = dec + block1
                    if block2 == MAGIC_STRING:
                        pad = False
                    else:
                        block = block2
                else:
                    block = xtea.xtea_decrypt(self.key,data)

                if pad == True:
                    rindex = block.rfind(chr(0x80))
                    if rindex != -1:
                        tmp = block[rindex:len(block)]
                        pad = chr(0x80) + (len(block)-rindex-1)*chr(0x00)
                        if(pad == tmp):
                            print "remove padding", pad, "padlen", len(pad)
                            block = block[:rindex]
                    dec = dec + block
                #print "decrypted data ",dec
                self.send(dec, "outbox")
