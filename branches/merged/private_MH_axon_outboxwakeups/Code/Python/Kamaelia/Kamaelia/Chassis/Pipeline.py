#!/usr/bin/env python

# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""\
==================================
Wiring up components in a Pipeline
==================================

The Pipeline component wires up a set of components in a linear chain (a
Pipeline) and encapsulates them as a single component.



Example Usage
-------------
::
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
   Pipeline(*components) -> new Pipeline component.

   Encapsulates the specified set of components and wires them up in a chain
   (a Pipeline) in the order you provided them.
   
   Keyword arguments:
   
   - components  -- the components you want, in the order you want them wired up
   """
   def __init__(self, *components):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(Pipeline,self).__init__()
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
    from Console import ConsoleEchoer
    from passThrough import passThrough
    
    from Axon.Ipc import producerFinished, shutdownMicroprocess
    
    class fruitSource(component):
        def __init__(self):
            self.outlist = ["apples\n","pears\n","grapes\n","bananas\n","oranges\n","cherrys\n","lemons\n","<end of list>\n"]
            self.__super.__init__()

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
            self.__super.__init__()
            
            self.source = fruitSource()
            self.pipe   = Pipeline(passThrough([]))
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
        
    print "Should output 7 fruit, followed by '<end of list>'.\n"
    
    scheduler.run.runThreads(slowmo=0)
    