#!/usr/bin/python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.UI.PygameDisplay import PygameDisplay
import pygame

class VideoOverlay(component):
    """Sets up a video overlay using pygame, and feeds yuv video data to it"""
    
    Inboxes = {"inbox":"uncompressed video frames",
               "control":""
              }
    Outboxes = {"outbox":"unused",
                "signal":"",
                "displayctrl":"pygame display service",
                "yuvdata":"yuv data sent to overlay display service"
               }
    
    def __init__(self, **argd):
        super(VideoOverlay,self).__init__()
        self.size = None
        self.pixformat = None
        self.position = (0,0)
        
        

    def waitBox(self,boxname):
        waiting = True
        while waiting:
            if self.dataReady(boxname): return
            else: yield 1

    def formatChanged(self, frame):
        return frame['size'] != self.size or frame['pixformat'] != self.pixformat
            
    def newOverlay(self, frame):
        """Request an overlay to suit the supplied frame of data"""
        self.size = frame['size']
        self.pixformat = frame['pixformat']
                
        displayservice = PygameDisplay.getDisplayService()
        self.link((self,"displayctrl"), displayservice)
        self.send({ "OVERLAYREQUEST":True,
                    "pixformat":self.pixformat,
                    "yuvservice":(self, "yuvdata"),
                    "size":self.size,
                    "position":self.position,
                    "yuv":frame['yuv'],
                  },
                  "displayctrl")

        yield 1
#        for _ in self.waitBox("control"): yield 1
#        display = self.recv("control")

            
    def main(self):

        done = False
        
        while not done:
            while self.dataReady("inbox"):
                frame = self.recv("inbox")
                if self.formatChanged(frame):
                    for _ in self.newOverlay(frame):
                        yield _
                else:
                    self.send( frame['yuv'], "yuvdata" )

            if self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                    self.send(msg, "signal")
                    done=True
                    
            if not done:
                self.pause()
                
            yield 1




            
        
if __name__ == "__main__":
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
    from RawYUVFramer import RawYUVFramer
    
#    pipeline( ReadFileAdaptor("/data/dirac-video/snowboard-jum-352x288x75.yuv", readmode="bitrate", bitrate = 2280960*8),
    pipeline( ReadFileAdaptor("test.yuv", readmode="bitrate", bitrate = 2280960*8),
              RawYUVFramer(size=(352,288), pixformat = pygame.IYUV_OVERLAY),
#    pipeline( ReadFileAdaptor("/data/dirac-video/snowboard-jum-720x576x50.yuv", readmode="bitrate", bitrate = 2280960*8*4),
#              RawYUVFramer(size=(720,576), pixformat = pygame.IYUV_OVERLAY),
              VideoOverlay(),
            ).run()
            