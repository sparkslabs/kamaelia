#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
# -------------------------------------------------------------------------
#

import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess
import pygame
import time

# Webcam - Idea: Send images to network. Display on both local and remote screen
import pygame.camera
        
class Webcam(Axon.Component.component):
    
    Inboxes =  { "inbox"   : "Receives stuff (possibly)",
               }
               
    Outboxes = { "outbox" : "Issues drawing instructions locally",
                 "networkout" : "Issues drawing instructions remotely",
               }
    
    def __init__(self):
        super(Webcam,self).__init__()
        pygame.camera.init()
        capturesize = (640,480)
        self.imagesize=((63*3+2),140)
        self.imageorigin = ((1024-(63*3+2+1)),1) #(768-(288+32+15))
        device="/dev/video0"
        self.camera = X=pygame.camera.Camera(device, capturesize)
        try:
            self.camera.start()
        except Exception, e:
            self.camera = False
            print ("Camera fail")
    
    def main(self):
        while(1):
            try:	
                if (self.camera):
                    snapshot = self.camera.get_image()
                    snapshot = pygame.transform.scale(snapshot, self.imagesize)
                    self.send([["CAM", snapshot, self.imageorigin, "local"]], "outbox")
                    self.send([["CAM", snapshot, self.imageorigin, "remote"]], "networkout")
            except Exception, e:
                pass
	    #print("image")
            self.pause()
            yield 1
            #time.sleep(0.2)
	    yield 1