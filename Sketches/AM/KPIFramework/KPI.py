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
from Axon.Ipc import newComponent
from Kamaelia.Util.Splitter import PlugSplitter as Splitter
from Kamaelia.Util.Splitter import Plug
from Axon.AxonExceptions import ServiceAlreadyExists
from Axon.CoordinatingAssistantTracker import coordinatingassistanttracker as CAT
from Kamaelia.Util.passThrough import passThrough
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Backplane import *
from Kamaelia.Util.Graphline import *

from Kamaelia.File import ReadFileAdaptor
from Kamaelia.File.Reading import PromptedFileReader
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Util.RateFilter import ByteRate_RequestControl
from Kamaelia.SingleServer import SingleServer
from Kamaelia.Internet.TCPClient import TCPClient

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
	 while self.dataReady("inbox"):
	    data = self.recv("inbox")
	    print "encrypting data: ",data
	    enc = xxtea.xxbtea(data,2,"AABBCCDDEE0123456789AABBCCDDEEFF")
	    self.send(enc, "outbox")
         self.pause()
	 yield 1

class Decryptor(Axon.Component.component):
   def __init__(self,key):
      super(Decryptor,self).__init__()
      self.key = key
   
   def main(self):
      while 1:
	 while self.dataReady("inbox"):
	    data = self.recv("inbox")
	    dec = xxtea.xxbtea(data,-2,"AABBCCDDEE0123456789AABBCCDDEEFF")
	    print "decrypted data ",dec
	    self.send(dec, "outbox")
         self.pause()
	 yield 1
	    
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
   def __init__(self):
      super(ClientSimulator,self).__init__()

   def main(self):
      count = 0
      while count != 20:
          mesg = "Client Subscribed " + str(count)
	  print "mesg is ", mesg
	  self.send(mesg)
          count=count+1
	  yield 1
      

# create a back plane by name server talk
Backplane("ServerTalk").activate()

# the client events backplane will publish an event whenever the client joins/leaves the backplane.

Backplane("ClientEvents").activate()

def fixedString():
 # create a reader and pipeline it to publish object
 pipeline(
        MyReader(),
        Encryptor("12345678901234567890123456789012"),
        publishTo("ServerTalk"),
 ).activate()

 #pipeline the subscribe object to the echoer
 #note the connection publisher and subscriber is via BACKPLANE:)
 pipeline(
         subscribeTo("ServerTalk"),
         Decryptor("12345678901234567890123456789012"),
	 echoer(),
 ).run()

def fileRW():
 port = 1602
 #Read 8 bytes at a time from a file, encrypt it, and publish to the backplane.
 
 pipeline(
        ByteRate_RequestControl(rate=10000,chunksize=8), #The rate parameter might have to change for if it becomes across a network.
        PromptedFileReader("SelfishTriangle.jpg","bytes"),
        Encryptor("12345678901234567890123456789012"),
        #SingleServer(port=port),
        publishTo("ServerTalk")
 ).activate()

# Read 8 bytes from the subscriber, decrypt it and write it to the output file.
 pipeline(
        subscribeTo("ServerTalk"),
        #TCPClient("127.0.0.1",port),
        Decryptor("12345678901234567890123456789012"),
        SimpleFileWriter("SelfishTriangle-dec.jpg")
 ).run()


def multipleClients():
 #Read 8 bytes at a time from a file, encrypt it, and publish to the backplane.
 
 Graphline(
        brrc = ByteRate_RequestControl(rate=10000,chunksize=8), #The rate parameter might have to change for if it becomes across a network.
        pfr = PromptedFileReader("Chekov.txt","bytes"),
        snd = Sender(),
        sub = subscribeTo("ClientEvents"), # the sender subscribes to the graphline and comes to know of key change events, like client join/leave
	enc = Encryptor("12345678901234567890123456789012"),
	pub = publishTo("ServerTalk"),
	linkages = { ("brrc","outbox") : ("pfr","inbox"),
	             ("pfr","outbox") : ("snd","databox"),
		     ("sub","outbox") : ("snd","keybox"),
		     ("snd","outbox") : ("pub","inbox"),
		     #("enc","outbox") : ("pub","inbox"),
		   }
 ).activate()

# the recipient publishes to a backplane whenever clients join/leave

 #Graphline(
  #     cs = ClientSimulator(),
   #    pub = publishTo("ClientEvents"),
    #   linkages = { ("cs","outbox") : ("pub","inbox") 
     #             }
 #).activate()
 
