#!/usr/bin/python
#
# Basic acceptance test harness for the Multicast_sender and receiver
# components.
#

import socket
import Axon

def tests():
   from Axon.Scheduler import scheduler
   from Kamaelia.Util.Console import ConsoleEchoer
   from Kamaelia.Util.Chargen import Chargen

   from Kamaelia.Internet.Multicast_sender import Multicast_sender
   from Kamaelia.Internet.Multicast_receiver import Multicast_receiver
   from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver


   Graphline(chargen = = Chargen(),
            sender   = Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600),
            receiver = Multicast_transceiver("0.0.0.0", 1600, "224.168.2.9", 0),
            display = ConsoleEchoer()

        self.link((chargen,"outbox"), (sender,"inbox"))
        self.link((receiver,"outbox"), (display,"inbox"))
        self.addChildren(chargen, sender, receiver, display)
        yield Axon.Ipc.newComponent(*(self.children))
        while 1:
           self.pause()
           yield 1

   harness = testComponent()
   harness.activate()
   scheduler.run.runThreads(slowmo=0.1)

if __name__=="__main__":

    tests()
     
