#!/usr/bin/python

#
# This import line is required to pull in pygame.camera support
#
import sys ; 
sys.path.insert(0, "/home/zathras/Documents/pygame-1.9.0rc1/build/lib.linux-i686-2.5")

import time
import pygame
import pygame.camera

import Axon
import Image # PIL - Python Imaging Library

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Codec.Dirac import DiracEncoder, DiracDecoder
from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay
from Kamaelia.Video.PixFormatConversion import ToYUV420_planar
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Util.PureTransformer import PureTransformer

pygame.init()
pygame.camera.init()

class VideoCapturePlayer(Axon.ThreadedComponent.threadedcomponent):
    displaysize = (1024, 768)
    capturesize = ( 640, 480 )
    mirror = True
    delay = 1/24.0
    def __init__(self, **argd):
        self.__dict__.update(**argd)
        super(VideoCapturePlayer, self).__init__(**argd)
        self.display = pygame.display.set_mode( self.displaysize )
        self.camera = X=pygame.camera.Camera("/dev/video0", (352,288))
        self.camera.start()
        self.snapshot = None

    def get_and_flip(self):
        self.snapshot = None
        self.snapshot = self.camera.get_image()

    def main(self):
        c = 0
        tfr = 15.0
        Itfr = int((tfr/2)+0.5)
        tfrU = tfr + 0.05
        tfrL = tfr - 0.05
        d = 1/tfr
        fudge = 0
        ts = t = time.time()

        while 1:
            self.get_and_flip()
            t2 = time.time()

            dt = t2-t
            d = 1/tfr
            s = d - dt + fudge
            if s<0: 
               s=0.0                 
            
            time.sleep(s)
            self.send((t2,self.snapshot), "outbox")
            t = time.time()         
            c += 1
            if (c % Itfr) ==0:
               f= c/(t2-ts)
               print "framerate", f,"cpu", dt, "target", d, "sleep",s 
               if f>tfrU:
                   fudge += 0.001
               if f<tfrU:
                   fudge -= 0.001

Pipeline(
    VideoCapturePlayer(),
    PureTransformer(lambda (i,F) : {
                            "rgb" : pygame.image.tostring(F, "RGB"),
                            "size" : (352, 288),
                            "pixformat" : "RGB_interleaved",
                          }),
    ToYUV420_planar(),
    DiracEncoder(preset="CIF",  encParams={"num_L1":0}),
    SimpleFileWriter("X.drc"),
).run()
