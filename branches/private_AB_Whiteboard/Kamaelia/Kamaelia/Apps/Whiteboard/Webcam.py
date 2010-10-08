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

try:
    import pygame.camera
except ImportError:
    print "*****************************************************************************************"
    print
    print "Sorry, Video camera support requires using a version of pygame with pygame.camera support"
    print """You could try adding something like this at the start of your file using this componen:

# To use pygame alpha
import sys ;
sys.path.insert(0, "<path to release candidate>/pygame-1.9.0rc1/build/lib.linux-i686-2.5")

"""
    print "*****************************************************************************************"
    raise
  
from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import producerFinished, shutdownMicroprocess, WaitComplete
from Axon.Component import component

from Kamaelia.UI.Pygame.Display import PygameDisplay

pygame.init()        # Would be nice to be able to find out if pygame was already initialised or not.
pygame.camera.init() # Ditto for camera subsystem

class VideoCaptureSource(threadedcomponent):
    #capturesize = (352, 288)
    capturesize = (1024, 768)
    delay = 0.1
    fps = -1
    device = "/dev/video0"
 
    def __init__(self, **argd):
        super(VideoCaptureSource, self).__init__(**argd)
        self.camera = pygame.camera.Camera(self.device, self.capturesize)
        if self.fps != -1:
            self.delay = 1.0/self.fps
        self.snapshot = None

    def shutdown(self):
       """Return 0 if a shutdown message is received, else return 1."""
       if self.dataReady("control"):
           msg=self.recv("control")
           if isinstance(msg,producerFinished) or isinstance(msg,shutdownMicroprocess):
               self.send(producerFinished(self),"signal")
               return 0
       return 1

    def capture_one(self):
        self.snapshot = None
        try:
            self.snapshot = self.camera.get_image()
        except Exception, e:
            pass

    def main(self):
        try:
            self.camera.start()
            while self.shutdown():
                self.capture_one()
                #self.snapshot = pygame.transform.scale(self.snapshot,(190,140))
                self.snapshot=self.snapshot.convert()
                self.send(self.snapshot, "outbox")
                time.sleep(self.delay)
        except Exception, e:
            pass


class WebcamManager(component):
    Inboxes = {
        "inbox" : "",
        "control" : "",
        "callback" : "",
    }
    Outboxes = {
        "outbox" : "",
        "signal" : "",
        "display_signal" : "",
    }
    remotecams = [0,0,0,0]
    remotecamcount = [25,25,25,25]
    def __init__(self, **argd):
        super(WebcamManager, self).__init__(**argd)
        self.disprequest = { "DISPLAYREQUEST" : True,
                           "callback" : (self,"callback"),
                           "size": self.displaysize,
                           "position" : self.position,
                           "bgcolour" : self.bgcolour}

    def shutdown(self):
       """Return 0 if a shutdown message is received, else return 1."""
       if self.dataReady("control"):
           msg=self.recv("control")
           if isinstance(msg,producerFinished) or isinstance(msg,shutdownMicroprocess):
               self.send(producerFinished(self),"signal")
               return 0
       return 1

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
       self.display.fill( (self.bgcolour) )

    def main(self):
       yield WaitComplete(self.getDisplay())
       # initialise five webcam windows
       if self.webcam == 1:
          snapshot = "No Local Camera"
          font = pygame.font.Font(None,22)
          self.display.fill( (0,0,0) )
          snapshot = font.render(snapshot, False, (255,255,255))
          self.display.blit(snapshot, (34,56))
          self.pygame_display_flip()
       elif self.webcam == 2:
          snapshot = "No Remote Camera"
          font = pygame.font.Font(None,22)
          self.display.fill( (0,0,0),pygame.Rect(0,0,190,140*4))
          snapshot = font.render(snapshot, False, (255,255,255))
          self.display.blit(snapshot, (25,56)) 
          self.display.blit(snapshot, (25,56+140*1+1)) 
          self.display.blit(snapshot, (25,56+140*2+2)) 
          self.display.blit(snapshot, (25,56+140*3+3)) 
          self.pygame_display_flip()
       while self.shutdown():
          if self.webcam:
              while self.dataReady("inbox"):
                  snapshot = self.recv("inbox")
                  if self.webcam == 1:
                      #snapshot=snapshot.convert()
                      self.display.blit(snapshot, (0,0))
                      self.pygame_display_flip()
                  elif self.webcam == 2:
                      # remove tag
                      tag = snapshot[0]
                      data = snapshot[1]
                      pretagged = False
                      # allocate tag to a cam window
                      for x in self.remotecams:
                          if x == tag:
                              pretagged = True
                              
                      if pretagged == False:
                          if self.remotecams[0] == 0:
                              self.remotecams[0] = tag
                          elif self.remotecams[1] == 0:
                              self.remotecams[1] = tag
                          elif self.remotecams[2] == 0:
                              self.remotecams[2] = tag
                          elif self.remotecams[2] == 0:
                              self.remotecams[3] = tag

                      # public cam pic to window if one is available
                      iteration = 0
                      for x in self.remotecams:
                          if self.remotecams[iteration] == tag:
                              offset = (140 * iteration + iteration * 1)
                              self.display.blit(data, (0,0+offset))
                              self.remotecamcount[iteration] = 25 # reset cam count to prevent 'no remote cam'
                          iteration += 1

                      # Reset remote cameras where clients have disconnected (remotecamcount = 0)
                      iteration = 0
                      for x in self.remotecamcount:
                          if self.remotecamcount[iteration] == 0:
                              snapshot = "No Remote Camera"
                              font = pygame.font.Font(None,22)
                              offset = (iteration * 140 + iteration * 1)
                              self.display.fill( (0,0,0),pygame.Rect(0,offset,190,140))
                              snapshot = font.render(snapshot, False, (255,255,255))
                              self.display.blit(snapshot, (25,56+offset)) 
                              self.remotecams[iteration] = 0
                          elif self.remotecamcount[iteration] > 0:
                              self.remotecamcount[iteration] -= 1
                          iteration += 1

                      self.pygame_display_flip()

              while not self.anyReady():
                self.pause()
                yield 1
              yield 1  
          else:
              self.pause()
              yield 1