---
pagename: Examples/IntrospectingASimpleStreamingSystem
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Cookbook Example]{style="font-size:24pt;font-weight:600"}

[How can I\...?]{style="font-size:18pt"}

Example 5: An introspecting version of Examples 2/3. This creates a
simple streaming system, and looks inside to see what components are
running/active, and passes the resulting information over a network
connection to an Axon Visualisation server. [Components used:
]{style="font-weight:600"}[SimpleServer](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.SimpleServer.html),
[TCPClient](/Components/pydoc/Kamaelia.Internet.TCPClient.TCPClient.html),
[ReadFileAdaptor](/Components/pydoc/Kamaelia.ReadFileAdaptor.ReadFileAdaptor.html),
[VorbisDecode](/Components/pydoc/Kamaelia.vorbisDecodeComponent.VorbisDecode.html),
[AOAudioPlaybackAdaptor](/Components/pydoc/Kamaelia.vorbisDecodeComponent.AOAudioPlaybackAdaptor.html),
[Introspector](/Components/pydoc/Kamaelia.Util.Introspector.Introspector.html)

```{.python}
#!/usr/bin/python

from Kamaelia.SimpleServerComponent import SimpleServer
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.vorbisDecodeComponent import VorbisDecode, AOAudioPlaybackAdaptor
from Kamaelia.Util.PipelineComponent import pipeline
import Kamaelia.ReadFileAdaptor
# This next line is new
from Kamaelia.Util.Introspector import Introspector

file_to_stream = "/usr/share/wesnoth/music/wesnoth-1.ogg"
clientServerTestPort = 1501

def AdHocFileProtocolHandler(filename):
    class klass(Kamaelia.ReadFileAdaptor.ReadFileAdaptor):
        def __init__(self,*argv,**argd):
            super(klass,self).__init__(filename, readmode="bitrate", bitrate=400000)
    return klass

# Start the server
SimpleServer(protocol=AdHocFileProtocolHandler(file_to_stream),
             port=clientServerTestPort).activate()

# Start the client
pipeline(
      TCPClient("127.0.0.1",clientServerTestPort),
      VorbisDecode(),
      AOAudioPlaybackAdaptor(),
).activate()

# This next pipeline is new
# Start the introspector and connect to a local visualiser
pipeline(
    Introspector(),
    TCPClient("127.0.0.1", 1500),
).run()
```

**Source:** Examples/example5/IntrospectingSimpleStreamingSystem.py
