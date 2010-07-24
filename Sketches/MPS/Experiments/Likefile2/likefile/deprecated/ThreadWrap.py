#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

# component that creates and encapsulates a Pipeline of components, connecting
# their outbox to inbox, and signal to control to form the Pipeline chain.

import Axon
import time
import Queue

class ThreadWrap(Axon.ThreadedComponent.threadedcomponent):
   Inboxes = {
       "inbox":"From the outside world",
       "control":"From the outside world",

       "_inbox":"From the component to go to the outside world",
       "_control":"From the component to go to the outside world",
   }
   Outboxes = {
       "outbox":"To the outside world",
       "signal":"To the outside world",

       "_outbox":"From the outside world to go to the component",
       "_signal":"From the outside world to go to the component",
   }
   def __init__(self, someComponent):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(ThreadWrap,self).__init__()
      self.comp = someComponent
      self.inboundData = Queue.Queue()
      self.outboundData = Queue.Queue()

   def put(self, *args):
       self.inboundData.put(*args)

   def get(self):
       return self.outboundData.get_nowait()

   def main(self):
      """Main loop."""
      self.addChildren(self.comp)

      self.link((self,"_outbox"), (self.comp,"inbox"))
      self.link((self,"_signal"), (self.comp,"control"))
      self.link((self.comp,"outbox"), (self,"_inbox"))
      self.link((self.comp,"signal"), (self,"_control"))

      for child in self.children:
          child.activate()

      # run until all child components have terminated
      # at which point this component can implode

      # becuase they are children, if they terminate, we'll be woken up
      while not self.childrenDone():

          # We manually forward the data here. There are probably nicer methods, but for the
          # moment, lets stick to brute force/clarity

          time.sleep(0.01) # so that we're not totally spinning

          while self.dataReady("inbox"):
              self.send(self.recv("inbox"), "_outbox")
          while self.dataReady("control"):
              self.send(self.recv("control"), "_signal")

          while self.dataReady("_inbox"):
              self.outboundData.put( (self.recv("_inbox"), "outbox") )
          while self.dataReady("_control"):
              self.send(self.recv("_control"), "signal")


   def childrenDone(self):
       """Unplugs any children that have terminated, and returns true if there are no
          running child components left (ie. their microproceses have finished)
       """
       for child in self.childComponents():
           if child._isStopped():
               self.removeChild(child)   # deregisters linkages for us

       return 0==len(self.childComponents())
                  
if __name__=="__main__":
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    from Kamaelia.Chassis.Pipeline import Pipeline
    import time
    class Waiter(Axon.Component.component):
        def main(self):
            print "RUNNING"
            t = time.time()
            while time.time()-t >2:
                yield 1
            print "DONE"
            
    # All the following run as you would expect at this stage
    if 0:
        Waiter().run()

    if 0:
        ThreadWrap( Waiter() ).run()

    if 1:
        Pipeline(
            ThreadWrap(ConsoleReader()),
            ConsoleEchoer(),
        ).run()
