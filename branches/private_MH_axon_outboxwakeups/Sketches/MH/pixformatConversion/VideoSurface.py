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


from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Axon.Ipc import WaitComplete
from Kamaelia.UI.GraphicDisplay import PygameDisplay
import pygame


from pixConvert import rgbi_to_yuv420p   # RGB_interleaved to YUV420_planar
from pixConvert import yuv420p_to_rgbi   # YUV420_planar to RGB_interleaved
from pixConvert import yuv422p_to_rgbi   # YUV422_planar to RGB_interleaved

class YUVtoRGB(component):
    
    Inboxes =  { "inbox"   : "YUV video frame",
                 "control" : "Shutdown signalling"
               }
    Outboxes = { "outbox"      : "RGB video frame",
                 "signal"      : "Shutdown signalling",
               }


    def main(self):
        """Main loop."""

        done = False
        
        while not done:
            while self.dataReady("inbox"):
                
                frame = self.recv("inbox")
                if frame['pixformat'] == "YUV420_planar":
                    Y,U,V = frame['yuv']
                    W,H   = frame['size']
                    self.send({ "rgb"       : yuv420p_to_rgbi(Y,U,V, W,H),
                                "size"      : (W,H),
                                "pixformat" : "RGB_interleaved",
                              }, "outbox")
                    
                elif frame['pixformat'] == "YUV422_planar":
                    Y,U,V = frame['yuv']
                    W,H   = frame['size']
                    self.send({ "rgb"       : yuv422p_to_rgbi(Y,U,V, W,H),
                                "size"      : (W,H),
                                "pixformat" : "RGB_interleaved",
                              }, "outbox")
                    

            if self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                    self.send(msg, "signal")
                    done=True
                    
            if not done:
                self.pause()
                
            yield 1



class RGBtoYUV(component):
    
    Inboxes =  { "inbox"   : "RGB video frame",
                 "control" : "Shutdown signalling"
               }
    Outboxes = { "outbox"      : "YUV video frame",
                 "signal"      : "Shutdown signalling",
               }


    def main(self):
        """Main loop."""

        done = False
        
        while not done:
            while self.dataReady("inbox"):
                
                frame = self.recv("inbox")
                if frame['pixformat'] == "RGB_interleaved":
                    rgb = frame['rgb']
                    W,H = frame['size']
                    self.send({ "yuv"       : rgbi_to_yuv420p(rgb, W,H),
                                "size"      : (W,H),
                                "pixformat" : "YUV420_planar",
                              }, "outbox")
                    
            if self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                    self.send(msg, "signal")
                    done=True
                    
            if not done:
                self.pause()
                
            yield 1



class VideoSurface(component):
    """\
    Image() -> new VideoSurface component
    
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
        
    def __init__(self):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(VideoSurface, self).__init__()
        self.display = None
        
        self.size = None
        self.pixformat = None
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



__kamaelia_components__  = ( YUVtoRGB, VideoSurface )

            
        
if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
    from Kamaelia.Codec.RawYUVFramer import RawYUVFramer
    from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay
    
#    Pipeline( ReadFileAdaptor("/data/dirac-video/snowboard-jum-352x288x75.yuv", readmode="bitrate", bitrate = 2280960*8),
#              RawYUVFramer(size=(352,288), pixformat = "YUV420_planar" ),
#              YUVtoRGB(),
#              VideoSurface(),
#            ).run()
            
    from Kamaelia.Codec.Dirac import DiracDecoder
            
    Pipeline( ReadFileAdaptor("/data/dirac-video/snowboard-jum-352x288x75.dirac.drc", readmode="bitrate", bitrate = 2280960*8),
              DiracDecoder(),
              YUVtoRGB(),
              RGBtoYUV(),
              YUVtoRGB(),
              VideoSurface(),
#              VideoOverlay(),
            ).run()
