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

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess


class passThrough(component):
   """\
   """
   Inboxes= {
      "inbox" : "",
      "control" : "",
   }
   Outboxes = {
      "outbox" : "", 
      "signal" : "",
   }

   Connections={ "inbox":"outbox","control":"signal" }
   
   def __init__(self, shutdownOn = [producerFinished,shutdownMicroprocess]):
      """\
      """
      self.__super.__init__()  # !!!! Must happen, if this method exists
      self.shutdownOn = shutdownOn

   def mainBody(self):
      """\
      """
      forwarded = 1
      
      for (inbox,outbox) in self.Connections.items():
      
         while self.dataReady(inbox):
             forwarded += 1
             data = self.recv(inbox)
             self.send(data, outbox)
             if inbox == "control":
                for ipc in self.shutdownOn:
                    if isinstance(data, ipc):
                        return 0
                
      return forwarded

__kamaelia_components__  = ( passThrough, )

      
if __name__=="__main__":
    from Axon.Component import scheduler
    from ConsoleEcho import consoleEchoer
    
    class fruitSource(component):
        def __init__(self):
            self.outlist = ["apples\n","pears\n","grapes\n","bananas\n","oranges\n","cherrys\n","lemons\n","<end of list>\n"]
            self.__super.__init__()

        def main(self):
            for i in self.outlist:
                self.send(i,"outbox")
                yield 1
            self.send(producerFinished(), "signal")
            yield 1

    
    class testComponent(component):
        Inboxes=['_control']
        Outboxes=['_signal']

        def __init__(self):
            self.__super.__init__()
            
            self.source = fruitSource()
            self.passT   = passThrough()
            self.dest   = consoleEchoer()
            self.addChildren(self.source, self.passT, self.dest)
            
            self.link((self.source, "outbox"),  (self.passT, "inbox"))
            self.link((self.passT,  "outbox"),  (self.dest,  "inbox"))
            self.link((self.source, "signal"),  (self.passT, "control"))
            self.link((self.passT , "signal"),  (self,       "_control"))
            self.link((self,        "_signal"), (self.dest,  "control"))

        def childComponents(self):
            return [self.source, self.passT, self.dest]

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
        
    print "Should output 7 fruit, followed by '<end of list>' then terminate.\n"
    
    scheduler.run.runThreads(slowmo=0)
    