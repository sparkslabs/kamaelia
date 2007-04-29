#!/usr/bin/env python2.3
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""Kamaelia Concurrency Component Framework.

POSTMAN

A postman is a microprocess that knows about linkages, and components,
and hence runs concurrently to your components. It can have a number of
components & linkages registered with it.

Periodically it checks the sources of the linkages it knows about for
messages. If it finds some messages it checks where to deliver them to by
looking at the sink of the linkage. Assuming it finds a destination to deliver to, the
postmans then delivers the messages to the inbox of the assigned destination
component.

"""
from __future__ import generators

import time

from util import removeAll
from idGen import strId, numId
#from debug import debug
from Microprocess import microprocess
from AxonExceptions import AxonException

class postman(microprocess):
   """The Postman microprocess handles message delivery along linkages
   between inboxes and outboxes, usually contained in components.
   There is one postman per component.

   Since a postman is a microprocess it runs in parallel with the components
   it's delivering messages between.

   !!!! It is highly possible this could result in a race hazard if message queues
   !!!! can grow faster than the postman can deliver them. As a result the system
   !!!! provides Synchronised Boxes as well which have a maximum, enforced
   !!!! capacity which works to prevent this issue - at the expense of extra logic
   !!!! in the client

   A Postman can have a debug name - this is to help differentiate between
   postmen who are delivering things versus those that aren't if problems
   arise.
   """
   def __init__(self, debugname=""):
      """ Constructor. If a debug name is assigned this will be stored as a
      debugname attribute. Other attributes:
         * linkages = list of linkages this postman needs to know about
         * things = dict of things this postman has to monitor outboxes on.
         the index into the dict is the name of the thing monitored, with the
         value being the thing.
         * reverse things = this provides a reverse lookup of things - the index
         being the id of the component, the value being the name of the
         component.
      The super class's constructor is then called to make this a fully initialised
      microprocess.
      """
      super(postman, self).__init__()
      if debugname:
         self.debugname = debugname + ":debug "
      else:
         self.debugname =""
      self.linkages = list()
      self.things = dict()
      self.reversethings = dict()

   def __str__(self):
      "Provides a string representation of a postman, designed for debugging"
      result = "{{ POSTMAN: " + self.debugname
      result = result + "links " + self.linkages.__str__() + "; "
      result = result + "things " + self.things.__str__() + "; "
      result = result + microprocess.__str__(self) + " }}"
      return result

   def register(self, name, component):
      """Registers a _named_ component with the postman.
      These are stored in forward & reverse lookup tables.
      """
#      assert self.debugger.note("postman.register",5,self.name,name,component)
      self.things[name] = component
      self.reversethings[id(component)] = name

   def registerlinkage(self, thelinkage):
      """Registers a linkage with the postman. It's likely this is
      actually more useful, looking back on this design, since we
      only deliver things along linkages. (no defaults)
      """
#      assert self.debugger.note("postman.registerlinkage",5,self.name, thelinkage)
      self.linkages.append(thelinkage)

   def deregister(self, name=None, component=None):
      """This deregisters a component from this postman, deleting
      the reference to the component object. If the reference isn't
      deleted, the reference count of the object will never reach
      zero and never be garbage collected.

      Attempts to partially deal with broken usage. (Which makes this longer
      than it might need to be otherwise.)
      """
      # Most common case by far. (Only one done by Component) - Other cases use this by tail recursion
      if component and (not name):
         if self.reversethings[id(component)]:
            del self.things[self.reversethings[id(component)]]
         del self.reversethings[id(component)]
         return self.deregisterlinkage(thecomponent=component)
      if name and (not component):
         if self.things[name]:
            return self.deregister(component=self.things[name]) # Simpify to common case and call recursively.
      if name and component:
         if self.things[name] == component: # If name matches the component
            return self.deregister(component=component) # Simpify to common case and call recursively.
         else:
            raise AxonException("Attempt to deregister name" + name + "component " + `component` + "at same time but don't match!")
      #if (not name) and (not component):
      raise AxonException("Attempted to deregister null name & null component")

   def deregisterlinkage(self, thecomponent=None,thelinkage=None):
      """De registers a linkage, based on a provided component. Does not yet
      de-register based on a user supplied linkage.
      Simply loops through the linkages, looking for the component being
      de-registered, and de-registers (deletes) any linkages with that component
      referenced inside.
      """
      if (not thelinkage) and (not thecomponent):
         raise AxonException("Attempt to deregister linkage with both args null")
      if (thelinkage and thecomponent):
         raise AxonException("Attempt to deregister linkage with both args not null" + `thelinkage` + " " + `thecomponent`)
      num = len(self.linkages) # Number of linkages.
      i = 0
      if (thelinkage):
         while num > 0:
            num = num - 1
            if self.linkages[num] is thelinkage:
#               assert self.debugger.note("postman.deregisterlinkage", 5,"Flushing linkage", thelinkage)
               while thelinkage.dataToMove():
#                  assert self.debugger.note("postman.deregisterlinkage", 5,"Flushing ", thelinkage.source.name,thelinkage.sink.name)
                  thelinkage.moveData(True)
               del self.linkages[num]
      while (i < num):
         if ((self.linkages[i].source is thecomponent) or
             (self.linkages[i].sink is thecomponent)):
            num = num -1 # We remove an item from the list, so num shrinks by 1
#            assert self.debugger.note("postman.deregisterlinkage", 5,"Flushing linkage", self.linkages[i])
            while self.linkages[i].dataToMove():
#               assert self.debugger.note("postman.deregisterlinkage", 5,"Flushing ", self.linkages[i].source.name,self.linkages[i].sink.name)
               self.linkages[i].moveData(True)
            del self.linkages[i]
         else:
            i = i +1

# Removed because it is a debugging function that if needed should be implemented elsewhere or should return the objects in a structure rather than a formatted string.
   def showqueuelengths(self):
      """Debugging function really. Takes the debug name of this postman,
      and appends a textual description of the queue lengths of the inboxes
      and outboxes of all the components this postman takes from/delivers to.
      Result is a string, does NOT send output to any output stream. (Did
      originally, hence "show", is likely to be renamed slightly.)
      """
      result = "" + self.debugname
      for componentname in self.things.keys():
         result = result + "Component "+ componentname +" ["
         for inbox in self.things[componentname].inboxes.keys():
            result = result + " " + inbox + ":"+ len(self.things[componentname].inboxes[inbox]).__str__()
         for outbox in self.things[componentname].outboxes.keys():
            result = result + " " + outbox + ":" + len(self.things[componentname].outboxes[outbox]).__str__()
         result = result + "]\n"
      return result

   def domessagedelivery(self):
      """Performs the actual message delivery activity.
      Loops through the *linkages*, scanning their sources, collects messages
      for delivery to the sinkwbox of the recipient.
      """
#      assert self.debugger.note("postman.domessagedelivery", 5,self.name,self.showqueuelengths())
      # The following commented code has no significant effects.  Only debugging purposes.  Above may be sufficient for the case.
##~       if self.linkages == [] :
##~          assert self.debugger.note("postman.domessagedelivery.linkages", 10, "No Destinations")
##~          return

#      assert self.debugger.note("postman.domessagedelivery.linkages", 5, self.name, self.linkages)

      for link in self.linkages:
#         assert self.debugger.note("postman.domessagedelivery.linkages", 5, self.name, "So Far")
#         assert self.debugger.note("postman.domessagedelivery", 7, "DELIVERY", link.sinkbox,link.sink.name)
#         assert self.debugger.note("postman.domessagedelivery", 10, self.name +" taking message from ", link.source.name, "outbox", link.sourcebox, " delivering to ", link.sink.name, " inbox ", link.sinkbox)
         if link.dataToMove():
#             if link.showtransit:
#                 assert self.debugger.note("postman.specificTransits", 1, self.name + " "+ str(link))
             link.moveData()

   def islinkageregistered(self, linkage):
      """Returns a true value if the linkage given is registered with the postman."""
      return self.linkages.count(linkage)

   def main(self):
      yield "initialised"
      while 1:
         self.domessagedelivery()
#         assert self.debugger.note("postman.main",10,self.name)
         yield 1


if __name__ == '__main__':
   print "Ynit tests are in test/test_Postman.py"
