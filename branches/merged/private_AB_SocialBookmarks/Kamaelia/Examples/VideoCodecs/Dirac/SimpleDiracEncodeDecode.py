#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
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

Pipeline( ReadFileAdaptor(FILENAME, readmode="bitrate", bitrate= 1000000),
          RawYUVFramer( size=SIZE ),
          DiracEncoder(preset=DIRACPRESET, encParams=ENCPARAMS ),
          DiracDecoder(),
          VideoOverlay()
        ).run()
