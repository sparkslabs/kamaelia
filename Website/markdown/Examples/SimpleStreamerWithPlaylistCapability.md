---
pagename: Examples/SimpleStreamerWithPlaylistCapability
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Cookbook Example]{style="font-size:24pt;font-weight:600"}

[How can I\...?]{style="font-size:18pt"}

Example 12 : Simple TCP based streamer that repeatedly streams (3 times)
the same audio file. The reason it\'s the same file is because it\'s
configured with a playlist that is created: \[ shortfile, shortfile,
shortfile \]. If this was \[ song\_one, song\_two, song\_three \], then
this would be a simple streamer that had a playlist of 3 songs played
repeatedly. Something that does this is often referred to as a carousel.
[Components used:
]{style="font-weight:600"}[SimpleServer](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.SimpleServer.html),
[JoinChooserToCarousel]{style="font-style:italic;color:#ff0004"},
[FixedRateControlledReusableFileReader]{style="font-style:italic;color:#ff0004"},
[ForwardIteratingChooser](/Components/pydoc/Kamaelia.Util.Chooser.ForwardIteratingChooser.html),
[pipeline](/Components/pydoc/Kamaelia.Util.PipelineComponent.pipeline.html)

```{.python}
#!/usr/bin/python

from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Kamaelia.Chassis.Prefab import JoinChooserToCarousel
from Kamaelia.File.Reading import FixedRateControlledReusableFileReader
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Graphline import Graphline
from Kamaelia.Util.Chooser import ForwardIteratingChooser

shortfile = "/opt/kde3/share/sounds/KDE_Startup_2.ogg"

FILES_TO_STREAM = [ shortfile, shortfile, shortfile ]# [  file_to_stream, file_to_stream2 ]
BITRATE         = 800000 # 38000
CHUNKSIZEBYTES  = 512
SERVERPORT      = 1500

def MultiFileReaderProtocol(filenames, bitrate, chunksizebytes):
    def protocolFactory(*argv, **argd):
        return JoinChooserToCarousel(
            ForwardIteratingChooser(filenames),
            FixedRateControlledReusableFileReader(readmode="bytes",
                                               rate=bitrate/8,
                                               chunksize=chunksizebytes)
          )
    return protocolFactory

if __name__ == '__main__':
   filereader = MultiFileReaderProtocol( FILES_TO_STREAM, BITRATE, CHUNKSIZEBYTES)
   server     = SimpleServer( protocol = filereader, port = SERVERPORT ).run()
```

**Source:** Examples/example12/SimpleMultiFileStreamer.py
