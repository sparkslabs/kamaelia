---
pagename: Examples/SimplestPossibleDiracVideoPlayer
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Cookbook Example]{style="font-size:24pt;font-weight:600"}

[How can I\...?]{style="font-size:18pt"}

Example 10: Simple dirac player. Shows how to play a specific file.
[Components used:
]{style="font-weight:600"}[ReadFileAdaptor](/Components/pydoc/Kamaelia.ReadFileAdaptor.ReadFileAdaptor.html),
[DiracDecoder](/Components/pydoc/Kamaelia.Codec.Dirac.DiracDecoder.html),
[MessageRateLimit](/Components/pydoc/Kamaelia.Util.RateFilter.MessageRateLimit.html),
[VideoOverlay](/Components/pydoc/Kamaelia.UI.Pygame.VideoOverlay.VideoOverlay.html)

```{.python}
#!/usr/bin/python

from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Codec.Dirac import DiracDecoder
from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Util.RateFilter import MessageRateLimit
from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay

file = "snowboard-jum-352x288x75.dirac.drc"
framerate = 15

pipeline(
         ReadFileAdaptor(file, readmode="bitrate",
                         bitrate = 300000*8/5),
         DiracDecoder(),
         MessageRateLimit(framerate),
         VideoOverlay(),
).run()
```

**Source:** Examples/example10/SimpleDiracPlayer.py
