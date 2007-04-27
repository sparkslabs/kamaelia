#!/usr/bin/env python
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
"""\
====================
Pygame Video Overlay
====================

Displays uncompressed video data on a pygame 'overlay' using the Pygame Display
service.



Example Usage
-------------

Read raw YUV data from a file and display it using VideoOverlay::

    imagesize = (352, 288)        # "CIF" size video
    fps = 15                      # framerate of video
    
    Pipeline(ReadFileAdapter("raw352x288video.yuv", ...other args...),
             RawYUVFramer(imagesize),
             MessageRateLimit(messages_per_second=fps, buffer=fps*2)
             VideoOverlay()
            ).activate()

RawYUVFramer is needed to frame raw YUV data into individual video frames.



How does it work?
-----------------

The component waits to receive uncompressed video frames from its "inbox" inbox.

The frames must be encoded as dictionary objects in the format described below.

When the first frame is received, the component notes the size and pixel format
of the video data and requests an appropriate 'overlay' surface from the
Pygame Display service component, to which video can be rendered.

NOTE: Currently the only supported pixelformat is "YUV420_planar".

NOTE: A fudge factor is currently applied to the video size (see below)

Included in the request is a reference to an outbox through which the component
will send the yuv video data for future frames of video. For video overlays,
the video data must be sent direct to the Pygame Display component rather than
be rendered onto an intermediate surface.

Also included in the request is the data for the first frame of video.

When subsequent frames of video are received the yuv data is sent to the
"yuvdata" outbox, which by now is linked to the Pygame Display component.

If the frame of video is of a different pixel format or size then VideoOverlay
will re-request a new overlay.

NOTE: If this happens, the component does NOT dispose of the old surface.
This behaviour should therefore be avoided at present - repeated changes of
video size/pixel format will result in multiple overlays accumulating in the
pygame display.


Fudge factor
^^^^^^^^^^^^

The size of overlay requested by the VideoOverlay component is adjusted by a
fudge factor.

This is a workaround for problems with  Xorg/fbdev based displays on linux. If
the overlay is precisely the right size and shape for the data, it can't be
displayed right. The value must be even, and preferably small. Odd values result
in the picture being sheared/slanted.

This problem rears itself when the following version numbers are aligned:
  
- SDL : 1.2.8
- pygame : Anything up to/including 1.7.1prerelease
- xorg : 6.8.2
- Linux (for fbdev) : 2.6.11.4

The fudge factor does not appear to adversely affect behaviour on other
system configurations.



=========================
UNCOMPRESSED FRAME FORMAT
=========================

Uncompresed video frames must be encoded as dictionaries. VidoeOverlay requires
the following entries::

    {
      "yuv" : (y_data, u_data, v_data)  # a tuple of strings
      "size" : (width, height)          # in pixels
      "pixformat" :  "YUV420_planar"    # format of raw video data
    }



"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.UI.GraphicDisplay import PygameDisplay
import pygame


# mappings of 'frame' pixformat values to pygame overlay modes
pygame_pixformat_map = { "YUV420_planar" : pygame.IYUV_OVERLAY }


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#
# XXX SMELL : Periodically check if this is still needed or not.
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
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

OVERLAY_FUDGE_OFFSET_FACTOR = 2

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#
# XXX VOMIT : does not get rid of an old overlay if a new one is requested
#             (due to a change in video size/pixel format)
#             resulting in overlays accumulating in Pygame Display
#
#             Either the request for a new overlay must be suppressed, or the
#             old overlay should be destroyed. The latter will require support
#             for deallocating surfaces/overlays to be added to Pygame Display
#             component
#
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX



class VideoOverlay(component):
    """\
    VideoOverlay() -> new VideoOverlay component

    Displays a pygame video overlay using the Pygame Display service component.
    The overlay is sized and configured by the first frame of
    (uncompressed) video data is receives.
    
    NB: Currently, the only supported pixel format is "YUV420_planar"
    """
    
    Inboxes =  { "inbox"   : "Receives uncompressed video frames",
                 "control" : "Shutdown signalling"
               }
    Outboxes = { "outbox"      : "NOT USED",
                 "signal"      : "Shutdown signalling",
                 "displayctrl" : "Sending requests to the Pygame Display service",
                 "yuvdata"     : "Sending yuv video data to overlay display service"
               }


    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(VideoOverlay,self).__init__()
        self.size = None
        self.pixformat = None
        self.position = (0,0)
        
        

    def waitBox(self,boxname):
        """Generator. yields 1 until data ready on the named inbox."""
        waiting = True
        while waiting:
            if self.dataReady(boxname): return
            else: yield 1

    def formatChanged(self, frame):
        """Returns True if frame size or pixel format is new/different for this frame."""
        return frame['size'] != self.size or frame['pixformat'] != self.pixformat
            
    def newOverlay(self, frame):
        """Request an overlay to suit the supplied frame of data"""
        self.size = frame['size']
        self.pixformat = frame['pixformat']
        self.pygamepixformat = pygame_pixformat_map[self.pixformat]
                
        displayservice = PygameDisplay.getDisplayService()
        self.link((self,"displayctrl"), displayservice)
        self.send({ "OVERLAYREQUEST":True,
                    "pixformat":self.pygamepixformat,
                    "yuvservice":(self, "yuvdata"),
                    "size":(self.size[0]-OVERLAY_FUDGE_OFFSET_FACTOR, self.size[1]),
                    "position":self.position,
                    "yuv":frame['yuv'],
                  },
                  "displayctrl")

        yield 1
#        for _ in self.waitBox("control"): yield 1
#        display = self.recv("control")

            
    def main(self):
        """Main loop."""

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

__kamaelia_components__  = ( VideoOverlay, )

            
        
if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
    from Kamaelia.Codec.RawYUVFramer import RawYUVFramer
    
    Pipeline( ReadFileAdaptor("/data/dirac-video/snowboard-jum-352x288x75.yuv", readmode="bitrate", bitrate = 2280960*8),
#    Pipeline( ReadFileAdaptor("test.yuv", readmode="bitrate", bitrate = 2280960*8),
              RawYUVFramer(size=(352,288), pixformat = "YUV420_planar" ),
#    Pipeline( ReadFileAdaptor("/data/dirac-video/snowboard-jum-720x576x50.yuv", readmode="bitrate", bitrate = 2280960*8*4),
#              RawYUVFramer(size=(720,576), pixformat = pygame.IYUV_OVERLAY),
              VideoOverlay(),
            ).run()
            