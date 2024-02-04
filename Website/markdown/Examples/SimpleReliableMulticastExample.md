---
pagename: Examples/SimpleReliableMulticastExample
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Cookbook Example]{style="font-size:24pt;font-weight:600"}

[How can I\...?]{style="font-size:18pt"}

Example 4: Building some reliability into the system ([Simple Reliable
Multicast](/SimpleReliableMulticast.html)). Idea is to show layering of
protocols.[ Components used:
]{style="font-weight:600"}[component]{style="font-style:italic;color:#ff0004"},
[ReadFileAdaptor](/Components/pydoc/Kamaelia.ReadFileAdaptor.ReadFileAdaptor.html),
[VorbisDecode](/Components/pydoc/Kamaelia.vorbisDecodeComponent.VorbisDecode.html),
[AOAudioPlaybackAdaptor](/Components/pydoc/Kamaelia.vorbisDecodeComponent.AOAudioPlaybackAdaptor.html),
[Multicast\_transceiver](/Components/pydoc/Kamaelia.Internet.Multicast_transceiver.Multicast_transceiver.html),
[pipeline](/Components/pydoc/Kamaelia.Util.PipelineComponent.pipeline.html),
[SRM\_Sender]{style="font-style:italic;color:#ff0004"},
[SRM\_Receiver]{style="font-style:italic;color:#ff0004"}

```{.python}
#!/usr/bin/python

from Axon.Component import component
from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.vorbisDecodeComponent import VorbisDecode, AOAudioPlaybackAdaptor
from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Protocol.SimpleReliableMulticast import SRM_Sender, SRM_Receiver

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

```

**Source:** Examples/example4/MulticastStreamingSystem_SRM.py

