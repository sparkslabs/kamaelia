#!/usr/bin/python
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
