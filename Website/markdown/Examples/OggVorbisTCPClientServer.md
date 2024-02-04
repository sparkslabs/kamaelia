---
pagename: Examples/OggVorbisTCPClientServer
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Cookbook Example]{style="font-size:24pt;font-weight:600"}

[How can I\...?]{style="font-size:18pt"}

Example 2: A Simple TCP Based Server that allows multiple connections at
once, but sends a random ogg vorbis file to the client. Includes a
simple TCP based client for this server, that connects to the server,
decodes the ogg vorbis audio and plays it back. [Components used:
]{style="font-weight:600"}[pipeline](/Components/pydoc/Kamaelia.Util.PipelineComponent.pipeline.html),
[SimpleServer](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.SimpleServer.html),
[ReadFileAdaptor](/Components/pydoc/Kamaelia.ReadFileAdaptor.ReadFileAdaptor.html),
[TCPClient](/Components/pydoc/Kamaelia.Internet.TCPClient.TCPClient.html),
[VorbisDecode](/Components/pydoc/Kamaelia.vorbisDecodeComponent.VorbisDecode.html),
[AOAudioPlaybackAdaptor](/Components/pydoc/Kamaelia.vorbisDecodeComponent.AOAudioPlaybackAdaptor.html)

```{.python}
#!/usr/bin/python

from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.SimpleServerComponent import SimpleServer
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.vorbisDecodeComponent import VorbisDecode, AOAudioPlaybackAdaptor

import Kamaelia.ReadFileAdaptor

file_to_stream = "/usr/share/wesnoth/music/wesnoth-1.ogg"

clientServerTestPort=1500

def AdHocFileProtocolHandler(filename):
    class klass(Kamaelia.ReadFileAdaptor.ReadFileAdaptor):
        def __init__(self,*argv,**argd):
            super(klass,self).__init__(filename, readmode="bitrate", bitrate=400000)
    return klass


server=SimpleServer(protocol=AdHocFileProtocolHandler(file_to_stream),
                    port=clientServerTestPort).activate()

pipeline(
   TCPClient("127.0.0.1",clientServerTestPort),
   VorbisDecode(),
   AOAudioPlaybackAdaptor()
).run()
```

**Source:**
Examples/example2/SimpleStreamingSystem.py
