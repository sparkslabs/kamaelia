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
import pygame
import pygame.camera
pygame.init()
pygame.camera.init()



class VideoCapturePlayer(object):
  displaysize = (800, 600)
  capturesize = (640, 480)
  imagesize = (352, 288)
  imageorigin = (0,0)
  device = "/dev/video0"

  def __init__(self, **argd):
    self.__dict__.update(**argd)
    super(VideoCapturePlayer,self).__init__(**argd)
    self.display = pygame.display.set_mode(self.displaysize)
    self.camera = pygame.camera.Camera(self.device,
                                  self.capturesize)
    self.camera.start()

  def get_and_flip(self):
    snapshot = self.camera.get_image()
    snapshot = pygame.transform.scale(snapshot,
                                      self.imagesize)
    self.display.blit(snapshot, self.imageorigin)
    pygame.display.flip()

  def main(self):
    while 1:
      self.get_and_flip()


VideoCapturePlayer().main()