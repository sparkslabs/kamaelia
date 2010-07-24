#!/usr/bin/env python2.3
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

