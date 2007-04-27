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

LINKAGES

Components only have input & output boxes. For data to get from a producer
(eg a file reader) to a consumer (eg an encryption component) then the output
of one component, the source component, must be linked to the input of
another component, the sink component.

These need to be registered with a postman (see below) who takes messages
from the outputs and delivers them to the appropriate destination. This is NOT
the usual technique for software messaging. Normally you create messages,
addressed to something specific, and then the message handler delivers them.

However the method of communication used here is the norm for _hardware_ systems,
and generally results in very pluggable components - the aim of this system,
hence this design approach rather than the normal. This method of
communication is also the norm for one form of software system - unix shell
scripting - something that has shown itself time and again to be used in ways
the inventors of programs/components never envisioned.

"""
import time

from AxonExceptions import AxonException, ArgumentsClash
from Axon import AxonObject
from util import removeAll
from idGen import strId, numId,Debug
from debug import debug

class linkage(AxonObject):
   """Linkage - Since components can only talk to local interfaces, this defines the linkages
   between inputs and outputs of a component.
   At present no argument is really optional.
   """
   def __init__(self, source, sink, sourcebox="outbox", sinkbox="inbox",
                postoffice=None, passthrough=0, pipewidth=0,
                synchronous=None):
      # passthrough==0 -> outbox > inbox
      # passthrough==1 -> inbox > inbox
      # passthrough==2 -> outbox > outbox
      # There is potential for a value 3 that passes through data that a component no longer has a need to process.  This is not implemented yet!

      """ This needs to tag the source/sink boxes as synchronous, to get component to go "BANG" if
      writing to a blocked
      """
      if not sourcebox in source.outboxes:
         if not (passthrough ==  1): # If passthrough in, the source will be an _inbox_
            raise AxonException("No such outbox: " + sourcebox+":"+str(source))
      if not sinkbox in sink.inboxes:
         if not (passthrough ==  2): # If passthrough in, the sink will be an _outbox_
            raise AxonException("No such inbox: " + sinkbox+" Component: "+str(sink))
      self.source = source
      self.sink = sink
      self.sourcebox = sourcebox
      self.sinkbox = sinkbox
      self.showtransit = 0
      self.passthrough = passthrough
      self.pipewidth=pipewidth
      if pipewidth:
         if not synchronous and synchronous is not None:
            raise ArgumentsClash("When creating a linage if pipewidth is set then synchronous must not be false!!!",pipewidth,synchronous)
         self.setSynchronous()
      elif synchronous:
         self.pipewidth = 1
         self.setSynchronous()
      else:
         self.synchronous=False
      if not (postoffice ==None):
         postoffice.registerlinkage(self)
      assert Debug("linkage.linkage",1,self)

   def setSynchronous(self, pipewidth = None):
      self.synchronous=True
      if pipewidth is not None:
         self.pipewidth=pipewidth
      if not self.pipewidth:
         self.pipewidth=1
      assert self.pipewidth > 0
      if self.passthrough ==0:
         self.source._synchronisedBox("source","outbox",self.sourcebox, self.pipewidth)
         self.sink._synchronisedBox("sink","inbox",self.sinkbox, self.pipewidth)
      if self.passthrough ==1:
         self.source._synchronisedBox("source","inbox",self.sourcebox, self.pipewidth)
         self.sink._synchronisedBox("sink","inbox",self.sinkbox, self.pipewidth)
      if self.passthrough ==2:
         self.source._synchronisedBox("source","outbox",self.sourcebox, self.pipewidth)
         self.sink._synchronisedBox("sink","outbox",self.sinkbox, self.pipewidth)     
      
   def sourcePair(self):
      return self.source, self.sourcebox

   def sinkPair(self):
      return self.sink, self.sinkbox

   def __str__(self):
      return "Link( source:[" + self.source.name + "," + self.sourcebox + "], sink:[" + self.sink.name + "," + self.sinkbox + "] )"

   def dataToMove(self):
      if self.passthrough == 1:
         return len(self.source.inboxes[self.sourcebox]) > 0
      else:
         return len(self.source.outboxes[self.sourcebox]) > 0

   def moveDataWithCheck(self):
      if self.dataToMove():
         self.moveData()

   def moveData(self, force = False):
      if self.synchronous and not force: # Check the sink has space to recieve the data
         if self.passthrough != 2: # Delivering to an inbox
            if len(self.sink.inboxes[self.sinkbox]) >= self.pipewidth:
               return # Do not perform delivery
         elif len(self.sink.outboxes[self.sinkbox]) >= self.pipewidth:
               return # Do not perform delivery
      if self.showtransit:
         print "SOURCE:", self.source.name, self.sourcebox
         print "SINK:", self.sink.name, self.sinkbox
      if self.passthrough==0:
         message = self.source._collect(self.sourcebox)
         self.sink._deliver(message,self.sinkbox,force)
         return
      if self.passthrough==1: # Passthrough In
         message = self.source._collectInbox(self.sourcebox)
         self.sink._passThroughDeliverIn(message,self.sinkbox,force)
         return
      if self.passthrough==2: # Passthrough Out
         message = self.source._collect(self.sourcebox)
         self.sink._passThroughDeliverOut(message,self.sinkbox,force)
         return
   
   def setShowTransit(self, showtransit):
      self.showtransit=showtransit

if __name__ == '__main__':
   print "This code current has no test code"
