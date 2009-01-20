#!/usr/bin/python
#
# Basic acceptance test harness for the Multicast_sender and receiver
# components.
#

import Axon

file_to_stream = "../../SupportingMediaFiles/KDE_Startup_2.ogg"

def tests():
   from Axon.Scheduler import scheduler
   import Kamaelia.File.ReadFileAdaptor
   from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver

   class testComponent(Axon.Component.component):
      def main(self):
        source = Kamaelia.File.ReadFileAdaptor.ReadFileAdaptor(file_to_stream, 
                                                          readmode="bitrate",
                                                          bitrate=400000,
                                                          chunkrate=50)
        sender   = Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600)
        self.link((source,"outbox"), (sender,"inbox"))

        self.addChildren(source, sender)
        yield Axon.Ipc.newComponent(*(self.children))
        while 1:
           yield 1

   harness = testComponent()
   harness.activate()
   scheduler.run.runThreads(slowmo=0)

if __name__=="__main__":

    tests()
     