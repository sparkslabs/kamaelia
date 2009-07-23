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

from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Codec.Dirac import DiracEncoder
from Kamaelia.Video.PixFormatConversion import ToYUV420_planar
from Kamaelia.Util.PureTransformer import PureTransformer

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


