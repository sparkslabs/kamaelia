#!/usr/bin/python
#
# Basic acceptance test harness for the Multicast_sender and receiver
# components.
#

import socket
import Axon

file_to_stream = "/home/zathras/Documents/Music/PopularClassics/3/audio_09.ogg"

class detuple(Axon.Component.component):
   def __init__(self, index):
      self.__super.__init__()
      self.index = index
   def main(self):
      while 1:
         if self.dataReady("inbox"):
            tuple=self.recv("inbox")
            self.send(tuple[self.index], "outbox")
         yield 1

def tests():
   from Axon.Scheduler import scheduler
   import Kamaelia.ReadFileAdaptor
   from Kamaelia.vorbisDecodeComponent import VorbisDecode, AOAudioPlaybackAdaptor


   from Kamaelia.Util.ConsoleEcho import consoleEchoer
   from Kamaelia.Util.Chargen import Chargen

   from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver

   class testComponent(Axon.Component.component):
      def main(self):
        source = Kamaelia.ReadFileAdaptor.ReadFileAdaptor(file_to_stream, 
                                                          readmode="bitrate",
                                                          bitrate=400000,
                                                          chunkrate=50)
        sender   = Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600)
        receiver = Multicast_transceiver("0.0.0.0", 1600, "224.168.2.9", 0)
        detupler = detuple(1)
        decoder = VorbisDecode()
        player = AOAudioPlaybackAdaptor()

        self.link((source,"outbox"), (sender,"inbox"))

        self.link((receiver,"outbox"), (detupler,"inbox"))
        self.link((detupler,"outbox"), (decoder,"inbox"))
        self.link((decoder,"outbox"), (player,"inbox"))

        self.addChildren(source, sender, receiver, detupler, decoder, player)
        yield Axon.Ipc.newComponent(*(self.children))
        while 1:
           yield 1

   harness = testComponent()
   harness.activate()
   scheduler.run.runThreads(slowmo=0)

if __name__=="__main__":

    tests()
     