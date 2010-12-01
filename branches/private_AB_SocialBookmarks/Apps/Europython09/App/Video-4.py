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


