#!/usr/bin/python

# To use pygame alpha
import sys ;
sys.path.insert(0, "/home/zathras/Documents/pygame-1.9.0rc1/build/lib.linux-i686-2.5")

import time
import pygame
import pygame.camera
from Axon.ThreadedComponent import threadedcomponent
from Axon.Component import component
from Kamaelia.Chassis.Pipeline import Pipeline

pygame.init()
pygame.camera.init()

class VideoCaptureSource(threadedcomponent):
  capturesize = (352, 288)
  delay = 0
  fps = -1
  device = "/dev/video0"

  def __init__(self, **argd):
    super(VideoCaptureSource, self).__init__(**argd)
    self.camera = pygame.camera.Camera(self.device,
                                       self.capturesize)
    self.camera.start()
    if self.fps != -1:
      self.delay = 1.0/self.fps
    self.snapshot = None

  def capture_one(self):
    self.snapshot = None
    self.snapshot = self.camera.get_image()

  def main(self):
    while 1:
      self.capture_one()
      self.send(self.snapshot, "outbox")
      time.sleep(self.delay)


class SurfaceDisplayer(component):
  displaysize = (800,600)
  imagesize = (352, 288)
  imageorigin = (0,0)

  def __init__(self, **argd):
    super(SurfaceDisplayer, self).__init__(**argd)
    self.display = pygame.display.set_mode(self.displaysize)

  def pygame_display_flip(self):
    pygame.display.flip()

  def main(self):
    while 1:
      while self.dataReady("inbox"):
        snapshot = self.recv("inbox")
        snapshot = pygame.transform.scale(snapshot,
                                          self.imagesize)
        self.display.blit(snapshot, self.imageorigin)
        self.pygame_display_flip()
      while not self.anyReady():
        self.pause()
        yield 1
      yield 1

Pipeline(
   VideoCaptureSource(),
   SurfaceDisplayer(),
).run()