# Read 8 bytes from the subscriber, decrypt it and write it to the output file.
 Graphline(
        pub = publishTo("ClientEvents"),
        sub = subscribeTo("ServerTalk"),
        #dec = Decryptor("12345678901234567890123456789012"),
        sf = SimpleFileWriter("Chekov-1.txt"),
	linkages = { ("sub","outbox") : ("sf","inbox"),
	             #("dec","outbox") : ("sf","inbox"),
		   }
 ).activate()


# Read 8 bytes from the subscriber, decrypt it and write it to the output file.
 Graphline(
        pub = publishTo("ClientEvents"),
        sub = subscribeTo("ServerTalk"),
        #dec = Decryptor("12345678901234567890123456789012"),
        sf = SimpleFileWriter("Chekov-2.txt"),
	linkages = { ("sub","outbox") : ("sf","inbox"),
	             #("dec","outbox") : ("sf","inbox"),
		   }
 ).activate()
# Read 8 bytes from the subscriber, decrypt it and write it to the output file.
 Graphline(
        pub = publishTo("ClientEvents"),
        sub = subscribeTo("ServerTalk"),
        #dec = Decryptor("12345678901234567890123456789012"),
        sf = SimpleFileWriter("Chekov-3.txt"),
	linkages = { ("sub","outbox") : ("sf","inbox"),
	             #("dec","outbox") : ("sf","inbox"),
		   }
 ).run()

def clientSubscribe():
 #Read 8 bytes at a time from a file, encrypt it, and publish to the backplane.
 
 Graphline(
        brrc = ByteRate_RequestControl(rate=10000,chunksize=8), #The rate parameter might have to change for if it becomes across a network.
        pfr = PromptedFileReader("Chekov.txt","bytes"),
        snd = Sender(),
        sub = subscribeTo("ClientEvents"), # the sender subscribes to the graphline and comes to know of key change events, like client join/leave
	enc = Encryptor("12345678901234567890123456789012"),
	pub = publishTo("ServerTalk"),
	linkages = { ("brrc","outbox") : ("pfr","inbox"),
	             ("pfr","outbox") : ("snd","databox"),
		     ("sub","outbox") : ("snd","keybox"),
		     ("snd","outbox") : ("enc","inbox"),
		     ("enc","outbox") : ("pub","inbox"),
		   }
 ).activate()

# the recipient publishes to a backplane whenever clients join/leave

 #Graphline(
  #     cs = ClientSimulator(),
   #    pub = publishTo("ClientEvents"),
    #   linkages = { ("cs","outbox") : ("pub","inbox") 
     #             }
 #).activate()
 
# Read 8 bytes from the subscriber, decrypt it and write it to the output file.
 Graphline(
        pub = publishTo("ClientEvents"),
        sub = subscribeTo("ServerTalk"),
        dec = Decryptor("12345678901234567890123456789012"),
        sf = SimpleFileWriter("Chekov-dec-1.txt"),
	linkages = { ("sub","outbox") : ("dec","inbox"),
	             ("dec","outbox") : ("sf","inbox"),
		   }
 ).activate()


# Read 8 bytes from the subscriber, decrypt it and write it to the output file.
 Graphline(
        pub = publishTo("ClientEvents"),
        sub = subscribeTo("ServerTalk"),
        dec = Decryptor("12345678901234567890123456789012"),
        sf = SimpleFileWriter("Chekov-dec-2.txt"),
	linkages = { ("sub","outbox") : ("dec","inbox"),
	             ("dec","outbox") : ("sf","inbox"),
		   }
 ).activate()
# Read 8 bytes from the subscriber, decrypt it and write it to the output file.
 Graphline(
        pub = publishTo("ClientEvents"),
        sub = subscribeTo("ServerTalk"),
        dec = Decryptor("12345678901234567890123456789012"),
        sf = SimpleFileWriter("Chekov-dec-3.txt"),
	linkages = { ("sub","outbox") : ("dec","inbox"),
	             ("dec","outbox") : ("sf","inbox"),
		   }
 ).run()

#fixedString()
#fileRW()
#print " *********************RUNNING UNENCRYPTED  MULTIPLE CLIENTS **************************"
#multipleClients()

print " *********************RUNNING ENCRYPTED  MULTIPLE CLIENTS **************************"
clientSubscribe()
