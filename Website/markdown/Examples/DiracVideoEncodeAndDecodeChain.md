---
pagename: Examples/DiracVideoEncodeAndDecodeChain
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Cookbook Example]{style="font-size:24pt;font-weight:600"}

[How can I\...?]{style="font-size:18pt"}

Example 10: Simple dirac encoder/decoder. Shows how to read raw video
frames from a file, encode them using dirac, decode them again, and then
playback via a video overlay. [Components used:
]{style="font-weight:600"}[ReadFileAdaptor](/Components/pydoc/Kamaelia.ReadFileAdaptor.ReadFileAdaptor.html),
[RawYUVFramer](/Components/pydoc/Kamaelia.Codec.RawYUVFramer.RawYUVFramer.html),
[DiracEncoder](/Components/pydoc/Kamaelia.Codec.Dirac.DiracEncoder.html),
[DiracDecoder](/Components/pydoc/Kamaelia.Codec.Dirac.DiracDecoder.html),
[VideoOverlay](/Components/pydoc/Kamaelia.UI.Pygame.VideoOverlay.VideoOverlay.html)
.

Download and build dirac first!

Get the source raw video file (in rgb format) from here, and gunzip it:

<http://sourceforge.net/project/showfiles.php?group_id=102564&package_id=119507>

To convert RGB to YUV:

```
RGBtoYUV420 snowboard-jum-352x288x75.rgb snowboard-jum-352x288x75.yuv 352 288 75
```

Alternatively, source your own AVI file and convert with:

```
ffmpeg -i file_from_digital_camera.avi rawvideo.yuv
```

and alter the config below as required.

```{.python}
#!/usr/bin/python

from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Codec.RawYUVFramer import RawYUVFramer
from Kamaelia.Codec.Dirac import DiracEncoder, DiracDecoder
from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay

FILENAME  = "/data/dirac-video/snowboard-jum-352x288x75.yuv"
SIZE = (352,288)
DIRACPRESET = "CIF"         # dirac resolution and encoder settings preset

# encoder param sets it to iframe only (no motion based coding, faster)
# (overrides preset)
ENCPARAMS = {"num_L1":0}

pipeline( ReadFileAdaptor(FILENAME, readmode="bitrate", bitrate= 1000000),
          RawYUVFramer( size=SIZE ),
          DiracEncoder(preset=DIRACPRESET, encParams=ENCPARAMS ),
          DiracDecoder(),
          VideoOverlay()
        ).run()
```

**Source:** Examples/example10/SimpleDiracEncodeDecode.py
