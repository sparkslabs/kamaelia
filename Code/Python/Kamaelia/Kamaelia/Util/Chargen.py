#!/usr/bin/env python
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
"""\
==========================
Simple Character Generator
==========================

This component is intended as a simple 'stream of characters' generator.

At the moment, it continually sends the string "Hello world" as fast as it can,
indefinitely out of its "outbox" outbox.



Example Usage
-------------
::
    >>> Pipeline( Chargen(), ConsoleEchoer() ).run()
    Hello WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello WorldHel
    lo WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello
    WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello Wor
    ldHello WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello WorldH
    ello WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello WorldHell

    ... you get the idea!


    
How does it work?
-----------------

This component, once activated repeatedly emits the string "Hello World" from
its "outbox" outbox. It is emitted as a single string. It does this continuously
forever. It is not rate limited in any way, and so emits as fast as it can.

This component does not terminate, and ignores messages arriving at any of its
inboxes. It does not output anything from its "signal" outbox.
"""

import socket
import Axon

class Chargen(Axon.Component.component):
   """\
   Chargen() -> new Chargen component.

   Component that emits a continuous stream of the string "Hello World" from its
   "outbox" outbox as fast as it can.
   """

   Inboxes  = { "inbox"   : "NOT USED",
                "control" : "NOT USED",
              }
   Outboxes = { "outbox" : "NOT USED",
                "signal" : "NOT USED",
              }
   
   # SMELL: Might be nice to set a rate.
   def main(self):
      """Main loop."""
      while 1:
         self.send("Hello World", "outbox")
         yield 1

def tests():
   from Axon.Scheduler import scheduler
   from Kamaelia.Util.Console import ConsoleEchoer

   class testComponent(Axon.Component.component):
      def main(self):
        chargen= Chargen()
        display = ConsoleEchoer()

        self.link((chargen,"outbox"), (display,"inbox"))
        self.addChildren(chargen, display)
        yield Axon.Ipc.newComponent(*(self.children))
        while 1:
           self.pause()
           yield 1

   harness = testComponent()
   harness.activate()
   scheduler.run.runThreads(slowmo=0)

__kamaelia_components__  = ( Chargen, )


if __name__=="__main__":

    tests()
     # Needed to allow import
