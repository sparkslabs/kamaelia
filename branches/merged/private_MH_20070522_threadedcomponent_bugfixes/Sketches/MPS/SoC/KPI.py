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
# MPS's experimental backplane code
import Axon
from Axon.Ipc import newComponent
from Kamaelia.Util.Splitter import PlugSplitter as Splitter
from Kamaelia.Util.Splitter import Plug
from Axon.AxonExceptions import ServiceAlreadyExists
from Axon.CoordinatingAssistantTracker import coordinatingassistanttracker as CAT
from Kamaelia.Util.passThrough import passThrough
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Backplane import *


class MyReader(Axon.Component.component):
    def main(self):
        while 1:
 #           line = raw_input(self.prompt)
            line = "hello"
            line = line + "\n"
            self.send(line, "outbox")
            yield 1


import xxtea
class Encryptor(Axon.Component.component):
   def __init__(self,key):
      super(Encryptor,self).__init__()
      self.key = key
   
   def main(self):
      while 1:
         self.pause()
	 yield 1
	 while self.dataReady("inbox"):
	    data = self.recv("inbox")
	    print "encrypting data: ",data
	    print data
	    enc = xxtea.xxbtea(data,2,"AABBCCDDEE0123456789AABBCCDDEEFF")
	    self.send(enc, "outbox")

class Decryptor(Axon.Component.component):
   def __init__(self,key):
      super(Decryptor,self).__init__()
      self.key = key
   
   def main(self):
      while 1:
         self.pause()
	 yield 1
	 while self.dataReady("inbox"):
	    data = self.recv("inbox")
	    print "in decrypt"
	    dec = xxtea.xxbtea(data,-2,"AABBCCDDEE0123456789AABBCCDDEEFF")
	    print "decrypted data ",dec
	    self.send(dec, "outbox")
	    
class echoer(Axon.Component.component):
    def main(self):
        count = 0
        while 1:
            self.pause()
            yield 1
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                print "echoer #",self.id,":", data, "count:", count
                count = count +1

# create a back plane by name Random talk
Backplane("RandomTalk").activate()

# create a reader and pipeline it to publish object
pipeline(
       MyReader(),
       Encryptor("12345678901234567890123456789012"),
       publishTo("RandomTalk"),
).activate()

#pipeline the subscribe object to the echoer
#note the connection publisher and subscriber is via BACKPLANE:)
pipeline(
        subscribeTo("RandomTalk"),
        Decryptor("12345678901234567890123456789012"),
	echoer(),
).run()
            
