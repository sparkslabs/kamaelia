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
import time

from util import removeAll
from idGen import strId, numId
from debug import debug
from Microprocess import microprocess
from AxonExceptions import AxonException
from Linkage import linkage

class postman(object):
    
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


   def __str__(self):
      "Provides a string representation of a postman, designed for debugging"
      result = "{{ POSTMAN: " + self.debugname
      result = result + "links " + self.linkages.__str__() + "; "
      result = result + "things " + self.things.__str__() + "; "
      result = result + microprocess.__str__(self) + " }}"
      return result

   def link(self, source, sink, passthrough=0):
       thelink = linkage(source,sink,passthrough)
       self.linkages.append(thelink)
       thelink.dst.addsource(thelink.src)
       return thelink

   def unlink(self, thecomponent=None, thelinkage=None):
        """\
        Destroys the specified linkage, or linkages for the specified component.
        
        Note, it only destroys linkages registered in this postoffice.
        """
        if thelinkage:
            try:
                self.linkages.remove(thelinkage)
            except ValueError:
                pass
            else:
                thelinkage.dst.removesource(thelinkage.src)
        if thecomponent:
            i=0
            num =len(self.linkages)
            while i<num:
                linkage = self.linkages[i]
                if linkage.source == thecomponent or linkage.sink == thecomponent:
                    num=num-1
                    self.unlink(thelinkage=linkage)
                else:
                    i=i+1
                    
        

   def deregister(self, name=None, component=None):
      if name and not component:
          if self.things[name]:
              component = self.things[name]
      return self.unlink(thecomponent=component)
       

   def deregisterlinkage(self, thecomponent=None,thelinkage=None):
       """Stub for legacy"""
       return self.unlink(thecomponent,thelinkage)

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


   def islinkageregistered(self, linkage):
      """Returns a true value if the linkage given is registered with the postman."""
      return self.linkages.count(linkage)



if __name__ == '__main__':
   print "Ynit tests are in test/test_Postman.py"
