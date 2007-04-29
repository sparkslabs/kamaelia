#!/usr/bin/env python

# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
====================================
Detecting cuts/shot changes in video
====================================

DetectShotChanges takes in (framenumber, videoframe) tuples on its "inbox" inbox and
attempts to detect where shot changes have probably occurred in the sequence.
When it thinks one has ocurred, a (framenumber, confidencevalue) tuple is sent
out of the "outbox" outbox.


Example Usage
-------------

Reading in a video in uncompressed YUV4MPEG file format, and outputting the
frame numbers (and confidence values) where cuts probably occur::
    
    Pipeline( RateControlledFileReader(..)
              YUV4MPEGToFrame(),
              TagWithSequenceNumber(),      # pair up frames with a frame number
              DetectShotChanges(threshold=0.85),
              ConsoleEchoer(),
            ).run()
            
Expect output like this::
    
    (17, 0.885)(18, 0.912)(56, 0.91922)(212, 0.818)(213, 0.825)(214, 0.904) ...
    


More detail
-----------

Send (frame-number, video-frame) tuples to this component's "inbox" inbox and
(frame-number, confidence-value) tuples will be sent out of the "outbox" outbox
whenever it thinks a cut has occurred.

Frames must be in a YUV format. See below for details. Frame numbers need not
necessarily be sequential; but they must be unique! If they are not, then it is
your own fault when you can't match up detected shot changes to actual video
frames!

Internally, the cut detector calculates a 'confidence' value representing how
likely that a shot change has occurred. At initialisation you set a threshold
value - if the confidence value reaches or exceeds this threshold, then a cut
is deemed to have taken place, and output will be generated.

How do you choose a threshold? It is a rather inexact science (as is the
subjective decision of whether something consitutes a shot change!) - you really
need to get a feel for it experimentally. As a rough guide, values between 0.8
and 0.9 are usually reasonable, depending on the type of video material.

Because of the necessary signal processing, this component has a delay of
several frames of data through it before you will get output. It therefore will
not necessarily detect cuts in the first 15 frames or so of a sequence sent to
it. Neither will it generate any output for the last 15 frames or so - they
will never make it through the internal signal processing.

Send a producerFinished() or shutdownMicroprocess() message to this component's
"control" inbox and it will immediately terminate. It will also forward on the
message out of its "signal" outbox.



Implementation details
----------------------

The algorithm used is based on a simple "mean absolute difference" between pixels
of one frame and the next; with some signal processing on the resulting stream
of frame-to-frame difference values, to detect a spike possibly indicating a
shot change.

The algorithm is courtesy of Jim Easterbrook of BBC Research. It is also
available in its own right as an independent open source library
`here<http://sourceforge.net/projects/shot-change>`_.

As signal processing is done on the confidence values internally to emphasise
spikes - which are likely to indicate a sudden increase in the level of change
from one frame to the next - a conseuqence is that this component
internally buffers inter-frame difference values for several frames, resulting
in a delay of about 15 frames through this component. This is the reason why
it is necessary to pair up video frames with a frame number, otherwise you
cannot guarantee being able to match up the resulting detected cuts with the
actual frame where they took place!

The change detection algorithm only looks at the Y (luminance) data in the video
frame.



=========================
UNCOMPRESSED FRAME FORMAT
=========================

A frame is a dictionary data structure. It must, for this component, at minimum
contain a key "yuv" that returns a tuple containing (y_data, u_data, v_data).

Any other entries are ignored.

