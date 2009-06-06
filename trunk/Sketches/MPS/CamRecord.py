#!/usr/bin/python

#
# This import line is required to pull in pygame.camera support
#
import sys ; sys.path.insert(0, "/home/zathras/Incoming/X/pygame/pygame-nrp/build/lib.linux-i686-2.5")
import time
import pygame
import pygame.camera

import Axon

pygame.init()

class VideoCapturePlayer(Axon.ThreadedComponent.threadedcomponent):
    displaysize = (1024, 768)
    capturesize = ( 640, 480 )
    mirror = True
    delay = 0
    camera = "/dev/video1"
    imagesize = (352,288)
    def __init__(self, **argd):
        self.__dict__.update(**argd)
        super(VideoCapturePlayer, self).__init__(**argd)
        self.camera = X=pygame.camera.Camera(self.camera, self.capturesize)
        self.camera.start()

    def get_and_flip(self):
        snapshot = self.camera.get_image()
        if self.imagesize:
            snapshot = pygame.transform.scale(snapshot,self.imagesize)
        self.send(snapshot, "outbox")

    def main(self):
        while 1:
            time.sleep(self.delay)
            self.get_and_flip()

class SurfaceDisplayer(Axon.Component.component):
    displaysize = (800, 600)
    def __init__(self, **argd):
        super(SurfaceDisplayer, self).__init__(**argd)
        self.display = pygame.display.set_mode( self.displaysize )

    def pygame_display_flip(self):
        pygame.display.flip()

    def main(self):
        while 1:
            snapshot = None
            for snapshot in self.Inbox("inbox"):
                pass
            if snapshot:
                self.display.blit(snapshot, (80,60))
                self.pygame_display_flip()

            while not self.anyReady():
                self.pause()
                yield 1
            yield 1

class PicSaver(Axon.Component.component):
    base = "vid/"
    def main(self):
        base = self.base
        while 1:
            snapshot = None
            for snapshot in self.Inbox("inbox"):
                pass
            if snapshot:
                filename = base + str(self.scheduler.time)+".jpg"
                pygame.image.save(snapshot, filename)
            while not self.anyReady():
                self.pause()
                yield 1
            yield 1


from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Apps.Whiteboard.TwoWaySplitter import TwoWaySplitter
from Kamaelia.Util.PureTransformer import PureTransformer


if 0:
    Graphline(
        SOURCE = VideoCapturePlayer(),
        SPLIT = TwoWaySplitter(),
        DISPLAY = SurfaceDisplayer(),
        FILE = PicSaver(),
        linkages = {
            ("SOURCE", "outbox") : ("SPLIT", "inbox"),
            ("SPLIT", "outbox") : ("DISPLAY", "inbox"),
            ("SPLIT", "outbox2") : ("FILE", "inbox"),
        }
    ).run()


if 1:
    Pipeline(
        VideoCapturePlayer(),
        PicSaver(base="vid/"),
    ).run()
