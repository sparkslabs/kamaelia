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

