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

class Encryptor(Axon.Component.component):
   Inboxes = {"inbox" : "data packets", "keyevent": "key for encryption", "control": "shutdown handling"}
   Outboxes = {"outbox" : "encrypted data packets", "signal": "shut handling"}    
   def __init__(self):
      super(Encryptor,self).__init__()
      self.key = "\0"

   def main(self):
    blocksize = 8 # to do generalize padding and breaking in to blocks
    fmtstr = '!'+ str(blocksize) +'s'
    MAGIC_STRING = blocksize * chr(0x80) 
    while 1:
      yield 1
      if self.dataReady("control"):
          data = self.recv("control")
          if data == "SHUTDOWN":
              self.send(data, "signal")
              print "encryptor shutdown"
              break
              
      if self.dataReady("keyevent"):
	    self.key = self.recv("keyevent")
	    #print "key recieved at the encryptor",self.key
	    
      if self.dataReady("inbox") and self.key != "\0":
            data = self.recv("inbox")
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

