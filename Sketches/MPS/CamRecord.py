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

def mprint(*args):
    print "VideoCapturePlayer", " ".join([str(x) for x in args])

class VideoCapturePlayer(object):
    displaysize = (1024, 768)
    capturesize = ( 640, 480 )
    mirror = True
    delay = 0
    def __init__(self, **argd):
        self.__dict__.update(**argd)
        super(VideoCapturePlayer, self).__init__(**argd)
        self.display = pygame.display.set_mode( self.displaysize )
        self.camera = X=pygame.camera.Camera("/dev/video0", self.capturesize)
        self.camera.start()
        self.camera2 = X=pygame.camera.Camera("/dev/video1", self.capturesize)
        self.camera2.start()

    def get_and_flip(self):
        snapshot = self.camera.get_image()
        snapshot2 = self.camera2.get_image()
        print snapshot, snapshot2
        snapshot = pygame.transform.scale(snapshot,(352,288))
        snapshot2 = pygame.transform.scale(snapshot2,(352,288))
#        snapshot = pygame.transform.scale(snapshot,(512,384))
#        snapshot = pygame.transform.scale(snapshot,(1024,768))
        if 0:
#        if self.mirror:
            flippedx = pygame.transform.flip(snapshot,1,0)
            flippedy = pygame.transform.flip(snapshot,0,1)
            flippedxy = pygame.transform.flip(snapshot,1,1)
#        self.display.blit(flippedy, (0,384))
#        self.display.blit(flippedxy, (512,384))
        self.display.blit(snapshot, (0,0))
        self.display.blit(snapshot2, (0,384))
#        self.display.blit(flippedx, (512,0))
        pygame.display.flip()

    def main(self):
        while 1:
            time.sleep(self.delay)
            self.get_and_flip()

if 1:
    VideoCapturePlayer().main()


class VideoCapturePlayer(Axon.ThreadedComponent.threadedcomponent):
    displaysize = (1024, 768)
    capturesize = ( 320, 240 )
    mirror = True
    delay = 0
    def __init__(self, **argd):
        super(VideoCapturePlayer, self).__init__(**argd)
        self.display = pygame.display.set_mode( self.displaysize )
        self.camera = X=pygame.camera.Camera("/dev/video0", self.capturesize)
        self.camera.start()

    def pygame_display_flip(self):
        pygame.display.flip()

    def get_and_flip(self):
        snapshot = self.camera.get_image()
        snapshot = pygame.transform.scale(snapshot,(512,384))
        if self.mirror:
            flippedx = pygame.transform.flip(snapshot,1,0)
            flippedy = pygame.transform.flip(snapshot,0,1)
            flippedxy = pygame.transform.flip(snapshot,1,1)
        self.display.blit(flippedy, (0,384))
        self.display.blit(flippedxy, (512,384))
        self.display.blit(snapshot, (0,0))
        self.display.blit(flippedx, (512,0))
        self.pygame_display_flip()

    def main(self):
        while 1:
            time.sleep(self.delay)
            self.get_and_flip()

class VideoCaptureSource(Axon.ThreadedComponent.threadedcomponent):
    capturesize = ( 640, 480 )
    mirror = True
    delay = 0
    fps = -1
    def __init__(self, **argd):
        super(VideoCaptureSource, self).__init__(**argd)
        self.camera = X=pygame.camera.Camera("/dev/video0", self.capturesize)
        self.camera.start()
        if self.fps != -1:
            self.delay = 1.0/self.fps # fps overrides delay

    def capture_one(self):
        snapshot = self.camera.get_image()
        if self.mirror:
            snapshot = pygame.transform.flip(snapshot,1,0)
        return snapshot

    def main(self):
        while 1:
            self.send(self.capture_one(), "outbox")
            time.sleep(self.delay) # This would be far better to be a synchronous link


# This doesn't play nicely yet. 
# It will
class SurfaceDisplayer(Axon.Component.component):
    displaysize = (800, 600)
    def __init__(self, **argd):
        super(SurfaceDisplayer, self).__init__(**argd)
        self.display = pygame.display.set_mode( self.displaysize )

    def pygame_display_flip(self):
        pygame.display.flip()

    def main(self):
        while 1:
            while self.dataReady("inbox"):
                snapshot = self.recv("inbox")
                self.display.blit(snapshot, (80,60))
                self.pygame_display_flip()
            while not self.anyReady():
                self.pause()
                yield 1
            yield 1

