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


#import xxtea
import xtea

class Encryptor(Axon.Component.component):
   Inboxes = {"inbox" : "data to be encrypted",
              "control" : "key updates"}
   def __init__(self):
      super(Encryptor,self).__init__()
      self.key = "\0"

   def main(self):
    keyReady = 'False'
    while 1:
      yield 1
      if self.dataReady("control"):
            keyReady = 'True'
	    self.key = self.recv("control")
	    print "key recieved at the encryptor",self.key
      while self.dataReady("inbox") and keyReady == 'True':
            data = self.recv("inbox")
	    if len(data) < 8:
	       data = '88888888'#FIXME: pad with null's the last bytes that are < 8
            #enc = xxtea.xxbtea(data,2,self.key)
	    if self.key != "\0":
               enc = xtea.xtea_encrypt(self.key,data)
	       print "encrypted text ",enc
	       self.send(enc, "outbox")
               yield 1
	    else:
              print "key is null. cannot encrypt"#TODO: this might be an exception

	    
class Decryptor(Axon.Component.component):
   Inboxes = {"inbox" : "data to be decrypted",
              "control" : "key updates"}

   def __init__(self):
      super(Decryptor,self).__init__()
      self.key = "\0"

   def main(self):
      keyRecieved = 'False'
      while 1:
         yield 1

	 if self.dataReady("control"):
	    self.key = self.recv("control")
            keyRecieved = 'True'
            print "key recieved at the decryptor",self.key
            yield 1

         while self.dataReady("inbox") and keyRecieved == 'True': 
          data = self.recv("inbox")
          print "decryptor recieved ",data
          if self.key != "\0":
            #dec = xxtea.xxbtea(data,-2,self.key)
            dec = xtea.xtea_decrypt(self.key,data)
	    print "decrypted text ",dec
	    self.send(dec, "outbox")
            yield 1
          else:
             print "key is null. cannot decrypt" #TODO:exception ?
	    
class KeyGen(Axon.Component.component):
   def main(self):
        self.send('1234567890123456',"outbox") 
        yield 1
         
class Echoer(Axon.Component.component):
   def main(self):
      while 1:
         while self.dataReady("inbox"):
            data = self.recv("inbox")
            print"Echoer", data  
         yield 1
    
class DataTransmitter(Axon.Component.component): # packetises and sends the encrypted key/data
   Inboxes = { "inbox" : "encrypted data to transmit to the sender",
               "keyin" : "session key encrypted with shared keys"
	     }
	     
   def main(self):
      dataHeader = 'DAT'
      keyHeader = 'KEY'
      while 1:
         yield 1
         
	 while self.dataReady("keyin"):
	   data = self.recv("keyin")
	   # the client should be able to distinguish between data and key
           packet = dataHeader
	   packet.append(data)
	   #self.send(data)
           yield 1
	   
         while self.dataReady("inbox"):
	    data = self.recv("inbox")
	    print "data transmitter",data
            self.send(data)
            yield 1

class SessionKeyController(Axon.Component.component):

   Inboxes = { "control" : "recieve new user-id notifications" } 
   Outboxes = { "signal" : "sending new session key to the encryptor",
                "outbox" : "encrypted new session key to transmitter"
              }
   def main(self):
      while 1:
         #self.pause()
	 yield 1
	 while self.dataReady("control"):
	    data = self.recv("control")
	    # generate a new session key.
            sessionKey = '1234567890123456'
	    print "sending session key",sessionKey
            self.send(sessionKey, "signal")
            self.send(sessionKey, "outbox")

   def getSessionKey():
      return '1234567890123456'

# Both Authenticator and Authenticatee for the time being act as pass thorugh 

class Authenticator(Axon.Component.component):
   Inboxes = {"inbox" : "pass through",
              "keyin" : "authentication key" }

   Outboxes = {"signal" : "publishing successful authentication to the keymanagement",
               "outbox" : "pass through encrypted content" }

   def main(self):
    while 1:
      yield 1
      while self.dataReady("keyin"):
         data = self.recv("keyin")
         self.send(data,"signal")
         yield 1
      while self.dataReady("inbox"):
	 data = self.recv("inbox")
         print "Authenticator sending ",data
	 self.send(data,"outbox")
         yield 1


class Authenticatee(Axon.Component.component):
   Inboxes = {"inbox" : "encrypted data pass through" }

   Outboxes = {"outbox" : "encrypted data pass through",
               "keyout" : "authentication information"}

   def main(self):
     yield 1
     self.send("1234567890123456","keyout")
     while 1:
       yield 1
       
       while self.dataReady("inbox"):
          data = self.recv("inbox")
          print "authenticatee sending ",data
          self.send(data,"outbox")
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

class MyReader(Axon.Component.component):
    def main(self):
        while 1:
 #           line = raw_input(self.prompt)
            line = "hello678"
            self.send(line, "outbox")
            yield 1


# create a back plane by name server talk
Backplane("DataManagement").activate()
Backplane("KeyManagement").activate()

def EncDec():
    # Server side code
    Graphline(
        rcfr = RateControlledFileReader("Chekov.txt",readmode="bytes",rate=100000,chunksize=8),
        mr = MyReader(),
        kg = KeyGen(),
        enc = Encryptor(),
        dtx = DataTransmitter(),
        pub = publishTo("DataManagement"),
        sub = subscribeTo("KeyManagement"),
        ses = SessionKeyController(),

        linkages = {
                     ("rcfr","outbox") : ("enc","inbox"),
                     ("enc","outbox") : ("dtx","inbox"),
                     ("dtx","outbox") : ("pub","inbox"),
                     ("sub","outbox") : ("ses","control"),
                     ("ses","signal") : ("enc","control"),
                     #("dec","outbox") : ("ech","inbox"),
                     #("kg","outbox") : ("enc","control"),
                   }
    ).activate()


   # Client side code
    Graphline(
       authenticator = Authenticator(),
       notifier = publishTo("KeyManagement"),
       authenticatee = Authenticatee(),
       dec = Decryptor(),
       sub = subscribeTo("DataManagement"),
       ech = Echoer(),
       sfw = SimpleFileWriter("Khochev-1.txt"),
       kg1 = KeyGen(),

       linkages = {
                   ("sub","outbox") : ("authenticator","inbox"),
                   ("authenticator","signal") : ("notifier","inbox"),
                   ("authenticator","outbox") : ("authenticatee","inbox"),
                   ("authenticatee","keyout") : ("authenticator","keyin"),
                   ("authenticatee","outbox") : ("dec","inbox"),
                   ("dec","outbox") : ("sfw","inbox"),
                   ("kg1","outbox") : ("dec","control"),
                  }
      ).activate()


   # Client side code
    Graphline(
       authenticator = Authenticator(),
       notifier = publishTo("KeyManagement"),
       authenticatee = Authenticatee(),
       dec = Decryptor(),
       sub = subscribeTo("DataManagement"),
       ech = Echoer(),
       sfw = SimpleFileWriter("Khochev-2.txt"),
       kg1 = KeyGen(),

       linkages = {
                   ("sub","outbox") : ("authenticator","inbox"),
                   ("authenticator","signal") : ("notifier","inbox"),
                   ("authenticator","outbox") : ("authenticatee","inbox"),
                   ("authenticatee","keyout") : ("authenticator","keyin"),
                   ("authenticatee","outbox") : ("dec","inbox"),
                   ("dec","outbox") : ("sfw","inbox"),
                   ("kg1","outbox") : ("dec","control"),
                  }
      ).run()


EncDec()
