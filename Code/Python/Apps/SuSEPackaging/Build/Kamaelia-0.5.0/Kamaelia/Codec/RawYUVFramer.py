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
"""\
=========================
Raw YUV video data framer
=========================

This component takes a raw stream of YUV video data and breaks it into
invidual frames. It sends them out one at a time, tagged with relevant data
such as the frame size.

Many components that expect uncompressed video require it to be structured into
frames in this way, rather than as a raw stream of continuous data. This
component fulfills that requirement.


Example Usage
-------------

Reading and encoding raw video::

    imagesize = (352, 288)        # "CIF" size video
    
    Pipeline(ReadFileAdapter("raw352x288video.yuv", ...other args...),
             RawYUVFramer(imagesize),
             DiracEncoder(preset="CIF"),
            ).activate()



More Detail
-----------

Receives raw yuv video data, as strings on its "inbox" inbox.

Sends out individual frames packaged in a dictionary::
    {
      "yuv" : (y_data, u_data, v_data),  # a tuple of strings
      "size" : (width, height),          # in pixels
      "pixformat" : "YUV420_planar",     # raw video data format
    }

The component will terminate if it receives a shutdownMicroprocess or
producerFinished message on its "control" inbox. The message is passed on out of
the "signal" outbox.


"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess


class RawYUVFramer(component):
    """
    RawYUVFramer(size,pixformat) -> raw yuv video data framing component

    Creates a component that frames a raw stream of YUV video data into frames.

    Keyword arguments:
    
    - size = (width,height)        -- size of a video frame in pixels
    - pixformat = "YUV420_Planar"  -- raw video data format
    """
       
    def __init__(self, size, pixformat = "YUV420_planar"):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(RawYUVFramer, self).__init__()
        self.size = size
        self.pixformat = pixformat
#        if pixformat != YUV420_planar
#            raise ValueError("Can't handle anything except YUV420_planar at the mo. Sorry!")

        ysize = size[0]*size[1]
        usize = ysize / 4
        vsize = usize
        self.planes = { "y":"", "u":"", "v":"" }
        self.sizes = { "y":ysize, "u":usize, "v":vsize }

    def main(self):
        """Main loop"""
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
                  "yuv":(self.planes['y'], self.planes['u'], self.planes['v'])
                }
        self.send( frame, "outbox" )
        self.planes['y'] = ""
        self.planes['u'] = ""
        self.planes['v'] = ""
        

    def packAndSend(self, raw):
        """
        packAndSend(raw) -> None
        
        Pack incoming raw data into y,u,v planes, and triggers a flush when all
        planes are full.
        """
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

__kamaelia_components__ = ( RawYUVFramer, )