"""

from Kamaelia.Support.Optimised.Video.ComputeMeanAbsDiff import ComputeMeanAbsDiff

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

import math


class DetectShotChanges(component):
    """\
    DetectShotChanges([threshold]) -> new DetectShotChanges component.
    
    Send (framenumber, videoframe) tuples to the "inbox" inbox. Sends out
    (framenumber, confidence) to its "outbox" outbox when a cut has probably
    occurred in the video sequence.
    
    Keyword arguments:
        
    - threshold  -- threshold for the confidence value, above which a cut is detected (default=0.9)
    """
    
    def __init__(self, threshold=0.9):
        super(DetectShotChanges,self).__init__()
        
        self.C0     = [0.0] * 2    # 'cut' signal
        self.C1     = [0.0] * 2    # 'standard converted cut' signal
        self.MAD    = [0.0] * 10   # mean absolute difference
        self.thresh = [0.0] * 11   # threshold based on local activity
        
        self.fnum   = [None] * 11  # frame number history
        self.ydata  = [""] * 2     # frame luminance data
        
        self.validframes = 0       # how many valid frames we've seen
        
        self.threshold = threshold
        
        
    def main(self):
        """Main loop"""
        
        while 1:
            while self.dataReady("inbox"):
                (framenum, frame) = self.recv("inbox")
                confidence, framenum = self.detectCut(framenum, frame['yuv'][0])
                if confidence >= self.threshold:
                    self.send((framenum,confidence), "outbox")
                    
            while self.dataReady("control"):
                msg = self.recv("control")
                self.send(msg, "signal")
                if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                    return
                
            self.pause()
            yield 1
            
    
    def detectCut(self, framenum, ydata):
        # shuffle histories along
        self.C0.pop()
        self.C0.insert(0,None)
        self.C1.pop()
        self.C1.insert(0,None)
        self.MAD.pop()
        self.MAD.insert(0,None)
        self.thresh.pop()
        self.thresh.insert(0,None)
        self.fnum.pop()
        self.fnum.insert(0,framenum)
        self.ydata.pop()
        self.ydata.insert(0,ydata)
        
        self.validframes = min(self.validframes+1, 9999)
        
        # compute mean absolute difference
        if self.validframes >= 2:
            self.MAD[0] = ComputeMeanAbsDiff(self.ydata[0], self.ydata[1])
            
        # compute variable threshold
        self.thresh[0] = 1.3 * max(*self.MAD[0:5])
        
        # compute 'cut' signal
        if self.validframes >= 14:
            risingEdge  = (self.MAD[6] - self.thresh[7]) \
                          - max(0.0, self.MAD[7] - self.thresh[8])
            fallingEdge = (self.MAD[6] - self.thresh[1]) \
                          - max(0.0, self.MAD[5] - self.thresh[0])
            self.C0[0] = (risingEdge-fallingEdge)/2.0
            
        # compute 'standards converted cut' signal
        if self.validframes >= 15:
            risingEdge  = (self.MAD[7] - self.thresh[8]) \
                          - max(0.0, self.MAD[8] - self.thresh[9]) \
                          - max(0.0, self.MAD[7] - self.thresh[2])
            fallingEdge = (self.MAD[6] - self.thresh[1]) \
                          - max(0.0, self.MAD[5] - self.thresh[0]) \
                          - max(0.0, self.MAD[6] - self.thresh[7])
            self.C1[0] = (risingEdge-fallingEdge)/2.0
            
        if self.validframes >= 16:
            # mask signals to either a cut or sc cut but not both
            if self.C0[1]*5.0 >= max(self.C1[0], self.C1[1]):
                C0_Msk = self.C0[1]
            else:
                C0_Msk = 0.0
            if self.C1[0] > max(self.C0[0], self.C0[1]) * 5.0:
                C1_Msk = self.C1[0]
            else:
                C1_Msk = 0.0
            
            if C0_Msk > 0.0:
                confidence = (math.log(C0_Msk) + 0.1) / 4.6
                framenum = self.fnum[7]
                return confidence,framenum
                
            if C1_Msk > 0.0:
                confidence = (math.log(C1_Msk) + 0.1) / 4.6
                framenum = self.fnum[6]
                return confidence,framenum
                
        return -99,None

__kamaelia_components__  = ( DetectShotChanges )
