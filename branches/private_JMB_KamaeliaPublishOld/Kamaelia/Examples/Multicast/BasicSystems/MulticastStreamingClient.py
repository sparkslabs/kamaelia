#!/usr/bin/python
#
# Basic acceptance test harness for the Multicast_sender and receiver
# components.
#

import Axon
from Kamaelia.Util.Detuple import SimpleDetupler

def tests():
   from Axon.Scheduler import scheduler
   import Kamaelia.File.ReadFileAdaptor
   from Kamaelia.Codec.Vorbis import VorbisDecode, AOAudioPlaybackAdaptor

   from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver

   class testComponent(Axon.Component.component):
      def main(self):
        receiver = Multicast_transceiver("0.0.0.0", 1600, "224.168.2.9", 0)
        detupler = SimpleDetupler(1)
        decoder = VorbisDecode()
        player = AOAudioPlaybackAdaptor()

        self.link((receiver,"outbox"), (detupler,"inbox"))
        self.link((detupler,"outbox"), (decoder,"inbox"))
        self.link((decoder,"outbox"), (player,"inbox"))

        self.addChildren(receiver, detupler, decoder, player)
        yield Axon.Ipc.newComponent(*(self.children))
        while 1:
           yield 1

   harness = testComponent()
   harness.activate()
   scheduler.run.runThreads(slowmo=0)

if __name__=="__main__":

    tests()
     