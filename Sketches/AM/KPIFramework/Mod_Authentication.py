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
import xxtea
from Kamaelia.Util.Graphline import *

# based on the needham-schroeder protocol.

class Authenticator(Axon.Component.component):
   Inboxes = {"inbox" : "data input",
              "control" : "control information"}
   Outboxes = {"outbox" : "data output",
               "control" : "success/failure of authntication is written here"}
   
   def __init__(self,key):
      super(Authenticator,self).__init__()
      self.key = key
      
   def main(self):
	rand = xxtea.getRandKey(8);
        print "rand is",rand
        enc = xxtea.xxbtea(rand,2,"AABBCCDDEE0123456789AABBCCDDEEFF")
        self.send(enc,"outbox")
        status = False 
         
	while not self.dataReady("inbox"):
           yield 1
	data = self.recv("inbox")

        if status == False:
		status = True
		dec = xxtea.xxbtea(rand,-2,"AABBCCDDEE0123456789AABBCCDDEEFF")
		print "authenticator recieved frm tee ",dec
		if enc == dec:
			self.send("authentication successful","control")
		else:
      		   self.send("authentication failed","control")
	else:
		self.send(data, "outbox")
   
class Authenticatee(Axon.Component.component):

   Inboxes = {"inbox" : "data input",
              "control" : "control information"}
   Outboxes = {"outbox" : "data output",
               "control" : "control information"}
   
   def __init__(self,key):
      super(Authenticatee,self).__init__()
      self.key = key

   def main(self):
       while not self.dataReady("inbox"):
         yield 1
       data = self.recv("inbox")
       dec = xxtea.xxbtea(data,-2,"AABBCCDDEE0123456789AABBCCDDEEFF")
       print "authenticatee recieved ",dec
	 #actually enc = dec+1
       enc = xxtea.xxbtea(dec,2,"AABBCCDDEE0123456789AABBCCDDEEFF")
       self.send(enc,"outbox")

class echoer(Axon.Component.component):
    def main(self):
         while not self.dataReady("inbox"):
            yield 1    
         data = self.recv("inbox")
         print "echoer ", data

Graphline(Sender = Authenticator("AABBCCDDEE0123456789AABBCCDDEEFF"), 
          Recipient = Authenticatee("AABBCCDDEE0123456789AABBCCDDEEFF"),
	  ech = echoer(),
          linkages = { ("Sender" ,"outbox") : ("Recipient","inbox"),
                       ("Recipient","outbox") : ("Sender","inbox"),
                       ("Sender","control") : ("ech","inbox"),
                     }
         ).run()
	 
