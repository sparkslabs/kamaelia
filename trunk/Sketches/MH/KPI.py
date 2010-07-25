#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
# -------------------------------------------------------------------------
#
import Axon
from Kamaelia.Util.PipelineComponent import pipeline

from Kamaelia.File.Reading import RateControlledFileReader
from Kamaelia.File.Writing import SimpleFileWriter


import xxtea
class Encryptor(Axon.Component.component):
   def __init__(self,key):
      super(Encryptor,self).__init__()
      self.key = key
   
   def main(self):
      while self.dataReady("inbox") or not self.dataReady("control"):   # really messy shutdown hack - should really check the kind of message received on "control" inbox
         while self.dataReady("inbox"):
            data = self.recv("inbox")
            enc = xxtea.xxbtea(data,2,"AABBCCDDEE0123456789AABBCCDDEEFF")
            self.send(enc, "outbox")
         if not self.anyReady():
             self.pause()
         yield 1
      self.send(self.recv("control"),"signal")

class Decryptor(Axon.Component.component):
   def __init__(self,key):
      super(Decryptor,self).__init__()
      self.key = key
   
   def main(self):
      while self.dataReady("inbox") or not self.dataReady("control"):   # really messy shutdown hack - should really check the kind of message received on "control" inbox
         while self.dataReady("inbox"):
            data = self.recv("inbox")
            dec = xxtea.xxbtea(data,-2,"AABBCCDDEE0123456789AABBCCDDEEFF")
            self.send(dec, "outbox")
         if not self.anyReady():
             self.pause()
         yield 1
      self.send(self.recv("control"),"signal")
        

class echoer(Axon.Component.component):
    def main(self):
        count = 0
        while 1:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                print  data, "count:", count
                count = count +1
            self.pause()
            yield 1

      

if __name__=="__main__": 
    pipeline(
        RateControlledFileReader("../AM/KPIFramework/SelfishTriangle.jpg",readmode="bytes",rate=100000,chunksize=8),
        Encryptor("12345678901234567890123456789012"),
        Decryptor("12345678901234567890123456789012"),
        SimpleFileWriter("SelfishTriangle-dec.jpg")
    ).run()

