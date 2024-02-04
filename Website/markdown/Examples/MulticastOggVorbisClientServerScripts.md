---
pagename: Examples/MulticastOggVorbisClientServerScripts
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Cookbook Example]{style="font-size:24pt;font-weight:600"}

[How can I\...?]{style="font-size:18pt"}

Example 4: Building a very simplistic multicast based streaming system
using ogg vorbis. This time using 2 separate scripts. [Components used
in server script:
]{style="font-weight:600"}[component]{style="font-style:italic;color:#ff0004"},
[ReadFileAdaptor](/Components/pydoc/Kamaelia.ReadFileAdaptor.ReadFileAdaptor.html),
[Multicast\_transceiver](/Components/pydoc/Kamaelia.Internet.Multicast_transceiver.Multicast_transceiver.html).
[Components used in client script:]{style="font-weight:600"}
[component]{style="font-style:italic;color:#ff0004"},
[Multicast\_transceiver](/Components/pydoc/Kamaelia.Internet.Multicast_transceiver.Multicast_transceiver.html),
[detuple]{style="font-style:italic;color:#ff0004"} (defined in the
example),
[VorbisDecode](/Components/pydoc/Kamaelia.vorbisDecodeComponent.VorbisDecode.html),
[AOAudioPlaybackAdaptor](/Components/pydoc/Kamaelia.vorbisDecodeComponent.AOAudioPlaybackAdaptor.html).

### Server Script, the easy way

```{.python}
#!/usr/bin/python

from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver
from Kamaelia.Util.PipelineComponent import pipeline

file_to_stream = "/usr/share/wesnoth/music/wesnoth-1.ogg"

pipeline(
    ReadFileAdaptor(file_to_stream, readmode="bitrate", bitrate=400000, chunkrate=50),
    Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600),
).run()
```

### Server Script, the hard way (but exactly equivalent)

```{.python}
#!/usr/bin/python

import Axon

file_to_stream = "/usr/share/wesnoth/music/wesnoth-1.ogg"

def tests():
   from Axon.Scheduler import scheduler
   import Kamaelia.ReadFileAdaptor
   from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver

   class testComponent(Axon.Component.component):
      def main(self):
        source = Kamaelia.ReadFileAdaptor.ReadFileAdaptor(file_to_stream,
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
```

**Source:** Examples/example4/MulticastStreamingServer.py


### Client Script

```{.python}
#!/usr/bin/python

from Axon.Component import component
from Kamaelia.vorbisDecodeComponent import VorbisDecode, AOAudioPlaybackAdaptor
from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver
from Kamaelia.Util.PipelineComponent import pipeline

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

# Client
pipeline(
    Multicast_transceiver("0.0.0.0", 1600, "224.168.2.9", 0),
    detuple(1),
    VorbisDecode(),
    AOAudioPlaybackAdaptor(),
).run()
```

## Client Script, the hard way (but exactly equivalent)

```{.python}
#!/usr/bin/python

import Axon

class detuple(Axon.Component.component):
   def __init__(self, index):
      super(detuple,self).__init__()
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
   from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver

   class testComponent(Axon.Component.component):
      def main(self):
        receiver = Multicast_transceiver("0.0.0.0", 1600, "224.168.2.9", 0)
        detupler = detuple(1)
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
```

**Source:** Examples/example4/MulticastStreamingClient.py

