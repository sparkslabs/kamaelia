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
"""
This component allows the data from a single outbox to be sent to many inboxes.

This version blocks all data if any of the outboxes have no space in them.
Other versions could take other approaches such as dropping messages to those
outboxes which are full.
"""


import Axon.AdaptiveCommsComponent
from Axon.Ipc import ipc
from Axon.Linkage import linkage

class addsink(ipc):
   def __init__(self, sink, sinkbox="inbox"):#, sinkcontrol = None):
      self.sink = sink
      self.sinkbox = sinkbox
#      self.sinkcontrol = sinkcontrol

class removesink(ipc):
   def __init__(self,sink,sinkbox="inbox"):
      self.sink = sink
      self.sinkbox = sinkbox

class Splitter(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
   #inbox is the box for data too be split.  control is for future use to also split the signal/control data
   #associated with the main data.  configuration is the port to send requests for extra outward connections
   #and for deletions.
   Inboxes = ["inbox", "control", "configuration"]
   Outboxes = ["signal"]

   def __init__(self):
      super(Splitter,self).__init__()
      #outlist is for tuples of (sinkcomponent, sinkbox) to a tuple of (outboxname, linkage)
      self.outlist = {}
   
   def mainBody(self):
         postponedmesage = None
         self.delayedboxlist = []
         dontpause = False # Assumption is that we should be able to pause after finishing
         if self.dataReady("configuration"):
            mes = self.recv("configuration")
            dontpause = True
            if isinstance(mes, addsink):
               self.createsink(mes.sink,mes.sinkbox)
            elif isinstance(mes,removesink):
               self.deletesink(mes)
         if postponedmesage:
            mes,bl = postponedmesage, self.delayedboxlist
            postponedmesage, self.delayedboxlist = None, []
            for box in bl:
                try:
                    self.send(mes,self.outlist[box][0])
                except noSpaceInBox:
                    postponedmesage = mes
                    self.delayedboxlist.append(box)
         if self.dataReady() and not postponedmesage:
            mes = self.recv()
            dontpause = True
            for box in self.outlist:
               try:
                  self.send(mes,self.outlist[box][0])
               except noSpaceInBox:
                  postponedmesage = mes
                  self.delayedboxlist.append(box)
         if postponedmesage or not dontpause:
            self.pause()
         return 1

   def createsink(self, sink, sinkbox="inbox"):
      name = self.addOutbox(sink.name + '-' + sinkbox)
      lnk = linkage(source = self, sourcebox = name, sink = sink, sinkbox = sinkbox, postoffice = self.postoffice)
      self.outlist[(sink,sinkbox)] = (name, lnk)
   
   def deletesink(self, oldsink):
      sink = self.outlist[(oldsink.sink,oldsink.sinkbox)]
      del self.outlist[(oldsink.sink,oldsink.sinkbox)]
      self.postoffice.deregisterlinkage(thelinkage=sink[1])
      self.deleteOutbox(sink[0])
      try:
        self.delayedboxlist.remove(sink[0])
      except ValueError:
        pass # Common occurence, not an error.
   
