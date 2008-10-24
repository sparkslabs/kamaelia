#!/usr/bin/env python2.3
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

from Component import component
import idGen

class AdaptiveCommsComponent(component):
   #
   # Public Methods
   #
   def __init__(self):
      super(AdaptiveCommsComponent,self).__init__()
      self._resourceStore = {}
      self._resourceLookup = {}

   def trackResource(self, resource, inbox):
      "Tracks a _single_ resource associated with the inbox"
      self.inboxes[inbox] # Force failure if the inbox does not exist
      self._resourceLookup[inbox] = resource

   def retrieveTrackedResource(self, inbox):
      "Retrieves a single resource associated with the inbox"
      return self._resourceLookup[inbox]

   def trackResourceInformation(self, resource, inboxes, outboxes, information):
      "Provides a lookup service associating inboxes/outboxes & user information with a resource. Uses GIGO principle."
      [ self.inboxes[x] for x in inboxes] # Force an assertion if any inbox does not exist
      [ self.outboxes[x] for x in outboxes] # Force an assertion if any inbox does not exist
      self._resourceStore[resource] = (inboxes, outboxes, information)


   def ceaseTrackingResource(self, resource):
      "Stop tracking a resource and release references to it"
      del self._resourceStore[resource]

   def retrieveTrackedResourceInformation(self, resource):
      "retrieveTrackedResourceInformation(self, resource) -> informationBundle     ( {inboxes, outboxes,otherdata} ) (Uses GIGO principle.)"
      return self._resourceStore[resource]

   def addInbox(self,*args):
      "Adds a custom inbox with the name requested - or the closest name possible. (appends an integer) Returns the name of the inbox added."
      name = self._newInboxName(*args)
      self.inboxes[name]=[]
      return name

   def deleteInbox(self,name):
      "Deletes the named inbox"
      del self.inboxes[name]

   def addOutbox(self,*args):
      "Adds a custom outbox with the name requested - or the closest name possible. (appends an integer) Returns the name of the outbox added."
      name = self._newOutboxName(*args)
      self.outboxes[name]=[]
      return name

   def deleteOutbox(self,name):
      "Deletes the named outbox"
      del self.outboxes[name]
   #
   # Private Methods
   #
   def _newInboxName(self, name="inbox"):
      "Allocates a new inbox name based on the name provided. If this name is available it will be returned unchanged. Otherwise the name will be returned with a number appended"
      while name in self.inboxes:
          name =name+str(idGen.idGen().next())
      return name
   #
   def _newOutboxName(self, name="outbox"):
      "Allocates a new outbox name based on the name provided. If this name is available it will be returned unchanged. Otherwise the name will be returned with a number appended"
      while name in self.outboxes:
         name =name+str(idGen.idGen().next())
      return name

if __name__=="__main__":
   print "Tests are separated into test/test_AdaptiveCommsComponent.py"

