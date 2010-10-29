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
from Kamaelia.Apps.Whiteboard.ProperSurfaceDisplayer import ProperSurfaceDisplayer

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
                self.capture_one() # THIS IS FAILING - MAY BE THE CAMERA'S FAULT BUT NOT SURE
                #self.snapshot = pygame.transform.scale(self.snapshot,(190,140))
                self.snapshot=self.snapshot.convert()
                self.send(self.snapshot, "outbox")
                time.sleep(self.delay)
        except Exception, e:
            pass


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
    
    def __init__(self, displaysize, position, bgcolour, vertical=True):
        super(WebcamManager, self).__init__()
        self.displaysize = displaysize
        self.position = position
        self.bgcolour = bgcolour
        self.vertical = vertical
        # [[camera,displayhandle,oldposition,timeout=25],[camera,displayhandle,oldposition,timeout]....]
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
                    camera[3] -= 1
                    if camera[3] == 0:
                        # Camera has disconnected
                        # DESTROY ITS SURFACE HERE
                        camera[1].stop()
                        removallist.append(x)
                        
                for entry in removallist:
                    # Remove unused cameras from the camera list
                    self.cameralist.pop(entry)
                
                if isinstance(data,list):
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
                        camera[3] = 25 # Reset the timeout
                        handle = camera[1]
                        oldposition = camera[2]
                        cameraindex = self.cameralist.index(camera)
                        break
                else:
                    # Camera not found in the index - let's add it.
                    # Positioning calculated from the number of current active cams, along with specified display sizes and on screen position
                    self.cameralist.append([tag,None,None,25])
                    cameraindex = len(self.cameralist) - 1
                    handle = None
                    oldposition = None
                    
                if self.vertical:
                    cameraposition = (self.position[0],self.position[1]+((self.displaysize[1]+1)*cameraindex))
                else:
                    cameraposition = (self.position[0]+((self.displaysize[0]+1)*cameraindex),self.position[1])
                
                if handle == None or oldposition != cameraposition:
                    if oldposition != cameraposition and handle != None:
                        # Need to destroy the old component here
                        handle.stop()
                    handle = ProperSurfaceDisplayer(displaysize = self.displaysize, position = cameraposition, bgcolour=self.bgcolour).activate()
                    self.cameralist[cameraindex][1] = handle
                    self.cameralist[cameraindex][2] = cameraposition
                
                # Create a temporary link to send out data to the display
                self.link((self, "outbox"), (handle, "inbox"))
                snapshot = pygame.transform.scale(snapshot,self.displaysize)
                self.send(snapshot, "outbox")
                self.unlink(thecomponent=handle)

            while not self.anyReady():
                self.pause()
                yield 1
            yield 1  