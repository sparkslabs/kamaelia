#!/usr/bin/python
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
from Axon.Ipc import producerFinished

class Chooser(Axon.Component.component):
   """Chooses items out of a set, as directed by commands sent to its inbox

      Emits the first item at initialisation, then whenever a command is received
      it emits another item (unless you're asking it to step beyond the start or
      end of the set)
   """
   
   Inboxes = { "inbox"   : "receive commands",
               "control" : ""
             }
   Outboxes = { "outbox" : "emits chosen items",
                "signal" : ""
              }
   
   def __init__(self, items = []):
      """Initialisation.
         items = set of items that can be iterated over. Must be finite.
         If an iterator is supplied, it is enumerated into a list during initialisation.
      """
      super(Chooser,self).__init__()
      
      self.items = list(items)
      self.useditems = []

      
   def shutdown(self):
        if self.dataReady("control"):
            message = self.recv("control")
            if isinstance(message, shutdownMicroprocess):
                self.send(message, "signal")
                return True
        return False


            
   def main(self):
      try:
         self.send( self.getCurrentChoice(), "outbox")
      except IndexError:
         pass
         
      done = False
      while not done:
         yield 1

         while self.dataReady("inbox"):
            send = True
            msg = self.recv("inbox")

            if msg == "SAME":
               pass
            elif msg == "NEXT":
               send = self.gotoNext()
            elif msg == "PREV":
               send = self.gotoPrev()
            elif msg == "FIRST":
               send = self.gotoFirst()
            elif msg == "LAST":
               send = self.gotoLast()
            else:
               send = False

            if send:
               try:
                  self.send( self.getCurrentChoice(), "outbox")
               except IndexError:
                  pass

         done = self.shutdown()

   
   def getCurrentChoice(self):
      """Return the current choice to the outbox"""
      return self.items[0]
            
   def gotoNext(self):
      """Advance the choice forwards one"""
      if len(self.items) > 1:
         self.useditems.append(self.items[0])
         del(self.items[0])
         return True
      return False

   def gotoPrev(self):
      """Backstep the choice backwards one"""
      try:
         self.items.insert(0, self.useditems[-1])
         del(self.useditems[-1])
         return True
      except IndexError:
         return False
   
   def gotoLast(self):
      """Goto the last item in the set"""
      self.useditems.extend(self.items[:-1])
      self.items = [self.items[-1]]
      return True
            
   def gotoFirst(self):
      """Goto the first item in the set"""
      self.useditems.extend(self.items)
      self.items = self.useditems
      self.useditems = []
      return True
      