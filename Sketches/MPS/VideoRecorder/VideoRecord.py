#!/usr/bin/python

#
# This import line is required to pull in pygame.camera support
#
import sys ; 
#sys.path.insert(0, "/home/zathras/Incoming/X/pygame/pygame-nrp/build/lib.linux-i686-2.5")
sys.path.insert(0, "/home/zathras/code.google/pygame-seul/trunk/build/lib.linux-i686-2.5")
sys.path.insert(0, "/home/zathras/Documents/pygame-1.9.0rc1/build/lib.linux-i686-2.5")

import time
import pygame
import pygame.camera

import Axon
import Image
pygame.init()
pygame.camera.init()


if 0:
    display = pygame.display.set_mode( (1024, 768) )
    camera = pygame.camera.Camera("/dev/video0", ( 640, 480 ) )
    camera.start()
    snapshot = camera.get_image()
    X =snapshot.get_buffer()
    width, height = snapshot.get_size()

    print X.length, width, height

def save_raw(snapshot,i):
    X = snapshot.get_buffer()
    im = Image.frombuffer("RGB", snapshot.get_size(), X.raw, "raw", "RGB", 0, 1)
    F = "vid/"+str(i)+".png"
    print "F",F
    im.save(F)

 
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


class Mangler(Axon.Component.component):
    def main(self):
        while True:
            i = None
            for (i,F) in self.Inbox("inbox"): # Only try to get the last frame (for now)
              if i is not None:
                X = pygame.image.tostring(F, "RGB")
                self.send( {
                            "rgb" : X,
                            "size" : (352, 288),
                            "pixformat" : "RGB_interleaved",
                           }, "outbox")

            if not self.anyReady():
                self.pause()
            yield 1
        

class FileDump(Axon.Component.component):
    def main(self):
        f = open("X.drc","wb")
#        if 1:
        try:
            while True:
                for i in self.Inbox("inbox"):
                    f.write(i)
                yield 1
                if not self.anyReady():
                    self.pause()
        except:
            f.close()

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Codec.Dirac import DiracEncoder, DiracDecoder
from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay
from Kamaelia.Video.PixFormatConversion import ToYUV420_planar

Pipeline(
    VideoCapturePlayer(),
    Mangler(),
    ToYUV420_planar(),
    DiracEncoder(preset="CIF",  encParams={"num_L1":0}),
#    DiracDecoder(),
#    VideoOverlay()
    FileDump(),
).run()





