#!/usr/bin/python
#
# Basic acceptance test harness for the Multicast_sender and receiver
# components.
#

from Axon.Component import component
from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.vorbisDecodeComponent import VorbisDecode, AOAudioPlaybackAdaptor
from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver
from Kamaelia.Util.PipelineComponent import pipeline

file_to_stream = "/usr/share/wesnoth/music/wesnoth-1.ogg"

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

# Server
pipeline(
    ReadFileAdaptor(file_to_stream, readmode="bitrate", bitrate=400000, chunkrate=50),
    Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600),
).activate()

# Client
pipeline(
    Multicast_transceiver("0.0.0.0", 1600, "224.168.2.9", 0),
    detuple(1),
    VorbisDecode(),
    AOAudioPlaybackAdaptor(),
).run()
