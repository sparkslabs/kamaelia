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

#
# SMELL : Periodically check if this is still needed or not.
#
# OVERLAY_FUDGE_OFFSET_FACTOR  is the result of experimentally
# trying to get SDL_Overlay/pygame.Overlay to work with Xorg/fbdev
# based displays on linux. If the overlay is precisely the right
# size and shape for the data, it can't be displayed right. 
# The value must be even, and preferably small. Odd values 
# result in the picture being sheared/slanted.
#
# This problem rears itself when the following version numbers are aligned:
#    SDL : 1.2.8
#    pygame : Anything up to/including 1.7.1prerelease
#    xorg : 6.8.2
#    Linux (for fbdev) : 2.6.11.4
#    
OVERLAY_FUDGE_OFFSET_FACTOR = 2
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
        self.size = argd.get("size",None)
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
        print self.size
        self.pixformat = frame['pixformat']
                
        displayservice = PygameDisplay.getDisplayService()
        self.link((self,"displayctrl"), displayservice)
        
        self.send({ "OVERLAYREQUEST":True,
                    "pixformat":self.pixformat,
                    "yuvservice":(self, "yuvdata"),
                    "size":(self.size[0]-OVERLAY_FUDGE_OFFSET_FACTOR, self.size[1]),
                    "position":self.position,
                    "yuv":frame['yuv'],
                  },
                  "displayctrl")

        yield 1

            
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

    pygamedisplay = PygameDisplay(width=800, height= 600, fullscreen = 1)
    pygamedisplay.activate()
    PygameDisplay.setDisplayService(pygamedisplay)

    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
    from RawYUVFramer import RawYUVFramer
    
    graph = ["\n",
"""DEL ALL
ADD NODE 0 0 auto -
""",
"""ADD NODE 1 1 auto -
ADD LINK 1 0
""",
"""ADD NODE 2 2 auto -
ADD LINK 2 0
""",
"""ADD NODE 3 3 auto -
ADD LINK 3 1
""",
"""ADD NODE 4 4 auto -
ADD LINK 4 1
""",
"""ADD NODE 5 5 auto -
ADD LINK 5 2
""",
"""ADD NODE 6 6 auto -
ADD LINK 6 2
""",
"""ADD NODE 7 7 auto -
ADD LINK 7 3
""",
"""ADD NODE 8 8 auto -
ADD LINK 8 3
""",
"""DEL ALL
""",
"""ADD NODE MusicServer MusicServer auto -
""",
"""ADD NODE TCPS1 TCPDistributionHub auto -
ADD NODE MS1 MulticastSender auto -
ADD LINK TCPS1 MS1
""",
"""ADD NODE MulticastRecv MulticastRecv auto -
ADD NODE TCPC1 "TCPClient (hub source)" auto -
ADD LINK MulticastRecv TCPC1
""",
"""ADD LINK MusicServer MulticastRecv
""",
"""ADD LINK TCPC1 TCPS1
""",
"""ADD NODE TCPC2 "TCPClient (BT)" auto -
""",
"""ADD LINK TCPS1 TCPC2
""",
"""ADD NODE MS2 MulticastSender auto -
ADD LINK TCPC2 MS2
""",
"""ADD NODE TCPS2 TCPSplitter auto -
ADD LINK TCPC2 TCPS2
""",
"""ADD NODE TCPC2 "TCPClient (NTL)" auto -
ADD LINK TCPS1 TCPC2
""" ]

    from Kamaelia.UI.Pygame.Button import Button
    from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
    from Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines import chunks_to_lines
    from Kamaelia.Visualisation.PhysicsGraph.TopologyViewerComponent import TopologyViewerComponent
    from Kamaelia.Util.Chooser import Chooser


    pipeline( ReadFileAdaptor("/data/dirac-video/foo.yuv", 
              readmode="bitrate",
              bitrate = 2280960*8),

              RawYUVFramer(size=(320,240), pixformat = pygame.IYUV_OVERLAY),

              VideoOverlay(),
            ).activate()
    
    pipeline(
         Button(caption="dink", msg="NEXT", position=(136,0), transparent=True, key=13),
         Chooser(items = graph),
         chunks_to_lines(),
         lines_to_tokenlists(),
         TopologyViewerComponent(transparency = (255,255,255), showGrid = False, position=(0,0)),
    ).run() # activate()




#    pipeline( ReadFileAdaptor("/data/dirac-video/snowboard-jum-720x576x50.yuv", 
#    pipeline( ReadFileAdaptor("/data/dirac-video/snowboard-jum-352x288x75.yuv", 
##    pipeline( ReadFileAdaptor("/data/dirac-video/snowboard-jum-720x576x50.yuv", 
#              readmode="bitrate",
#              bitrate = 2280960*8),
#              RawYUVFramer(size=(352,288), pixformat = pygame.IYUV_OVERLAY),
#              VideoOverlay(),
#            ).run()
