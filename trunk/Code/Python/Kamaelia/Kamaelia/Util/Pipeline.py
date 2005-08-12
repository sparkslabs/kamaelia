#!/usr/bin/env python

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

# component that creates and encapsulates a pipeline of components, connecting
# their outbox to inbox, and signal to control to form the pipeline chain.

from Axon.Scheduler import scheduler as _scheduler
import Axon as _Axon

component = _Axon.Component.component


class pipeline(component):

   def __init__(self, *components):
      super(pipeline,self).__init__()
      self.components = list(components)

   def main(self):
      self.addChildren(*self.components)
      pipeline = self.components[:]
      source = pipeline[0]
      del pipeline[0]
      while len(pipeline)>0:
         dest = pipeline[0]
         del pipeline[0]
         self.link((source,"outbox"), (dest,"inbox"))
         self.link((source,"signal"), (dest,"control"))
         source = dest
      self.link((self,"inbox"), (self.components[0],"inbox"), passthrough=1)
      self.link((self,"control"), (self.components[0],"control"), passthrough=1)
      self.link((self.components[-1],"outbox"), (self,"outbox"), passthrough=2)
      self.link((self.components[-1],"signal"), (self,"signal"), passthrough=2)
      yield _Axon.Ipc.newComponent(*(self.children))

      # run until all child components have terminated
      # at which point this component can implode

      # could just look for the first and last component terminating (the ends of the pipe)
      # BUT the creator of this pipeline might assume that the pipeline terminating means ALL
      # children have finished.
      while not self.childrenDone():
          # can't self.pause() as children may not pass data in/out of this pipeline, or may not immediately terminate      
          yield 1
          
      self.unplugChildren()
#      print "PIPELINE done"
      

   def childrenDone(self):
       """Unplugs any children that have terminated, and returns true if there are no
          running child components left (ie. their microproceses have finished)
       """
       for child in self.childComponents():
           if child._isStopped():
               self.removeChild(child)   # deregisters linkages for us
               
       return 0==len(self.childComponents())

           
   def unplugChildren(self):
      for child in self.childComponents():
         self.removeChild(child)   # deregisters linkages for us
          

                  
if __name__=="__main__":
    from Axon.Component import scheduler
    from ConsoleEcho import consoleEchoer
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
            self.pipe   = pipeline(passThrough([]))
            self.dest   = consoleEchoer()
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
    