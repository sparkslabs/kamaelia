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
"""\
==================================
Wiring up components in a Pipeline
==================================

The Pipeline component wires up a set of components in a linear chain (a
Pipeline) and encapsulates them as a single component.



Example Usage
-------------

A simple pipeline of 4 components::

    Pipeline(MyDataSource(...),
             MyFirstStageOfProcessing(...),
             MySecondStageOfProcessing(...),
             MyDestination(...),
            ).run()


How does it work?
-----------------
A Pipeline component gives you a way of wiring up a system of components in a
chain and then encapsulating the whole as a single component. The inboxes of
this component pass through to the inboxes of the first component in the
Pipeline, and the outboxes of the last component pass through to the outboxes
of the Pipeline component.

The components you specify are registered as children of the Pipeline
component. When Pipeline is activate, all children are wired up and activated.

For the components in the Pipeline, "outbox" outboxes are wired to "inbox"
inboxes, and "signal" outboxes are wired to "control" inboxes. They are wired
up in the order in which you specify them - data will flow through the chain
from first component to last.

The "inbox" and "control" inboxes of the Pipeline component are wired to
pass-through to the "inbox" and "control" inboxes (respectively) of the first
component in the Pipeline chain.

The "outbox" and "signal" outboxes of the last component in the Pipeline chain
are wired to pass-through to the "outbox" and "signal" outboxes (respectively)
of the Pipeline component.

During runtime, the Pipeline component monitors the child components. It will
terminate if, and only if, *all* the child components have also terminated.

NOTE that if your child components create additional components themselves, the
Pipeline component will not know about them. It only monitors the components it
was originally told about.

Pipeline does not intercept any of its inboxes or outboxes. It ignores whatever
traffic flows through them.
"""

# component that creates and encapsulates a Pipeline of components, connecting
# their outbox to inbox, and signal to control to form the Pipeline chain.

from Axon.Scheduler import scheduler as _scheduler
import Axon as _Axon

component = _Axon.Component.component


class Pipeline(component):
   """\
   Pipeline(\*components) -> new Pipeline component.

   Encapsulates the specified set of components and wires them up in a chain
   (a Pipeline) in the order you provided them.
   
   Keyword arguments:
   
   - components  -- the components you want, in the order you want them wired up
   """
   circular = False
   def __init__(self, *components, **argv):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(Pipeline,self).__init__(**argv)
      self.components = list(components)

   def main(self):
      """Main loop."""
      self.addChildren(*self.components)
      Pipeline = self.components[:]
      source = Pipeline[0]
      del Pipeline[0]
      while len(Pipeline)>0:
         dest = Pipeline[0]
         del Pipeline[0]
         self.link((source,"outbox"), (dest,"inbox"))
         self.link((source,"signal"), (dest,"control"))
         source = dest
      self.link((self,"inbox"), (self.components[0],"inbox"), passthrough=1)
      self.link((self,"control"), (self.components[0],"control"), passthrough=1)
      if self.circular:
          self.link((self.components[-1],"outbox"), (self.components[0],"inbox"))
          self.link((self.components[-1],"signal"), (self.components[0],"control"))
      else:
          self.link((self.components[-1],"outbox"), (self,"outbox"), passthrough=2)
          self.link((self.components[-1],"signal"), (self,"signal"), passthrough=2)

      for child in self.children:
          child.activate()

      # run until all child components have terminated
      # at which point this component can implode

      # becuase they are children, if they terminate, we'll be woken up
      while not self.childrenDone():
          self.pause()
          yield 1



   def childrenDone(self):
       """Unplugs any children that have terminated, and returns true if there are no
          running child components left (ie. their microproceses have finished)
       """
       for child in self.childComponents():
           if child._isStopped():
               self.removeChild(child)   # deregisters linkages for us

       return 0==len(self.childComponents())

import Kamaelia.Support.Deprecate as Deprecate

pipeline = Deprecate.makeClassStub(
    Pipeline,
    "Use Kamaelia.Chassis.Pipeline:Pipeline instead of Kamaelia.Chassis.Pipeline:pipeline",
    "WARN"
    )

__kamaelia_components__  = ( Pipeline, )
                  
if __name__=="__main__":
    from Axon.Component import scheduler
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Util.PassThrough import PassThrough
    
    from Axon.Ipc import producerFinished, shutdownMicroprocess
    
    class fruitSource(component):
        def __init__(self):
            super(fruitSource,self).__init__()
            self.outlist = ["apples\n","pears\n","grapes\n","bananas\n","oranges\n","cherrys\n","lemons\n","<end of list>\n"]

        def main(self):
            for i in self.outlist:
                self.send(i,"outbox")
                yield 1
            self.send(producerFinished(self), "signal")
            yield 1

    
    class testComponent(component):
        Inboxes=['_control']
        Outboxes=['_signal']

        def __init__(self):
            super(testComponent,self).__init__()
            
            self.source = fruitSource()
            self.pipe   = Pipeline(PassThrough([]))
            self.dest   = ConsoleEchoer()
            self.addChildren(self.source, self.pipe, self.dest)
            
            self.link((self.source, "outbox"),  (self.pipe, "inbox"))
            self.link((self.source, "signal"),  (self.pipe, "control"))
            
            self.link((self.pipe,   "outbox"),  (self.dest, "inbox"))
            self.link((self.pipe,   "signal"),  (self,      "_control"))
            
            self.link((self,        "_signal"), (self.dest, "control"))

        def childComponents(self):
            return [self.source, self.pipe, self.dest]

        def main(self):
            done = False
            while not done:
                if self.dataReady("_control"):
                    data = self.recv("_control")
                    done = done or isinstance(data, producerFinished) or isinstance(data, shutdownMicroprocess)
                    self.send(data, "_signal")
                yield 1


    r = scheduler()
    t = testComponent()
    t.activate()
    cs = t.childComponents()
    for c in cs:
        c.activate()
        
    print ("Should output 7 fruit, followed by '<end of list>'.\n")
    
    scheduler.run.runThreads(slowmo=0)
    