#
# This plays nicely with pygame display
#
from Kamaelia.UI.GraphicDisplay import PygameDisplay
class ProperSurfaceDisplayer(Axon.Component.component):
    Inboxes = ["inbox", "control", "callback"]
    Outboxes= ["outbox", "signal", "display_signal"]
    displaysize = (640, 480)
    def __init__(self, **argd):
        super(ProperSurfaceDisplayer, self).__init__(**argd)
        self.disprequest = { "DISPLAYREQUEST" : True,
                           "callback" : (self,"callback"),
                           "size": self.displaysize}

    def pygame_display_flip(self):
        self.send({"REDRAW":True, "surface":self.display}, "display_signal")

    def getDisplay(self):
       displayservice = PygameDisplay.getDisplayService()
       self.link((self,"display_signal"), displayservice)
       self.send(self.disprequest, "display_signal")
       while not self.dataReady("callback"):
           self.pause()
           yield 1
       self.display = self.recv("callback")

    def main(self):
       yield Axon.Ipc.WaitComplete(self.getDisplay())
       time.sleep(1)
       if 1:
         while 1:
            while self.dataReady("inbox"):
                snapshot = self.recv("inbox")
                self.display.blit(snapshot, (0,0))
                self.pygame_display_flip()
            while not self.anyReady():
                self.pause()
                yield 1
            yield 1


class VideoCaptureSource(Axon.ThreadedComponent.threadedcomponent):
    capturesize = ( 640, 480 )
    mirror = True
    delay = 0
    fps = -1
    def __init__(self, **argd):
        super(VideoCaptureSource, self).__init__(**argd)
        self.camera = X=pygame.camera.Camera("/dev/video0", self.capturesize)
        self.camera.start()
        if self.fps != -1:
            self.delay = 1.0/self.fps # fps overrides delay

    def capture_one(self):
        snapshot = self.camera.get_image()
        if self.mirror:
            snapshot = pygame.transform.flip(snapshot,1,0)
        return snapshot

    def main(self):
        t = time.time()
        c = 0
        while 1:
            tn =time.time()
            self.safeSend((tn, self.capture_one()), "outbox")
            c +=1
            if tn - t > 1:
                td = tn -t
                t = tn
                print "FPS", c
                c =0
#            time.sleep(self.delay) # This would be far better to be a synchronous link
    def safeSend(self, data, box):
        while 1:
            try:
                self.send(data,box)
#                print "SENT", data
                return
            except Axon.AxonExceptions.noSpaceInBox:
                pass
#                print "MISS", data
            self.pause()



class ProperSurfaceDisplayer(Axon.Component.component):
    Inboxes = ["inbox", "control", "callback"]
    Outboxes= ["outbox", "signal", "display_signal"]
    displaysize = (640, 480)
    def __init__(self, **argd):
        super(ProperSurfaceDisplayer, self).__init__(**argd)
        self.disprequest = { "DISPLAYREQUEST" : True,
                           "callback" : (self,"callback"),
                           "size": self.displaysize}

    def pygame_display_flip(self):
        self.send({"REDRAW":True, "surface":self.display}, "display_signal")

    def getDisplay(self):
       displayservice = PygameDisplay.getDisplayService()
       self.link((self,"display_signal"), displayservice)
       self.send(self.disprequest, "display_signal")
       while not self.dataReady("callback"):
           self.pause()
           yield 1
       self.display = self.recv("callback")

    def main(self):
#       self.inboxes["inbox"].setSize(1)
       yield Axon.Ipc.WaitComplete(self.getDisplay())
       time.sleep(1)
       if 1:
         while 1:
            while self.dataReady("inbox"):
                t,snapshot = self.recv("inbox")
                snapshot=snapshot.convert()
                self.display.blit(snapshot, (0,0))
                self.pygame_display_flip()
            while not self.anyReady():
                self.pause()
                yield 1
            yield 1


if 0:
    VideoCapturePlayer().run() # Runs at full speed - basic test case

if 1:
    print "Hello World"
    sys.path.append("/home/zathras/kamaelia/trunk/Sketches/MH/pixformatConversion")
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay
    from VideoSurface import VideoSurface

    class Framer(Axon.Component.component):
        def main(self):
            while 1:
                while self.dataReady("inbox"):
                    D = self.recv("inbox")
                    print D, D[1].get_width(),D[1].get_height(),
                    X = {
                          "yuv" : (D[1], D[1], D[1]),  # a tuple of strings
                          "size" : (D[1].get_width(), D[1].get_width()),          # in pixels
                          "pixformat" :  "YUV420_planar"    # format of raw video data
                        }
                    self.send(X, "outbox")
                yield 1
    X = PygameDisplay(width=640,height=480).activate()
    PygameDisplay.setDisplayService(X)
    Pipeline(
        VideoCaptureSource(fps=32),
#        Framer(),
#        VideoOverlay(),
        ProperSurfaceDisplayer(),
    ).run()

if 1:
    X = VideoCaptureSource(fps=32)
    snap = X.capture_one()

    pygame.image.save(snap, "photo.bmp")
#    pygame.image.save(snap, "photo.png")
