#!/usr/bin/python

import pygame
import pygame.camera
pygame.init()
pygame.camera.init()

displaysize = (800, 600)
capturesize = (640, 480)
imagesize = (352, 288)
imageorigin = (0,0)
device = "/dev/video0"

display = pygame.display.set_mode(displaysize)
camera = pygame.camera.Camera(device,
                              capturesize)
camera.start()

while 1:
  snapshot = camera.get_image()
  snapshot = pygame.transform.scale(snapshot,
                                    imagesize)
  display.blit(snapshot, imageorigin)
  pygame.display.flip()
