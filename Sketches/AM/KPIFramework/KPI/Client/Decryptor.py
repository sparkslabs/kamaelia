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
from KPI.Crypto import xtea

class Decryptor(Axon.Component.component):
   Inboxes = {"inbox" : "encrypted data packets", "keyevent": "key for decryption", "control": "shutdown handling"}
   Outboxes = {"outbox" : "decrypted data packets", "signal": "shut handling"}
   
   def __init__(self):
      super(Decryptor,self).__init__()
      self.key = "\0"

   def main(self):
      blocksize = 8
      MAGIC_STRING = blocksize * chr(0x80) 
      while 1:
         yield 1

         if self.dataReady("control"):
             data = self.recv("control")
             if data == "SHUTDOWN":
                 self.send(data, "signal")
                 print "decryptor shutdown"
                 break
            
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

