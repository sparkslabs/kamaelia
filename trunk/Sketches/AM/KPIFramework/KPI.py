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
from Kamaelia.Util.Backplane import *
from Kamaelia.Util.Graphline import *
import xtea
import random
import struct


class MyDataSource(Axon.Component.component):
   def main(self):
       index = 0
       while 1:
           data = str(index) + "helloknr"
           self.send(data[:8], "outbox")
           index = index + 1
           yield 1           

#todo
#this is just a dummy tree interface
class KPIDB(object):
    def __init__(self):
      super(KPIDB,self).__init__()
      self.tree = ['0000000000000000', '1111111111111111', 'AAAAAAAAAAAAAAAA',
                   'BBBBBBBBBBBBBBBB', 'CCCCCCCCCCCCCCCC', 'DDDDDDDDDDDDDDDD',
                   'EEEEEEEEEEEEEEEE', 'FFFFFFFFFFFFFFFF']
    

    def getKey(self, userid):
        return self.tree[userid]

    def getRootKey(self):
        return self.tree[1]

    def isValidUser(self, userid):
        if userid >= len(self.tree)/2 or userid < len(self.tree):
            return True
        return False

    def getCommonKeys(self, users):
        if (len(users) >= 2):
            return self.tree[3]
        else:
            return self.tree[users[0]]

#todo
#this is just a user interface
class KPIUser(object):
    def __init__(self, config="", userid=0):
      super(KPIUser,self).__init__()
      self.config = config
      self.userid = userid
      self.tree = ['0000000000000000', '1111111111111111', 'AAAAAAAAAAAAAAAA',
                   'BBBBBBBBBBBBBBBB', 'CCCCCCCCCCCCCCCC', 'DDDDDDDDDDDDDDDD',
                   'EEEEEEEEEEEEEEEE', 'FFFFFFFFFFFFFFFF']

    def getID(self):
        return self.userid

    def getKey(self):
        return self.tree[self.userid]

    def getRootKey(self):
        return self.tree[1]
    


    

class Authenticatee(Axon.Component.component):
    Inboxes = {"inbox" : "authentication and data packets"}
    Outboxes = {"outbox" : "authentication",
                "encout" : "encrypted data packets",
                "notifykey" : "notify key"}

    def __init__(self, kpiuser):
      super(Authenticatee,self).__init__()
      self.kpiuser = kpiuser
   
    
    def main(self):
        userid = self.kpiuser.getID()
        data = xtea.xtea_encrypt(self.kpiuser.getRootKey(),
                                 struct.pack('!2L',0, userid))
        print "encrypting user id with root key", self.kpiuser.getID(), self.kpiuser.getRootKey()
        self.send(data, "outbox")
        yield 1

        while not self.dataReady("inbox"):
            yield 1
        data = self.recv("inbox")
        temp = xtea.xtea_decrypt(self.kpiuser.getKey(), data)
        padding, challenge = struct.unpack('!2L',temp)
        response = challenge+1
        print "received challenge",challenge
        print "sending response", response
        data = xtea.xtea_encrypt(self.kpiuser.getKey(),
                                 struct.pack('!2L',0, response))
        
        
        self.send(data, "outbox")
        yield 1
        while not self.dataReady("inbox"):
            yield 1
        data = self.recv("inbox")
        if data == "SUCCESS":
            print "authentication success"
        else:
            print "authenication failure"
            return

        #decode data
        while 1:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                print "decoder", data
                if data.startswith("KEY"):
                    data = data[len("KEY"):len(data)]
                    print "decoded key", data
                    self.send(data, "notifykey")
                else:
                    data = data[len("DAT"):len(data)]
                    print "decoded data", data
                    self.send(data, "encout")
            yield 1


class Authenticator(Axon.Component.component):
    Inboxes = {"inbox" : "authentication and data packets"}
    Outboxes = {"outbox" : "authentication",
                "notifyuser" : "user notification"}
    
    def main(self):
        kpidb = KPIDB()
        while not self.dataReady("inbox"):
            yield 1
        data = self.recv("inbox")
        padding,userid = struct.unpack('!2L',
                xtea.xtea_decrypt(kpidb.getRootKey(),data))
        print "Authenticator received userid:", userid
        if kpidb.isValidUser(userid) == False:
            print "Invalid UserID" # todo shutdown
            return

        challenge = random.getrandbits(32)
        temp = struct.pack('!2L',0, challenge)
        data = xtea.xtea_encrypt(kpidb.getKey(userid), temp)
        print data, challenge, kpidb.getKey(userid)
        self.send(data, "outbox")
        yield 1
        while not self.dataReady("inbox"):
            yield 1
        data = self.recv("inbox")
        temp = xtea.xtea_decrypt(kpidb.getKey(userid),data)
        padding, response = struct.unpack('!2L', temp)
	print data, response
	if response == challenge + 1:
            self.send("SUCCESS", "outbox")
            yield 1
        else:
            print "authenication failure"
            return # shutdown

        #new user added 
        self.send(userid, "notifyuser")

        #subscribe to data Management back plane
        subscriber = subscribeTo("DataManagement")
        self.link( (subscriber, "outbox"), (self, "outbox"), passthrough=2)
        subscriber.activate()
        yield 1

        while 1:
            yield 1
        
        

