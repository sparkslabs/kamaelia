#!/usr/bin/python

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