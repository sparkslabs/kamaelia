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
=====================================================================
"Adaptive Comms Components" - can add and remove inboxes and outboxes
=====================================================================

An AdaptiveCommsComponent is just like an ordinary component but with the
ability to create and destroy extra inboxes and outboxes whilst it is running.

* An AdaptiveCommsComponent is based on an Axon.Component.component

There are other variants on the basic component:
    
* Axon.ThreadedComponent.threadedcomponent
* Axon.ThreadedComponent.threadedadaptivecommscomponent

If your component needs to block - eg. wait on a system call; then make it a
'threaded' component. If it needs to change what inboxes or outboxes it has at
runtime, then make it an 'adaptive' component. Otherwise, simply make it an
ordinary component!



Adding and removing inboxes and outboxes
----------------------------------------

To add a new inbox or outbox call self.addInbox() or self.addOutbox() specifying
a base name for the inbox/outbox. The created inbox or outbox is immediately
ready to be used.::

    actualInboxName = self.addInbox("inputData")
    actualOutboxName = self.addOutbox("outputData")

You specify a name you would ideally like the inbox or outbox to be given. If
that name is already taken then a variant of it will be generated. Calls to
addInbox() and addOutbox() therefore return the actual name the inbox or outbox
was given. You should always use this returned name. It is unwise to assume your
ideal choice of name has been allocated!

To remove a box, call self.deleteInbox() or self.deleteOutbox() specifying the
name of the box to be deleted::

    self.deleteInbox(actualInboxName)
    self.deleteOutbox(actualOutboxName)

When deleting an inbox or outbox, try to make sure that any linkages involving
that inbox/outbox have been destroyed. This includes not only linkages created
by your component, but any created by other components too.



Tracking resources
------------------

adaptivecommscomponent also includes an ability to track associations between
resources and inboxes, outboxes and other information.

For example, you might want to associate another component (that your component
is interacting with) with the set of inboxes, outboxes and any other info that
are being used to communicate with it.

You can also associate particular inboxes or outboxes with those resources. This
therefore allows you to map both ways: "which resource relates to this inbox?"
and "which inboxes relate to this resource?"

For example, suppose a request leads to your component creating an inbox and
outbox to deal with another component. You might store these as a tracked
resource, along with other information, such as the 'other' component and any
state or linkages that were created; and associate this resource with the inbox
from which data might arrive::

    def wireUpToOtherComponent(self, theComponent):
        newIn  = self.addInbox("commsIn")
        newOut = self.addOutbox("commsOut")
    
        newState = "WAITING"
        inLinkage  = self.link((theComponent,itsOutbox),(self,newIn))
        outLinkage = self.link((theComponent,itsInbox), (self,newOut))
    
        resource = theComponent

        inboxes = [newIn]
        outboxes = [newOut]
        info = (newState, inLinkage, outLinkage)
        self.trackResourceInformation(resource, inboxes, outboxes, info)

        self.trackResource(resource, newIn)

If a message then arrives at that inbox, we can easily look up all the
information we might need know where it came from and how to handle it::

    def handleMessageArrived(self, inboxName):
        msg = self.recv(inboxName)

        resource = self.retrieveResource(inboxName)
        inboxes, outboxes, info = self.retrieveResourceInformation(resource)
        theComponent=resource

        ...

When you are finished with a resource and its associated information you can
clean it up with the ceaseTrackingResource() method which removes the
association between the resource and information. For example when you get rid
of a set of linkages and inboxes or outboxes associated with another component
you might want to clean up the resource you were using to track this too::

    def doneWithComponent(self, theComponent):
        resource=theComponent
        inboxes, outboxes, info = self.retrieveResourceInformation(resource)

        for name in inboxes:
            self.deleteInbox(name)
        for name in outboxes:
            self.deleteOutbox(name)

        state,linkages = info[0], info[1:]
        for linkage in linkages:
            self.unlink(thelinkage=linkage)
        
        self.ceaseTrackingResource(resource)


        
Implementation
--------------

AdaptiveCommsComponent's functionality above and beyond the ordinary
Axon.Component.component is implemented in a separate mixin class
_AdaptiveCommsable. This enables it to be reused for other variants on the
basic component that need to inherit this functionality - such as the
threadedadaptivecommscomponent.

When adding new inboxes or outboxes, name clashes are resolved by permuting the
box name with a suffixed unique ID number until there is no longer any clash.

