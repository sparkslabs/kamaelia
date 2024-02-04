---
pagename: Examples/MulticastOggVorbisServer
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Cookbook Example]{style="font-size:24pt;font-weight:600"}

[How can I\...?]{style="font-size:18pt"}

Example 4: Building a very simplistic multicast based streaming system
using ogg vorbis. [Components used:
]{style="font-weight:600"}[component]{style="font-style:italic;color:#ff0004"},
[ReadFileAdaptor](/Components/pydoc/Kamaelia.ReadFileAdaptor.ReadFileAdaptor.html),
[VorbisDecode](/Components/pydoc/Kamaelia.vorbisDecodeComponent.VorbisDecode.html),
[AOAudioPlaybackAdaptor](/Components/pydoc/Kamaelia.vorbisDecodeComponent.AOAudioPlaybackAdaptor.html),
[Multicast\_transceiver](/Components/pydoc/Kamaelia.Internet.Multicast_transceiver.Multicast_transceiver.html),
[pipeline](/Components/pydoc/Kamaelia.Util.PipelineComponent.pipeline.html)


```{.python}
#!/usr/bin/python

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
```

**Source:** Examples/example4/MulticastStreamingSystem.py
