#!/usr/bin/python

# To use pygame alpha
import sys ;
sys.path.insert(0, "/home/zathras/Documents/pygame-1.9.0rc1/build/lib.linux-i686-2.5")

import pygame
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Codec.Dirac import DiracEncoder
from Kamaelia.Video.PixFormatConversion import ToYUV420_planar
from Kamaelia.Util.PureTransformer import PureTransformer

from Kamaelia.Apps.Europython09.VideoCaptureSource import VideoCaptureSource

Pipeline(
   VideoCaptureSource(),
   PureTransformer(lambda F : \
             {"rgb" : pygame.image.tostring(F, "RGB"),
                      "size" : (352, 288),
                      "pixformat" : "RGB_interleaved",
             }),
    ToYUV420_planar(),
    DiracEncoder(preset="CIF",  encParams={"num_L1":0}),
    SimpleFileWriter("X.drc"),
).run()


