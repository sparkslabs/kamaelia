#!/usr/bin/env python
#
# Copyright (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""\
====================
Pygame Video Surface
====================

Displays uncompressed RGB video data on a pygame surface using the Pygame
Display service.



Example Usage
-------------

Read raw YUV data from a file, convert it to interleaved RGB  and display it
using VideoSurface::

    imagesize = (352, 288)        # "CIF" size video
    fps = 15                      # framerate of video
    
    Pipeline(ReadFileAdapter("raw352x288video.yuv", ...other args...),
             RawYUVFramer(imagesize),
             MessageRateLimit(messages_per_second=fps, buffer=fps*2),
             ToRGB_interleaved(),
             VideoSurface(),
            ).activate()

RawYUVFramer is needed to frame raw YUV data into individual video frames.
ToRGB_interleaved is needed to convert the 3 planes of Y, U and V data to a
single plane containing RGB data interleaved (R, G, B, R, G, B, R, G, B, ...)



How does it work?
-----------------

The component waits to receive uncompressed video frames from its "inbox" inbox.

The frames must be encoded as dictionary objects in the format described below.

When the first frame is received, the component notes the size and pixel format
of the video data and requests an appropriate surface from the
Pygame Display service component, to which video can be rendered.

NOTE: Currently the only supported pixelformat is "RGB_interleaved".

When subsequent frames of video are received the rgb data is rendered to the
surface and the Pygame Display service is notified that the surface needs
redrawing.

At present, VideoSurface cannot cope with a change of pixel format or video
size mid sequence.



=========================
UNCOMPRESSED FRAME FORMAT
=========================

Uncompresed video frames must be encoded as dictionaries. VideoSurface requires
the following entries::

    {
      "rgb" : rgbdata                    # a string containing RGB video data
      "size" : (width, height)           # in pixels
      "pixformat" : "RGB_interleaved"    # format of raw video data
    }

"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Axon.Ipc import WaitComplete
from Kamaelia.UI.GraphicDisplay import PygameDisplay
import pygame


class VideoSurface(component):
    """\
    VideoSurface([position]) -> new VideoSurface component

    Displays a pygame surface using the Pygame Display service component, for
    displaying RGB video frames sent to its "inbox" inbox.
    
    The surface is sized and configured by the first frame of (uncompressed)
    video data is receives.
    

    Keyword arguments:

   - position      -- (x,y) pixels position of top left corner (default=(0,0))
    """
    
    Inboxes = { "inbox"    : "Video frame data structures containing RGB data",
                "control"  : "Shutdown messages: shutdownMicroprocess or producerFinished",
                "callback" : "Receive callbacks from Pygame Display",
              }
    Outboxes = {
                 "outbox" : "NOT USED",
                 "signal" : "Shutdown signalling: shutdownMicroprocess or producerFinished",
                 "display_signal" : "Outbox used for sending signals of various kinds to the display service"
               }
        
    def __init__(self, position=None):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(VideoSurface, self).__init__()
        self.display = None
        
        self.size = None
        self.pixformat = None

        if position is not None:
            self.position = position
        else:
            self.position = (0,0)


    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True
        return False
    
        
    def waitBox(self,boxname):
        """Generator. yield's 1 until data is ready on the named inbox."""
        waiting = True
        while waiting:
            if self.dataReady(boxname): return
            else: yield 1

            
    def formatChanged(self, frame):
        """Returns True if frame size or pixel format is new/different for this frame."""
        return frame['size'] != self.size or frame['pixformat'] != self.pixformat
    
    def main(self):
        """Main loop."""
        
        displayservice = PygameDisplay.getDisplayService()
        self.link((self,"display_signal"), displayservice)
        
        while 1:
            # wait for a frame
            frame = False
            while not frame:
                if self.dataReady("inbox"):
                    frame = self.recv("inbox")
                    
                    if self.shutdown():
                        return
              
                if not self.anyReady():
                    self.pause()
                yield 1
              
            # is it the same format as our current frame?
            if self.formatChanged(frame):
                if self.display:
                    raise "Can't cope with a format change yet!"
                
                self.size = frame['size']
                self.pixformat = frame['pixformat']
                
                if self.pixformat != "RGB_interleaved":
                    raise "Can't cope with any pixformat other than RGB_interleaved"
              
      
                # request a surface
                # build the initial request to send to Pygame Display to obtain a surface
                # but store it away until main() main loop is activated.
                dispRequest = { "DISPLAYREQUEST" : True,
                                "callback" : (self,"callback"),
                                "size": self.size,
                                "position" : self.position
                              }
                              
                self.send(dispRequest, "display_signal")
                
                # wait for the surface back
                yield WaitComplete(self.waitBox("callback"))
                self.display = self.recv("callback")
                
            # now render our frame
            image = pygame.image.fromstring(frame['rgb'], frame['size'], "RGB", False)
      
            self.display.blit(image, (0,0))
            self.send({"REDRAW":True, "surface":self.display}, "display_signal")
            
            # deal with possible shutdown requests
            if self.shutdown():
                return
            
            if not self.anyReady():
                self.pause()
                yield 1



__kamaelia_components__  = ( VideoSurface, )

            
        
if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
    from Kamaelia.Codec.RawYUVFramer import RawYUVFramer
    from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay
    from Kamaelia.Video.PixFormatConversion import ToYUV420_planar
    from Kamaelia.Video.PixFormatConversion import ToRGB_interleaved
    
#    Pipeline( ReadFileAdaptor("/data/dirac-video/snowboard-jum-352x288x75.yuv", readmode="bitrate", bitrate = 2280960*8),
#              RawYUVFramer(size=(352,288), pixformat = "YUV420_planar" ),
#              ToRGB_interleaved(),
#              VideoSurface(),
#            ).run()
            
    from Kamaelia.Codec.Dirac import DiracDecoder
            
    Pipeline( ReadFileAdaptor("/data/dirac-video/snowboard-jum-352x288x75.dirac.drc", readmode="bitrate", bitrate = 2280960*8),
              DiracDecoder(),
              ToRGB_interleaved(),
              ToYUV420_planar(),
              ToRGB_interleaved(),
              VideoSurface((200,100)),
            ).run()
