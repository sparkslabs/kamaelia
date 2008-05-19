#!/usr/bin/python

from Kamaelia.Chassis.Pipeline import pipeline
from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Codec.RawYUVFramer import RawYUVFramer
from Kamaelia.Codec.Dirac import DiracEncoder, DiracDecoder
from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay

# Download and build dirac first!
#
# Get the source raw video file (in rgb format) from here, and gunzip it:
# http://sourceforge.net/project/showfiles.php?group_id=102564&package_id=119507
#
# To convert RGB to YUV:
#   RGBtoYUV420 snowboard-jum-352x288x75.rgb snowboard-jum-352x288x75.yuv 352 288 75
#
# Alternatively, source your own AVI file and convert with:
#   ffmpeg -i file_from_digital_camera.avi rawvideo.yuv
#
# and alter the config below as required.

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
