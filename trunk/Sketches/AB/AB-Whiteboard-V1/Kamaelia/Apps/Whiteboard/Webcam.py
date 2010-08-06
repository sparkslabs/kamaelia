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

    def capture_one(self):
        self.snapshot = None
        try:
            self.snapshot = self.camera.get_image()
        except Exception, e:
            pass

    def main(self):
        try:
            self.camera.start()
            while 1:
                self.capture_one()
                self.snapshot = pygame.transform.scale(self.snapshot,(190,140))
                self.snapshot=self.snapshot.convert()
                self.send(self.snapshot, "outbox")
                time.sleep(self.delay)
        except Exception, e:
            pass
