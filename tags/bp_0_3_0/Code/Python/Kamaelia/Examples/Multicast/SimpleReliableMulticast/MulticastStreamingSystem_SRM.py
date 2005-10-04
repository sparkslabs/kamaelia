#!/usr/bin/python
#
# This is a modification to the multicast streaming system that uses the
# SimpleReliableMulticast protocol, to add a thin skein of reliability over
# multicast. Passes basic lab tests, but needs real world testing to be
# certain.
#

from Axon.Component import component
from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.vorbisDecodeComponent import VorbisDecode, AOAudioPlaybackAdaptor
from Kamaelia.Util.ConsoleEcho import consoleEchoer
from Kamaelia.Util.Chargen import Chargen
from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Protocol.SimpleReliableMulticast import SRM_Sender, SRM_Receiver

file_to_stream = "/usr/share/wesnoth/music/wesnoth-1.ogg"

#
# This needs to be moved into a standard area
#
class detuple(component):
   def __init__(self, index):
      super(detuple, self).__init__()
      self.index = index
   def main(self):
      while 1:
         if self.dataReady("inbox"):
            tuple=self.recv("inbox")
            self.send(tuple[self.index], "outbox")
         yield 1

#
# This needs to be refactored out
#
class blockise(component):
    def main(self):
       maxlen = 1000 # Needs to be parameterisable
       buffer = ""
       while 1:
           if self.dataReady("inbox"):
               buffer = buffer + self.recv("inbox")
               if len(buffer) > maxlen:
                  send = buffer[:maxlen]
                  buffer = buffer[maxlen:]
               else:
                  send = buffer
                  buffer = ""
               self.send(send, "outbox")
           yield 1

#
# Server with simple added reliabilty protocol
# 
pipeline(
    ReadFileAdaptor(file_to_stream, readmode="bitrate", bitrate=400000, chunkrate=50),
    SRM_Sender(),
    blockise(), # Ensure chunks small enough for multicasting!
    Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600),
).activate()

#
# Client with simple added reliability protocol
#
pipeline(
    Multicast_transceiver("0.0.0.0", 1600, "224.168.2.9", 0),
    detuple(1),
    SRM_Receiver(),
    detuple(1),
    VorbisDecode(),
    AOAudioPlaybackAdaptor(),
).run()
