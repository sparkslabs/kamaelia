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
"""\
===============================
Co-ordinating Assistant Tracker
===============================

The co-ordinating assistant tracker is designed to allow components to
register services and statistics they wish to make public to the rest of the
system. Components can also query the co-ordinating assistant tracker to
create linkages to specific services, and for specific global statistics.

* A co-ordinating assistant tracker is shared between several/all components
* Components can register an inbox as a service with a name
* Components can retrieve a service by its name



Accessing the Co-ordinating Assistant Tracker
---------------------------------------------

Co-ordinating assistant trackers are designed to work in a singleton manner;
accessible via a local or class interface (though this is not enforced).

The simplest way to obtain the global co-ordinating assistant tracker is via
the getcat() class (static) method::

    from Axon.CoordinatingAssistantTracker import coordinatingassistanttracker
    
    theCAT = coordinatingassistanttracker.getcat()

The first time this method is called, the co-ordinating assistant tracker is
created. Subsequent calls, wherever they are made from, return that same
instance.



Services
--------

Components can register a named inbox on a component as a named service. This
provides a way for a component to provide a service for other components - an
inbox that another component can look up and create a linkage to.

Registering a service is simple::

    theComponent = MyComponentProvidingServiceOnItsInbox()
    theComponent.activate()

    theCAT = coordinatingassistanttracker.getcat()
    theCAT.registerService("MY_SERVICE", theComponent, "inbox")

Another component can then retrieve the service::

    theCAT = coordinatingassistanttracker.getcat()
    (comp, inboxname) = theCAT.retrieveService("MY_SERVICE")

Because services are run by components - these by definition die and so also
need to be de-registered::

    theCAT = coordinatingassistanttracker.getcat()
    theCAT.deRegisterService("MY_SERVICE")



Tracking global statistics
--------------------------

Microprocesses can also use the co-ordinating assistant tracker to log/retrieve
statistics/information.

Use the trackValue() method to initially start tracking a value under a given
name::

    value = ...

    theCAT = coordinatingassistanttracker.getcat()
    theCAT.trackValue("MY_VALUE", value)

This can then be easily retrieved::

    theCAT = coordinatingassistanttracker.getcat()
    value= theCAT.retrieveValue("MY_VALUE")

Call the updateValue() method (not the trackValue() method) to update the value
being tracked::

    newvalue = ...

    theCAT = coordinatingassistanttracker.getcat()
    theCAT.updateValue("MY_VALUE", newvalue)



Hierarchy of co-ordinating assistant trackers
---------------------------------------------

Although at initialisation a parent co-ordinating assistant tracker can be
specified; this is not currently used.

"""

from idGen import strId
#from Microprocess import microprocess
from AxonExceptions import BadParentTracker
from AxonExceptions import ServiceAlreadyExists
from AxonExceptions import BadComponent
from AxonExceptions import BadInbox
from AxonExceptions import MultipleServiceDeletion
from AxonExceptions import NamespaceClash
from AxonExceptions import AccessToUndeclaredTrackedVariable


#### class coordinatingassistanttracker(microprocess):
class coordinatingassistanttracker(object):
   """\
   coordinatingassistanttracker([parent]) -> new coordinatingassistanttracker object.
   
   Co-ordinating assistant tracker object tracks values and
   (component,inboxname) services under names.
   
   Keyword arguments:
   
   - parent  -- Optional. None, or a parent coordinatingassistanttracker object.
   """
   
   basecat = None
   def getcat(cls):
      """\
      Class method that returns a singleton coordinating assistant tracker (CAT).

      Call this to get hold of the system's CAT.
      """
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

   def zap(self):
      self._informationLogged = dict()
      self._servicesRegistered = dict()


   def informationItemsLogged(self):
      """Returns list of names values are being tracked under."""
      return self._informationLogged.keys()

   def servicesRegistered(self):
      """Returns list of names of registered services"""
      return self._servicesRegistered.keys()

   def registerService(self, service, thecomponent, inbox):
      """\
      Register a named inbox on a component as willing to offer a service with
      the specified name.
      
      Keyword arguments:
      
      - service       -- the name for the service
      - thecomponent  -- the component offering the service
      - inbox         -- name of the inbox on the component
      
      Exceptions that may be raised:
       
      * Axon.AxonExceptions.ServiceAlreadyExists
      * Axon.AxonExceptions.BadComponent
      * Axon.AxonExceptions.BadInbox
      """
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
      """\
      Deregister a service that was previously registered.
      
      Raises Axon.AxonExceptions.MultipleServiceDeletion if the service is not/
      no longer registered.
      """
      try:
         del self._servicesRegistered[service]
      except KeyError:
         raise MultipleServiceDeletion

   def retrieveService(self,name):
      """\
      Retrieve the (component, inboxName) service with the specified name.
      """
      service = self._servicesRegistered[name]
      return service
#      try:
#         return self._informationLogged[name]
#      except KeyError:
#         raise AccessToUndeclaredTrackedVariable(name)

   def trackValue(self, name, value):
      """\
      Track (record) the specified value under the specified name.
      
      Once we start tracking a value, we have it's value forever (for now).
      Trying to track the same named value more than once causes an
      Axon.AxonExceptions.NamespaceClash exception. This is done to capture
      problems between interacting components
      """
      try:
         self._informationLogged[name]
         raise NamespaceClash
      except KeyError:
         self._informationLogged[name]=value

   def updateValue(self,name, value):
      """\
      Update the value being tracked under the specified name with the new
      value provided.
      
      Trying to update a value under a name that isn't yet being tracked results
      in an Axon.AxonExceptions.AccessToUndeclaredTrackedVariable exception
      being raised.
      """
      try:
         self._informationLogged[name] # Forces failure if not being tracked
         self._informationLogged[name]=value
      except KeyError:
         raise AccessToUndeclaredTrackedVariable(name,value)

   def retrieveValue(self,name):
      """\
      Retrieve the value tracked (recorded) under the specified name.
      
      Trying to retrieve a value under a name that isn't yet being tracked
      results in an Axon.AxonExceptions.AccessToUndeclaredTrackedVariable
      exception being raised.
      """
      try:
         return self._informationLogged[name]
      except KeyError:
         raise AccessToUndeclaredTrackedVariable(name)

   def main(self):
      # redundant ... unless this class is modified to be a microprocess
      while 1:
         yield 1

if __name__ == '__main__':
   print "This code currently has no test code"
