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
"""\
===================
Passthrough of data
===================

The PassThrough component simply passes through data from its "inbox" inbox
to its "outbox" outbox.

This can be used, for example, as a dummy 'protocol' component - slotting it
into a system where ordinarily a component would go that somehow changes or
processes the data passing through it.



Example Usage
-------------

Creating a simple tcp socket server on port 1850 that echoes back to clients
whatever they send to it::

    def echoProtocol:
        return PassThrough()
    
    SimpleServer( protocol=echoProtocol, port=1850 ).run()



More Detail
-----------

Send any item to PassThrough component's "inbox" inbox and it will
immediately be sent on out of the "outbox" outbox.

If a producerFinished or shutdownMicroprocess message is received on the
"control" inbox then this component will immediately terminate. It will
send the message on out of its "signal" outbox. Any pending data waiting
in the "inbox" inbox may be lost.

"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess


class PassThrough(component):
   """\
   """
   Inboxes= {
      "inbox" : "Messages to be passed through",
      "control" : "Shutdown signalling",
   }
   Outboxes = {
      "outbox" : "Passed through messages", 
      "signal" : "Shutdown signalling",
   }

   Connections={ "inbox":"outbox","control":"signal" }
   
   def __init__(self, shutdownOn = [producerFinished,shutdownMicroprocess]):
      """\
      """
      super(PassThrough,self).__init__()
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
                    
      self.pause()
      return forwarded


import Kamaelia.Support.Deprecate as Deprecate

passThrough = Deprecate.makeClassStub(
    PassThrough,
    "Use Kamaelia.Util.PassThrough:PassThrough instead of Kamaelia.Util.PassThrough:passThrough or Kamaelia.Util.passThrough.PassThrough",
    "WARN"
    )


__kamaelia_components__  = ( PassThrough, )

      
if __name__=="__main__":
    from Axon.Component import scheduler
    from Console import ConsoleEchoer
    
    class fruitSource(component):
        def __init__(self):
            self.outlist = ["apples\n","pears\n","grapes\n","bananas\n","oranges\n","cherrys\n","lemons\n","<end of list>\n"]
            super(fruitSource,self).__init__()

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
            super(testComponent,self).__init__()
            
            self.source = fruitSource()
            self.passT   = PassThrough()
            self.dest   = ConsoleEchoer()
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
        
    print ("Should output 7 fruit, followed by '<end of list>' then terminate.\n")
    
    scheduler.run.runThreads(slowmo=0)
    