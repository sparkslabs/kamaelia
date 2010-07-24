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
"""Axon Component Framework.
Co-ordinating Assistant Tracker

The co-ordinating assistant tracker is designed to allow components to
register services and statistics they wish to make public to the rest of the
system. Components can also query the co-ordinating assistant tracker to
create linkages to specific services, and for specific global statistics.

Microprocesses can also use the co-ordinating assistant tracker to log/retrieve
statistics/information. Co-ordinating assistant trackers are designed to work in
a singleton manner accessible via a local or class interface.This singleton nature
of the co-ordinatin assistant tracker is not enforced.
"""
from __future__ import generators
from idGen import strId
#from Microprocess import microprocess
from AxonExceptions import BadParentTracker, ServiceAlreadyExists, BadComponent, BadInbox, MultipleServiceDeletion, NamespaceClash, AccessToUndeclaredTrackedVariable


#### class coordinatingassistanttracker(microprocess):
class coordinatingassistanttracker(object):
   basecat = None
   def getcat(cls):
      if not cls.basecat:
         cls.basecat = cls()
      return cls.basecat
   getcat = classmethod(getcat)

   def __init__(self,parent=None):
      name = strId(self)
      if self.basecat is None:
         self.__class__.basecat = self
#      super(coordinatingassistanttracker,self).__init__(name)
      self._informationLogged = dict()
      self._servicesRegistered = dict()
      if parent:
         if isinstance(parent, coordinatingassistanttracker):
            self._parent = parent
         else:
            raise BadParentTracker
      else:
         self._parent = None

   def informationItemsLogged(self):
      return self._informationLogged.keys()

   def servicesRegistered(self):
      """"Returns list of names of registered services"""
      return self._servicesRegistered.keys()

   def registerService(self, service, thecomponent, inbox):
      "t.registerService('service',component,inbox) - Registers that a component is willing to offer a service over a specific inbox"
      try:
         self._servicesRegistered[service] # We only add things if it doesn't exist
         raise ServiceAlreadyExists
      except KeyError:
         try:
            thecomponent.inboxes[inbox]
            self._servicesRegistered[service] = (thecomponent, inbox)
         except AttributeError:
            raise BadComponent(thecomponent)
         except KeyError:
            raise BadInbox(thecomponent, inbox)

   def deRegisterService(self, service):
      """Services are run by components - these by definition die and need to be
      de-registered"""
      try:
         del self._servicesRegistered[service]
      except KeyError:
         raise MultipleServiceDeletion

   def retrieveService(self,name):
      service = self._servicesRegistered[name]
      return service
#      try:
#         return self._informationLogged[name]
#      except KeyError:
#         raise AccessToUndeclaredTrackedVariable(name)

   def trackValue(self, name, value):
      """Once we start tracking a value, we have it's value forever (for now). Adding
      the same named value more than once causes a NamespaceClash to capture
      problems between interacting components"""
      try:
         self._informationLogged[name]
         raise NamespaceClash
      except KeyError:
         self._informationLogged[name]=value

   def updateValue(self,name, value):
      try:
         self._informationLogged[name] # Forces failure if not being tracked
         self._informationLogged[name]=value
      except KeyError:
         raise AccessToUndeclaredTrackedVariable(name,value)

   def retrieveValue(self,name):
      try:
         return self._informationLogged[name]
      except KeyError:
         raise AccessToUndeclaredTrackedVariable(name)

   def main(self):
      while 1:
         yield 1

if __name__ == '__main__':
   print "This code currently has no test code"
