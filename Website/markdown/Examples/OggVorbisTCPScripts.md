---
pagename: Examples/OggVorbisTCPScripts
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Cookbook Example]{style="font-size:24pt;font-weight:600"}

[How can I\...?]{style="font-size:18pt"}

Example 3: Same as example 2, but as separate scripts. [Components used
in server script:]{style="font-weight:600"}
[SimpleServer](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.SimpleServer.html),
[ReadFileAdaptor](/Components/pydoc/Kamaelia.ReadFileAdaptor.ReadFileAdaptor.html).
[Components used in client script:]{style="font-weight:600"}
[pipeline](/Components/pydoc/Kamaelia.Util.PipelineComponent.pipeline.html),
[TCPClient](/Components/pydoc/Kamaelia.Internet.TCPClient.TCPClient.html),
[VorbisDecode](/Components/pydoc/Kamaelia.vorbisDecodeComponent.VorbisDecode.html),
[AOAudioPlaybackAdaptor](/Components/pydoc/Kamaelia.vorbisDecodeComponent.AOAudioPlaybackAdaptor.html)
.

### Server script

```{.python}
#!/usr/bin/python

import Kamaelia.ReadFileAdaptor
from Kamaelia.SimpleServerComponent import SimpleServer

file_to_stream = "/usr/share/wesnoth/music/wesnoth-1.ogg"

def AdHocFileProtocolHandler(filename):
    class klass(Kamaelia.ReadFileAdaptor.ReadFileAdaptor):
        def __init__(self,*argv,**argd):
            super(klass,self).__init__(filename, readmode="bitrate", bitrate=400000)
    return klass

clientServerTestPort=1500
SimpleServer(protocol=AdHocFileProtocolHandler(file_to_stream),
             port=clientServerTestPort).run()
```

**Source:** Examples/example3/SimpleStreamer.py

### Client script

```{.python}
#!/usr/bin/python
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.vorbisDecodeComponent import VorbisDecode, AOAudioPlaybackAdaptor
from Kamaelia.Util.PipelineComponent import pipeline

clientServerTestPort=1500
pipeline(TCPClient("127.0.0.1",clientServerTestPort),
         VorbisDecode(),
         AOAudioPlaybackAdaptor()
        ).run()
```

**Source:** Examples/example3/SimpleStreamingClient.py

