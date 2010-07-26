#!/usr/bin/env python
#
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
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