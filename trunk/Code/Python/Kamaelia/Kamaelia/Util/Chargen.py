#!/usr/bin/python
#
# Simple udp /multicast/ sender and receiver
# Logically these map to being a single component each
#

import socket
import Axon

class Chargen(Axon.Component.component):
   # SMELL: Might be nice to set a rate.
   def main(self):
      while 1:
         self.send("Hello World", "outbox")
         yield 1

def tests():
   from Axon.Scheduler import scheduler
   from Kamaelia.Util.ConsoleEcho import consoleEchoer

   class testComponent(Axon.Component.component):
      def main(self):
        chargen= Chargen()
        display = consoleEchoer()

        self.link((chargen,"outbox"), (display,"inbox"))
        self.addChildren(chargen, display)
        yield Axon.Ipc.newComponent(*(self.children))
        while 1:
           self.pause()
           yield 1

   harness = testComponent()
   harness.activate()
   scheduler.run.runThreads(slowmo=0)

if __name__=="__main__":

    tests()
     