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

# RETIRED
print """
/Sketches/filereading/InfiniteChooser.py:

 This file has been retired.
 It is retired because it is now part of the main code base.
 If you want to use this, you should be using Kamaelia.File.Chooser
    InfiniteChooser here is named ForwardIteratingChooser there

 This file now deliberately exits to encourage you to fix your code :-)
 (Hopefully contains enough info to help you fix it)
"""

import sys
sys.exit(0)
#

# This component is rather poorly named at the mo, since its behaviour is more one of (forwards) iteration
# and termination

import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess

class ForwardIteratingChooser(Axon.Component.component):
   """Iterates forwards items out of something iterable, as directed by commands sent to its inbox.
   
      Emits the first item at initialisation, then whenever a command is received
      it emits another item (unless you're asking it to step beyond the end of the set)

      Stepping beyond the end will cause this component to shutdown and emit a producerFinished msg
   """   
   Inboxes = { "inbox"   : "receive commands",
               "control" : ""
             }
   Outboxes = { "outbox" : "emits chosen items",
                "signal" : ""
              }
   
   def __init__(self, items = []):
      """Initialisation.
         items = set of items that can be iterated over. Can be infinite.
      """
      super(ForwardIteratingChooser,self).__init__()

      self.items = iter(items)
      self.gotoNext()


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
               if not send:
                   done = True
                   self.send( producerFinished(self), "signal")
            else:
               send = False

            if send:
               try:
                  self.send( self.getCurrentChoice(), "outbox")
               except IndexError:
                  pass

         done = done or self.shutdown()

   def getCurrentChoice(self):
      """Return the current choice"""
      try:
         return self.currentitem
      except AttributeError:
         raise IndexError()

            
   def gotoNext(self):
      """Advance the choice forwards one"""
      try:
         self.currentitem = self.items.next()
         return True
      except StopIteration:
         return False
