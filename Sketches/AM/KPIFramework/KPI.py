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
import md5
import btree


class MyDataSource(Axon.Component.component):
   def main(self):
       index = 0
       while 1:
           data = str(index) + "-helloknr"
           self.send(data, "outbox")
           index = index + 1
           yield 1           


class KPIDB(object):
    
    def __init__(self, dbfile):
      super(KPIDB,self).__init__()
      self.dbfile = dbfile
      self.rootKey = btree.getKey(dbfile, 1)
      info = btree.getInfo(self.dbfile)
      self.max_user_id = info.max_user_id
    
    def getKey(self, userid):
        return btree.getUserKey(self.dbfile, userid)

    def getRootKey(self):
        return self.rootKey

    def isValidUser(self, userid):
        if (userid >= self.max_user_id/2 or userid < self.max_user_id):
            return True
        return False

    def getCommonKeys(self, users):
        return btree.getCommonKeys(self.dbfile, users)
        

class KPIUser(object):
    def __init__(self, configfile):
      super(KPIUser,self).__init__()
      self.idkeymap = {}
      self.user_id = 0
      self.key_len = 0
      #load config file
      fconfig = open(configfile,'r')
      for line in fconfig.readlines():
          line = line.strip()
          if (not line.startswith('#')) and (line.count('=') == 1):
              list = line.split('=')
              if list[0] == 'user_id':
                  self.user_id = long(list[1])
              elif list[0].strip() == 'key_len':
                  self.key_len = long(list[1])
              else:
                  id = long(list[0])
                  self.idkeymap[id] =  list[1].strip()

      print self.user_id, self.key_len, self.idkeymap
      fconfig.close()


    def getID(self):
        return self.user_id

    def getUserKey(self):
        return self.idkeymap[self.user_id]

    def getRootKey(self):
        return self.idkeymap[1]

    def getKey(self, ID):
        return self.idkeymap[ID]
    

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
        temp = xtea.xtea_decrypt(self.kpiuser.getUserKey(), data)
        padding, challenge = struct.unpack('!2L',temp)
        response = challenge+1
        print "received challenge",challenge
        print "sending response", response
        data = xtea.xtea_encrypt(self.kpiuser.getUserKey(),
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
                    index = len("KEY")
                    #get the ID
                    padding,ID = struct.unpack("!2L", data[index:index+8])
                    print "****ID****", ID
                    key = ""
                    try:
                        key = self.kpiuser.getKey(ID)
                    except KeyError:
                        pass #the key is not for me

                    if key != "":
                        enckey = data[index+8:len(data)]
                        part1 = xtea.xtea_decrypt(key, enckey[:8])
                        part2 = xtea.xtea_decrypt(key, enckey[8:16])
                        sessionkey = part1 + part2
                        print "decoded key", sessionkey
                        self.send(sessionkey, "notifykey")
                else:
                    data = data[len("DAT"):len(data)]
                    print "decoded data", data
                    self.send(data, "encout")
            yield 1


class Authenticator(Axon.Component.component):
    Inboxes = {"inbox" : "authentication and data packets"}
    Outboxes = {"outbox" : "authentication",
                "notifyuser" : "user notification"}

    def __init__(self, kpidb):
      super(Authenticator,self).__init__()
      self.kpidb = kpidb

    
    def main(self):
        kpidb = self.kpidb
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
    blocksize = 8 # to do generalize padding and breaking in to blocks
    while 1:
      yield 1
      if self.dataReady("keyevent"):
	    self.key = self.recv("keyevent")
	    print "key recieved at the encryptor",self.key
      if self.dataReady("inbox") and self.key != "\0":
            data = self.recv("inbox")
            enc = ''
            for i in range(0, len(data), blocksize):
                #do padding if less than block size
                #Pad with 0x80 followed by zero (null) bytes
                block = struct.pack('!8s', data[i:i+blocksize]+ chr(0x80))
                print "data block for encryption", block
                enc = enc + xtea.xtea_encrypt(self.key,block)
            self.send(enc, "outbox")

	    
class Decryptor(Axon.Component.component):
   Inboxes = {"inbox" : "encrypted data packets", "keyevent": "key for decryption"}
   Outboxes = {"outbox" : "decrypted data packets"}
   
   def __init__(self):
      super(Decryptor,self).__init__()
      self.key = "\0"

   def main(self):
      blocksize = 8 
      while 1:
         yield 1
	 if self.dataReady("keyevent"):
	    self.key = self.recv("keyevent")
            print "key recieved at the decryptor",self.key

         if self.dataReady("inbox") and self.key != "\0":
             data = self.recv("inbox")
             dec = ''
             print "decryptor data received ",data
             for i in range(0, len(data), blocksize):
                 #do unpadding if less than block size
                 #unpad any 0x80 followed by zero (null) bytes
                 block = xtea.xtea_decrypt(self.key,data[i:i+blocksize]).rstrip(chr(0x80)+chr(0x00))
                 print "decrypted block", block
                 dec = dec + block
             print "decrypted data ",dec
             self.send(dec, "outbox")
	    

# need to integrate with tree database
#todo need to send the session keys encrypted with common keys
class SessionKeyController(Axon.Component.component):
   Inboxes = {"userevent" : "new user event"}
   Outboxes = {"outbox" : "encrypted session key packets",
                "notifykey" : "notify key"}

   def __init__(self, kpidb):
       super(SessionKeyController,self).__init__()
       self.kpidb = kpidb


   def main(self):
       kpidb = self.kpidb
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
           idkeymap = kpidb.getCommonKeys(users)
           sessionKey = self.getSessionKey()
           print "idkeymap", idkeymap

           #encrypt the the session key with common keys
           for ID, key in idkeymap.iteritems():
               idstr = struct.pack("!2L", 0, ID)
               print "id,key", ID,len(key)
               cipher = xtea.xtea_encrypt(key, sessionKey[:8])
               cipher = cipher + xtea.xtea_encrypt(key, sessionKey[8:16])
               data = idstr + cipher
               self.send(data, "outbox")

           self.send(sessionKey, "notifykey")
           yield 1

   def getSessionKey(self):
       r1 = random.getrandbits(32)
       r2 = random.getrandbits(32)
       r3 = random.getrandbits(32)
       r4 = random.getrandbits(32)
       m = md5.new()
       m.update(struct.pack("!4L", r1, r3, r4, r2))
       return m.digest()        
                
                 

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
def client(config):
    authenticatee = Authenticatee(KPIUser(configfile=config))
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
    authenticator = Authenticator(KPIDB("mytree"))
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
        sc = SessionKeyController(KPIDB("mytree")),
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
    c=client("user1"),
    cc = clientconnector(),    
    linkages = {
        ("c","outbox") : ("cc","inbox"),
        ("cc","outbox") : ("c","inbox"),        
    }
).activate()


Graphline(
    c=client("user3"),
    cc = clientconnector(),    
    linkages = {
        ("c","outbox") : ("cc","inbox"),
        ("cc","outbox") : ("c","inbox"),        
    }
).run()
