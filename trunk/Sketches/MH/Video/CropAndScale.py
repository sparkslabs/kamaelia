#!/usr/bin/python
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
"""\
================================
Video frame cropping and scaling
================================

This component applies a crop and/or scaling operation to frames of RGB video.

Requires PIL - the `python imaging library<http://www.pythonware.com/products/pil/>`_.



Example Usage
-------------

Crop and scale a YUV4MPEG format uncompressed video file so that the output
is the region (100,100) ->(400,300), scaled up to 720x576::

    from Kamaelia.File.Reading import RateControlledFileReader

    Pipeline( RateControlledFileReader("input.yuv4mpeg", ... ),
              YUV4MPEGToFrame(),
              YUVtoRGB(),
              CropAndScale(newsize=(720,576), cropbounds=(100,100,400,300)),
              RGBtoYUV(),
              FrameToYUV4MPEG(),
              SimpleFileWriter("cropped_and_scaled.yuv4mpeg"),
            ).run()



More details
------------

Initialise this component specifying the region of the incoming video frames
to crop to, and the size of the desired output (the cropped region will be
scaled up/down to match this).

Send frame data structures to the "inbox" inbox of this component. The frames
will be cropped and scaled and output from the "outbox" outbox. Only frames
with one of the following pixel formats are currently supported:
    
    "RGB_interleaved"
    "RGBA_interleaved"
    "Y_planar"

See below for a description of the uncompressed frame data structure format.
Send uncompressed video frames, in the format described below,

This component supports sending data out of its outbox to a size limited inbox.
If the size limited inbox is full, this component will pause until it is able
to send out the data. Data will not be consumed from the inbox if this component
is waiting to send to the outbox.

If a producerFinished message is received on the "control" inbox, this component
will complete parsing any data pending in its inbox, and finish sending any
resulting data to its outbox. It will then send the producerFinished message on
out of its "signal" outbox and terminate.

If a shutdownMicroprocess message is received on the "control" inbox, this
component will immediately send it on out of its "signal" outbox and immediately
terminate. It will not complete processing, or sending on any pending data.



=========================
UNCOMPRESSED FRAME FORMAT
=========================

A frame is a dictionary data structure, containing at minimum one of these 
combinations::

    {
      "yuv" : luminance_data
      "pixformat" :  pixelformat        # format of raw video data
      "size" : (width, height)          # in pixels
    }

    {
      "rgb" : rgb_interleaved_data
      "pixformat" :  pixelformat        # format of raw video data
      "size" : (width, height)          # in pixels
    }

CropAndScale only guarantees to fill in the fields above. Any other fields will
be transparently passed through, unmodified.

"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Axon.AxonExceptions import noSpaceInBox

import Image


class CropAndScale(component):
    """\
    CropAndScale(newsize, cropbounds) -> new CropAndScale component.
    
    Crops and scales frames of video in RGB format.
    
    Keyword arguments:
        
    - newsize     -- (width, height) of the resulting output video frames (in pixels)
    - cropbounds  -- (x0,y0,x1,y1) region to crop out from the incoming video frames (in pixels)
    """

    def __init__(self, newsize, cropbounds):
        super(CropAndScale,self).__init__()
        self.newsize = newsize
        self.cropbounds = cropbounds[0], cropbounds[3], cropbounds[2], cropbounds[1]

    def handleControl(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) and not isinstance(self.shutdownMsg, shutdownMicroprocess):
                self.shutdownMsg = msg
            elif isinstance(msg, shutdownMicroprocess):
                self.shutdownMsg = msg

    def canStop(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, (producerFinished,shutdownMicroprocess))

    def mustStop(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, shutdownMicroprocess)
    
    def waitSend(self,data,boxname):
        while 1:
            try:
                self.send(data,boxname)
                return
            except noSpaceInBox:
                if self.mustStop():
                    raise "STOP"
                
                self.pause()
                yield 1
                
                if self.mustStop():
                    raise "STOP"

    def main(self):
        self.shutdownMsg = None
        i=0
        try:
            while 1:
                while self.dataReady("inbox"):
                    frame = self.recv("inbox")
                    newframe = self.processFrame(frame)
                    for _ in self.waitSend(newframe, "outbox"):
                        yield _
                    print i
                    i+=1
    
                if self.canStop():
                    raise "STOP"
    
                self.pause()
                yield 1
        except "STOP":
            self.send(self.shutdownMsg,"signal")


    def processFrame(self, frame):
        if frame['pixformat'] == "RGB_interleaved":
            mode = "RGB"
            datakey = "rgb"
        elif frame['pixformat'] == "RGBA_interleaved":
            mode = "RGBA"
            datakey = "rgb"
        elif frame['pixformat'] == "Y_planar":
            mode = "L"
            datakey = "yuv"
        else:
            raise "Can't process images with pixformat '"+frame['pixformat']+"'"

        img = Image.frombuffer(mode, frame['size'], frame[datakey])
        newimg = img.transform(self.newsize,
                                Image.EXTENT,
                                self.cropbounds,
                                Image.BICUBIC)
        newrgb = newimg.tostring()
        
        newframe = {}
        for key in frame.keys():
            newframe[key] = frame[key]
        newframe[datakey] = newrgb
        newframe['size'] = self.newsize
    
        return newframe

__kamaelia_components__  = ( CropAndScale )
