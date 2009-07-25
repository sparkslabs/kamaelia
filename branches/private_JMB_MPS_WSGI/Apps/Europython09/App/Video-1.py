#!/usr/bin/python

# To use pygame alpha on my machine, You probably need to change this
import sys ;
sys.path.insert(0, "/home/zathras/Documents/pygame-1.9.0rc1/build/lib.linux-i686-2.5")


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