class Encryptor(Axon.Component.component):
   Inboxes = {"inbox" : "data packets", "keyevent": "key for encryption"}
   Outboxes = {"outbox" : "encrypted data packets"}    
   def __init__(self):
      super(Encryptor,self).__init__()
      self.key = "\0"

   def main(self):
    while 1:
      yield 1
      if self.dataReady("keyevent"):
	    self.key = self.recv("keyevent")
	    print "key recieved at the encryptor",self.key
      if self.dataReady("inbox"):
            data = self.recv("inbox")
	    if len(data) < 8:
	       data = '88888888'#FIXME: pad with null's the last bytes that are < 8
	    if self.key != "\0":
               print "data to be encrypted", data
               enc = xtea.xtea_encrypt(self.key,data)
	       self.send(enc, "outbox")

	    
class Decryptor(Axon.Component.component):
   Inboxes = {"inbox" : "encrypted data packets", "keyevent": "key for decryption"}
   Outboxes = {"outbox" : "decrypted data packets"}
   
   def __init__(self):
      super(Decryptor,self).__init__()
      self.key = "\0"

   def main(self):
      while 1:
         yield 1
	 if self.dataReady("keyevent"):
	    self.key = self.recv("keyevent")
            print "key recieved at the decryptor",self.key

         if self.dataReady("inbox"):
            data = self.recv("inbox")
            print "decryptor data received ",data
            if self.key != "\0":
                dec = xtea.xtea_decrypt(self.key,data)
                print "decrypted data ",dec
                self.send(dec, "outbox")
	    

# need to integrate with tree database
#todo need to send the session keys encrypted with common keys
class SessionKeyController(Axon.Component.component):
   Inboxes = {"userevent" : "new user event"}
   Outboxes = {"outbox" : "encrypted session key packets",
                "notifykey" : "notify key"}

   def main(self):
       kpidb = KPIDB()
       users = []
       while 1:
           while not self.dataReady("userevent"):
               yield 1
           print "SC sending a key"
           userid = self.recv("userevent")
           #to avoid duplicate entries
           try:
               users.index(userid)
           except ValueError:
               users.append(userid)
               users.sort()
           #todo to send in a format
           key = kpidb.getCommonKeys(users)
           self.send(key, "notifykey")
           self.send(key, "outbox")
           yield 1
                
                 

class DataTx(Axon.Component.component):
   Inboxes = {"inbox" : "data to be encrypted",
              "keyIn" : "key updates"}

   def __init__(self):
      super(DataTx,self).__init__()

   def main(self):
       while 1:
           while self.dataReady("keyIn"):
               data = "KEY" + self.recv("keyIn")
               print "DataTx", data
               self.send(data, "outbox")
           yield 1
           if self.dataReady("inbox"):
               data = "DAT" + self.recv("inbox")
               print "DataTx", data               
               self.send(data, "outbox")
           yield 1
          


#client side
def client(ID):
    authenticatee = Authenticatee(KPIUser(userid=ID))
    Graphline(
        authee = authenticatee,
        dec = Decryptor(),
        linkages = {
            ("authee","encout") : ("dec","inbox"),
            ("authee","notifykey") : ("dec","keyevent"),
        }
    ).activate()
    return authenticatee
    

#server side client connector
def clientconnector():
    authenticator = Authenticator()
    Graphline(
        author = authenticator,
        notifier = publishTo("KeyManagement"),
        linkages = {
            ("author","notifyuser") : ("notifier","inbox"),
        }
    ).activate()
    return authenticator    


#KPI Session management and streaming backend
def KPIServer(datasource):
    Backplane("DataManagement").activate()
    Backplane("KeyManagement").activate()
    Graphline(
        ds = datasource, 
        sc = SessionKeyController(),
        keyRx = subscribeTo("KeyManagement"),
        enc = Encryptor(),
        sender = publishTo("DataManagement"),
        pz = DataTx(),
        linkages = {
            ("ds","outbox") : ("enc","inbox"),
            ("keyRx","outbox") : ("sc","userevent"),        
            ("sc","notifykey") : ("enc","keyevent"),
            ("sc","outbox") : ("pz","keyIn"),   
            ("enc","outbox") : ("pz","inbox"),
            ("pz","outbox") : ("sender","inbox"),
        }
    ).activate()


#client simulation
KPIServer(datasource=MyDataSource())
Graphline(
    c=client(ID=6),
    cc = clientconnector(),    
    linkages = {
        ("c","outbox") : ("cc","inbox"),
        ("cc","outbox") : ("c","inbox"),        
    }
).activate()


Graphline(
    c=client(ID=7),
    cc = clientconnector(),    
    linkages = {
        ("c","outbox") : ("cc","inbox"),
        ("cc","outbox") : ("c","inbox"),        
    }
).run()
