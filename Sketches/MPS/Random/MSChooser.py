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
   
   def __init__(self, items = [], loop = False):
      """Initialisation.
         items = set of items that can be iterated over. Must be finite.
         If an iterator is supplied, it is enumerated into a list during initialisation.
      """
      super(Chooser,self).__init__()
      
      self.items = list(items)
      self.index = 0
      self.loop = loop

   def shutdown(self):
        if self.dataReady("control"):
            message = self.recv("control")
            if isinstance(message, shutdownMicroprocess):
                self.send(message, "signal")
                return True
        return False

   def main(self):
      try:
         self.send( self.items[self.index], "outbox")
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
               self.index = self.index + 1
               if self.index >= len(self.items):
                  if self.loop:
                     self.index = 0
                  else:
                     self.index = len(self.items)-1               
            elif msg == "PREV":
               self.index = self.index - 1
               if self.index < 0:
                  if self.loop:
                     self.index = len(self.items)-1
                  else:
                     self.index = 0
            elif msg == "FIRST":
               self.index = 0
            elif msg == "LAST":
               self.index = 1

            try:
               self.send( self.items[self.index], "outbox")
            except IndexError:
               pass

         done = self.shutdown()

__kamaelia_components__  = ( Chooser, )
