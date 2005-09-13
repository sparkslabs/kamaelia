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
import pygame

class RawYUVFramer(component):
    """Receives a raw data stream containing YUV data and frames it

       Outputting one frame at a time, as separate YUV planes, with additional metadata.

       frame format:
               { "size" : (pixels_width, pixels_height),
                 "pixformat" : pygamepixelformat,
                 "yuv" : ( ydata_string, udata_string, vdata_string ),
               }

       Currently only supports pygame.IYUV_OVERLAY pixel format.

       Incoming data should be a byte stream as strings. They can be of any chunk size.
    """
       
    def __init__(self, size, pixformat = pygame.IYUV_OVERLAY):
        super(RawYUVFramer, self).__init__()
        self.size = size
        self.pixformat = pixformat
#        if pixformat != pygame.IYUV_OVERLAY:
#            raise ValueError("Can't handle anything except pygame.IYUV_OVERLAY at the mo. Sorry!")

        ysize = size[0]*size[1]
        usize = ysize / 4
        vsize = usize
        self.planes = { "y":"", "u":"", "v":"" }
        self.sizes = { "y":ysize, "u":usize, "v":vsize }

    def main(self):

        done = False
    
        while not done:
            while self.dataReady("inbox"):
                raw = self.recv("inbox")
                self.packAndSend(raw)
                    
    
            if self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                    self.send(msg, "signal")
                    done=True
    
            if not done:
                self.pause()
                
            yield 1


    def flushFrame(self):
        """Send out a frame, flushing buffers"""
        frame = { "pixformat":self.pixformat,
                  "size":self.size,
                  "yuv":(self.planes['y'], self.planes['v'], self.planes['u'])
                }
        self.send( frame, "outbox" )
        self.planes['y'] = ""
        self.planes['u'] = ""
        self.planes['v'] = ""
        

    def packAndSend(self, raw):
        """Pack incoming raw data into y,u,v planes, and trigger flushes when they fill"""
        while raw:
            filled = False
            for plane in ['y','u','v']:
                remainder = self.sizes[plane] - len(self.planes[plane])
                filled = len(raw) >= remainder
                topupsize = min( len(raw), remainder )
                if topupsize:
                    self.planes[plane] += raw[:topupsize]
                    raw = raw[topupsize:]

            if filled:
                self.flushFrame()
