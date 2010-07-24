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
	    \
print "ENCRYPTED DATA", repr(enc)
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
	    print "in decrypt", repr(data)
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

# create 19 clients...

if 1:
    for i in xrange(19):
        #pipeline the subscribe object to the echoer
        #note the connection publisher and subscriber is via BACKPLANE:)
        pipeline(
                subscribeTo("RandomTalk"),
                Decryptor("12345678901234567890123456789012"),
                echoer(),
        ).activate()

# And create a 20th, and set it running... :-)

#pipeline the subscribe object to the echoer
#note the connection publisher and subscriber is via BACKPLANE:)
pipeline(
        subscribeTo("RandomTalk"),
        Decryptor("12345678901234567890123456789012"),
	echoer(),
).run()
            
