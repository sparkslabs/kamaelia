#!/usr/bin/env python
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
=====================
Decryptor Component
=====================
Decryptor decrypts the encrypted data on its inbox with the key.The key
is passed as constructor param or sent to its "keyevent" inbox

Example usage
-------------
key = "1234567890123456"
pipeline (
    chargen(),
    Encryptor(key),
    Decryptor(key),
    consoleEchoer()
).run()
    
How it works?
--------------
Decryptor uses xtea cipher for encryption. xtea is a block cipher whose block
size is 8 bytes and key length is 16 bytes. The decryptor after decrypting
data looks for looks for padding, if it finds padding, it strips
the padding and sends the decrypted data to its outbox

"""
#TODO
#to be able plugin different ciphers
#separate unpadding from decryption

import Axon
import struct
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Crypto import xtea

class Decryptor(Axon.Component.component):
    """\   Decryptor([key]) -> new Decryptor component.
    Decrypts data and sends to outbox
    Keyword arguments:
    - key    -- key string (default="\0")
    """    
    Inboxes = {"inbox" : "encrypted data packets",
               "keyevent": "key for decryption",
               "control": "receive shutdown messages"}
    Outboxes = {"outbox" : "decrypted data packets",
                "signal" : "pass shutdown messages"}

    def __init__(self, key="\0"):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Decryptor,self).__init__()
        self.key = key

    def main(self):
        blocksize = 8
        #MAGIC_STRING indicates that its preceding block is not padded
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
                    #if data contains more than two blocks
                    if datalen > 2*blocksize:
                        #decrypt all the blocks
                        for i in range(0, datalen - 2*blocksize, blocksize):
                            block = data[i:i+blocksize]
                            #since the data is not padding, append it to
                            #dec string
                            dec = dec + xtea.xtea_decrypt(self.key,block)
                        k = i + blocksize
                    #decrypt last two blocks
                    block1 = xtea.xtea_decrypt(self.key,data[k:k+blocksize])
                    block2 = xtea.xtea_decrypt(self.key,data[k+blocksize:datalen])
                    #if the last block contains magic string
                    #it indicates that there is no padding for block1
                    dec = dec + block1
                    if block2 == MAGIC_STRING:
                        pad = False
                    else:
                        block = block2
                else:
                    block = xtea.xtea_decrypt(self.key,data)

                if pad == True:
                    #find the position of the last occurence of 0x80
                    rindex = block.rfind(chr(0x80))
                    if rindex != -1:
                        tmp = block[rindex:len(block)]
                        #if the substring is equal to 0x80 followed null bytes
                        pad = chr(0x80) + (len(block)-rindex-1)*chr(0x00)
                        if(pad == tmp):
                            #remove padding
                            block = block[:rindex]
                    dec = dec + block
                #print "decrypted data ",dec
                self.send(dec, "outbox")