"""

import sys
from Component import component
import idGen
from Box import makeInbox, makeOutbox

class _AdaptiveCommsable(object):
   """\
   Mixin for making a component 'adaptable' so that it can create and destroy
   extra inboxes and outboxes at runtime.
   """
   
   #
   # Public Methods
   #
   def __init__(self, *args, **argd):
      super(_AdaptiveCommsable, self).__init__(*args, **argd)
      self._resourceStore = {}
      self._resourceLookup = {}

   def trackResource(self, resource, inbox):
      """\
      Associate the specified resource with the named inbox.
      """
      self.inboxes[inbox] # Force failure if the inbox does not exist
      self._resourceLookup[inbox] = resource

   def retrieveTrackedResource(self, inbox):
      """\
      Retrieve the resource that has been associated with the named inbox.
      """
      return self._resourceLookup[inbox]

   def trackResourceInformation(self, resource, inboxes, outboxes, information):
      """\
      Store a list of inboxes, outboxes and other information as the specified
      resource.

      The inboxes and outboxes specified must exist.
      """
      "Provides a lookup service associating inboxes/outboxes & user information with a resource. Uses GIGO principle."
      #sys.stderr.write("OHHHH We're in HERE???!!\n"); sys.stderr.flush()
      # print "TRACKING", inboxes, outboxes, information
      # print "USING", repr(resource)

#      print "TRACKING FOR RESOURCE", resource
      [ self.inboxes[x] for x in inboxes] # Force an assertion if any inbox does not exist
      [ self.outboxes[x] for x in outboxes] # Force an assertion if any inbox does not exist
#      if self._resourceStore.get(resource, False):
#          print "Changing resources tracked for", resource
#          print "Was tracking", self._resourceStore[resource]
#          print "Now Tracking", (inboxes, outboxes, information)

      self._resourceStore[resource] = (inboxes, outboxes, information)


   def ceaseTrackingResource(self, resource):
      """Stop tracking a resource and release references to it"""
      # print "CEASING TO TRACK RESOURCE", repr(resource)
      del self._resourceStore[resource]

   def retrieveTrackedResourceInformation(self, resource):
      """\
      Retrieve a tuple (inboxes, outboxes, otherdata) that has been stored as
      the specified resource.
      """
#      print self._resourceStore
      return self._resourceStore[resource]

   def addInbox(self,*args):
      """
      Allocates a new inbox with name *based on* the name provided. If a box
      with the suggested name already exists then a variant is used instead.

      Returns the name of the inbox added.
      """
      name = self._newInboxName(*args)
      self.inboxes[name]=makeInbox(self.unpause)
      return name

   def deleteInbox(self,name):
      """\
      Deletes the named inbox. Any messages in it are lost.

      Try to ensure any linkages to involving this outbox have been destroyed -
      not just ones created by this component, but by others too! Behaviour is
      undefined if this is not the case, and should be avoided.
      """
      del self.inboxes[name]

   def addOutbox(self,*args):
      """\
      Allocates a new outbox with name *based on* the name provided. If a box
      with the suggested name already exists then a variant is used instead.

      Returns the name of the outbox added.
      """
      name = self._newOutboxName(*args)
      self.outboxes[name]=makeOutbox(self.unpause)
      return name

   def deleteOutbox(self,name):
      """\
      Deletes the named outbox.

      Try to ensure any linkages to involving this outbox have been destroyed -
      not just ones created by this component, but by others too! Behaviour is
      undefined if this is not the case, and should be avoided.
      """
      del self.outboxes[name]
      
   #
   # Private Methods
   #
   def _newInboxName(self, name="inbox"):
      """\
      Allocates a new inbox with name *based on* the name provided.

      If this name is available it will be returned unchanged.
      Otherwise the name will be returned with a number appended
      """
      while name in self.inboxes:
          name =name+str(idGen.idGen().next())
      return name
   #
   def _newOutboxName(self, name="outbox"):
      """\
      Allocates a new outbox name *based on* the name provided.

      If this name is available it will be returned unchanged.
      Otherwise the name will be returned with a number appended
      """
      while name in self.outboxes:
         name =name+str(idGen.idGen().next())
      return name


      
class AdaptiveCommsComponent(component, _AdaptiveCommsable):
   """\
   Base class for a component that works just like an ordinary component but can
   also 'adapt' its comms by adding or removing inboxes and outboxes whilst it
   is running.

   Subclass to make your own.

   See Axon.AdaptiveCommsComponent._AdaptiveCommsable for the extra methods that
   this subclass of component has.
   """
   def __init__(self,*args, **argd):
      component.__init__(self,*args, **argd)
      _AdaptiveCommsable.__init__(self)
          

if __name__=="__main__":
   print "Tests are separated into test/test_AdaptiveCommsableComponent.py"

