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
import sys

try:
    import pygame.camera
except ImportError:
    print ("*****************************************************************************************")
    print ("")
    print ("Sorry, Video camera support requires using a version of pygame with pygame.camera support")
    print ("""You could try adding something like this at the start of your file using this componen:

# To use pygame alpha
import sys ;
sys.path.insert(0, "<path to release candidate>/pygame-1.9.0rc1/build/lib.linux-i686-2.5")

""")
    print ("*****************************************************************************************")
    raise
  
from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import producerFinished, shutdownMicroprocess, WaitComplete
from Axon.Component import component

from Kamaelia.UI.Pygame.Display import PygameDisplay
from Kamaelia.Apps.Whiteboard.ProperSurfaceDisplayer import ProperSurfaceDisplayer

pygame.init()        # Would be nice to be able to find out if pygame was already initialised or not.
pygame.camera.init() # Ditto for camera subsystem

class VideoCaptureSource(threadedcomponent):
    #capturesize = (352, 288)
    capturesize = (1024, 768)
    delay = 0.1
    fps = -1
    
    def __init__(self, device="/dev/video0"):
        super(VideoCaptureSource, self).__init__()
        self.device = device

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
        except Exception:
            sys.stderr.write("Faled to grab image. Is your camera UVC compatible?")

    def main(self):
        self.camera = pygame.camera.Camera(self.device, self.capturesize)
        if self.fps != -1:
            self.delay = 1.0/self.fps
        self.snapshot = None
        try:
            self.camera.start()
            while self.shutdown():
                self.capture_one() # Fails for PWC webcam, need UVC
                self.snapshot=self.snapshot.convert()
                self.send(self.snapshot, "outbox")
                time.sleep(self.delay)
        except Exception:
            sys.stderr.write("Faled to connect to camera. Is it connected?")


class WebcamManager(component):
    # I strongly suspect the creating / destroying of component here will create a memory leak (albeit a very small and slow one)
    # The other way to achieve this would be to create a single display and pass images to blit, along with a position to the ProperSurfaceDisplayer
    # Need advice on the preferred approach
    
    Inboxes = {
        "inbox" : "Receives webcam images in. For local cameras, plainly in the format: image. For remote cameras, in the format [tag,image]",
        "control" : "",
    }
    Outboxes = {
        "outbox" : "",
        "signal" : "",
    }
    
    def __init__(self, camerasize, vertical=True):
        super(WebcamManager, self).__init__()
        self.camerasize = camerasize
        self.vertical = vertical
        
        # [[camera,oldposition,timeout=25],[camera,oldposition,timeout]....]
        self.cameralist = list()

    def shutdown(self):
       """Return 0 if a shutdown message is received, else return 1."""
       if self.dataReady("control"):
           msg=self.recv("control")
           if isinstance(msg,producerFinished) or isinstance(msg,shutdownMicroprocess):
               self.send(producerFinished(self),"signal")
               return 0
       return 1

    def main(self):
        while self.shutdown():
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                
                # Remove cameras where clients have disconnected
                removallist = list()
                for camera in self.cameralist:
                    camera[2] -= 1
                    if camera[2] == 0:
                        # Camera has disconnected
                        # DESTROY ITS SURFACE HERE
                        surf = pygame.Surface((1200,700))
                        surf.fill((255,255,0,255),pygame.Rect(0,0,200,700))
                        surf.fill((0,255,255,255),pygame.Rect(200,0,200,700))
                        surf.fill((128,255,0,255),pygame.Rect(400,0,200,700))
                        surf.fill((255,0,128,255),pygame.Rect(600,0,200,700))
                        surf.fill((255,0,0,255),pygame.Rect(800,0,200,700))
                        surf.fill((0,0,255,255),pygame.Rect(1000,0,200,700))
                        surf = pygame.transform.scale(surf,self.camerasize)
                        self.send([surf,camera[1]], "outbox")
                        removallist.append(camera)
                        
                for entry in removallist:
                    # Remove unused cameras from the camera list
                    self.cameralist.remove(entry)
                
                if isinstance(data,tuple):
                    # Received a remote camera image
                    tag = data[0]
                    snapshot = data[1]
                else:
                    # Received a local camera image
                    tag = "local"
                    snapshot = data
                    
                for camera in self.cameralist:
                    if camera[0] == tag:
                        # Found the camera in the positions index
                        camera[2] = 25 # Reset the timeout
                        oldposition = camera[1]
                        cameraindex = self.cameralist.index(camera)
                        break
                else:
                    # Camera not found in the index - let's add it.
                    # Positioning calculated from the number of current active cams, along with specified display sizes and on screen position
                    self.cameralist.append([tag,None,25])
                    cameraindex = len(self.cameralist) - 1
                    oldposition = None
                    
                if self.vertical:
                    cameraposition = (0,((self.camerasize[1]+1)*cameraindex))
                else:
                    cameraposition = (((self.camerasize[0]+1)*cameraindex),0)
                
                if oldposition != cameraposition:
                    if oldposition != cameraposition and oldposition != None:
                        # Need to destroy the old component here
                        surf = pygame.Surface(self.camerasize)
                        surf.fill((0,0,0,0))
                        self.send([surf,oldposition], "outbox")
                    self.cameralist[cameraindex][1] = cameraposition
                
                snapshot = pygame.transform.scale(snapshot,self.camerasize)
                self.send([snapshot,cameraposition], "outbox")

            while not self.anyReady():
                self.pause()
                yield 1
            yield 1  
