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
#from Axon.Ipc import newComponent
#from Kamaelia.Util.Splitter import PlugSplitter as Splitter
#from Kamaelia.Util.Splitter import Plug
#from Axon.AxonExceptions import ServiceAlreadyExists
#from Axon.CoordinatingAssistantTracker import coordinatingassistanttracker as CAT
#from Kamaelia.Util.passThrough import passThrough
#from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Backplane import *
from Kamaelia.Util.Graphline import *
from Kamaelia.File.Reading import RateControlledFileReader
#from Kamaelia.File import ReadFileAdaptor
#from Kamaelia.File.Reading import PromptedFileReader
from Kamaelia.File.Writing import SimpleFileWriter
#from Kamaelia.Util.RateFilter import ByteRate_RequestControl
#from Kamaelia.SingleServer import SingleServer
#from Kamaelia.Internet.TCPClient import TCPClient

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
            self.pause()
            yield 1
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                print  data, "count:", count
                count = count +1

class Sender(Axon.Component.component):
   Inboxes = {"databox" : "data input",
              "keybox"  :  "key update messages" }
   def __init__(self):
      super(Sender,self).__init__()
   def main(self):
      while 1:
         self.pause()
	 yield 1
	 while self.dataReady("keybox"):
	    #there is a keychange message.
	    data = self.recv("keybox");
	    print "event triggered. change key ",data
	    yield 1
	 while self.dataReady("databox"):
	       data = self.recv("databox")
	       self.send(data)
   

class ClientSimulator(Axon.Component.component):
   def __init__(self,id):
      super(ClientSimulator,self).__init__()
      self.id = id;
   def main(self):
         count = 0
         mesg = "Client Subscribed " + self.id
         print "mesg is ", mesg
         self.send(mesg)
         count=count+1
         yield 1
      
# create a back plane by name server talk
Backplane("ServerTalk").activate()

# the client events backplane will publish an event whenever the client joins/leaves the backplane.
Backplane("ClientEvents").activate()

def clientSubscribe():
 #Read 8 bytes at a time from a file, encrypt it, and publish to the backplane.
 
 Graphline(
        rcfr = RateControlledFileReader("Chekov.txt",readmode="bytes",rate=100000,chunksize=8),
        snd = Sender(),
        sub = subscribeTo("ClientEvents"), # the sender subscribes to the graphline and comes to know of key change events, like client join/leave
	enc = Encryptor("12345678901234567890123456789012"),
	pub = publishTo("ServerTalk"),
	linkages = {
	             ("rcfr","outbox") : ("snd","databox"),
		     ("sub","outbox") : ("snd","keybox"),
		     ("snd","outbox") : ("enc","inbox"),
		     ("enc","outbox") : ("pub","inbox"),
		   }
 ).activate()

# the recipient publishes to a backplane whenever clients join/leave

# Read 8 bytes from the subscriber, decrypt it and write it to the output file.
 Graphline(
        cs = ClientSimulator("100"),
        pub = publishTo("ClientEvents"),
        sub = subscribeTo("ServerTalk"),
        dec = Decryptor("12345678901234567890123456789012"),
        sf = SimpleFileWriter("Chekov-dec-1.txt"),
	linkages = { ("cs","outbox") : ("pub","inbox"),
	             ("sub","outbox") : ("dec","inbox"),
	             ("dec","outbox") : ("sf","inbox"),
		   }
 ).activate()

# Read 8 bytes from the subscriber, decrypt it and write it to the output file.
 Graphline(
        cs = ClientSimulator("101"),
        pub = publishTo("ClientEvents"),
        sub = subscribeTo("ServerTalk"),
        dec = Decryptor("12345678901234567890123456789012"),
        sf = SimpleFileWriter("Chekov-dec-2.txt"),
	linkages = { ("cs","outbox") : ("pub","inbox"),
	             ("sub","outbox") : ("dec","inbox"),
	             ("dec","outbox") : ("sf","inbox"),
		   }
 ).run()



#fixedString()
#fileRW()
#print " *********************RUNNING UNENCRYPTED  MULTIPLE CLIENTS **************************"
#multipleClients()

print " *********************RUNNING ENCRYPTED  MULTIPLE CLIENTS **************************"
clientSubscribe()
