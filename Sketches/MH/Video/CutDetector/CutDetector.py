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
#

from ComputeMeanAbsDiff import ComputeMeanAbsDiff

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

import math


class CutDetector(component):
    
    def __init__(self, threshold=0.9):
        super(CutDetector,self).__init__()
        
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
                    self.send((confidence,framenum), "outbox")
                    
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

if __name__=="__main__":
    
    class FormatOutput(component):
        def main(self):
            self.send('<?xml version="1.0" encoding="ISO-8859-1"?>\n\n', "outbox")

            self.send('<detected_cuts xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="DetectedCuts.xsd">\n',"outbox")
            try:
                while 1:
                    while self.dataReady("inbox"):
                        confidence,framenum = self.recv("inbox")
                        output = '    <cut frame="%d" confidence="%.04f" />\n' % (framenum,confidence)
                        self.send(output, "outbox")
                        
                    while self.dataReady("control"):
                        msg = self.recv("control")
                        if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                            self.shutdownMsg=msg
                            raise "STOP"
                        else:
                            self.send(msg, "signal")

                        
                    self.pause()
                    yield 1
                        
            except "STOP":
                self.send("</detected_cuts>\n\n","outbox")
                yield 1
                yield 1
                yield 1
                yield 1
                self.send(self.shutdownMsg,"signal")
    
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Util.Detuple import SimpleDetupler
    
    import sys

    sys.path.append("../")
    from YUV4MPEG import YUV4MPEGToFrame
    
    sys.path.append("../../MobileReframe/")
    from UnixProcess import UnixProcess
    from TagWithSequenceNumber import TagWithSequenceNumber
    from Chassis import Pipeline
    from StopSelector import StopSelector
    
    
    show=False
    files=[]
    threshold=0.9
    
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.lower() in ["--show", "-s"]:
                show=True
            else:
                files.append(arg)
                
    if len(files) > 1:
        try:
            threshold = float(files[0])
        except ValueError:
            threshold = None
        files.pop(0)
    
    if len(files) != 1 or threshold is None or threshold<=0.0:
        sys.stderr.write("Usage:\n\n    CutDetector.py [--show] [threshold] videofile\n\n* threshold is a floating point value greater than zero (default=0.9)\n\n")
        sys.exit(1)
    
    
    infile=files[0].replace(" ","\ ")
    
    if not show:
        # simple cut detector
    
        Pipeline( UnixProcess("ffmpeg -i "+infile+" -f yuv4mpegpipe -y /dev/stdout",32768),
                2, YUV4MPEGToFrame(),
                1, TagWithSequenceNumber(),
                1, CutDetector(threshold),
                FormatOutput(),
                ConsoleEchoer(),
                StopSelector(waitForTrigger=True),
                ).run()
            
    else:
        # cut detector plus playback at the same time
        
        from Kamaelia.UI.Pygame.Display import PygameDisplay
        from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay
        from Kamaelia.Util.Backplane import Backplane,PublishTo,SubscribeTo
        from Kamaelia.Util.RateFilter import MessageRateLimit
        
        PygameDisplay.setDisplayService(PygameDisplay(width=1024,height=500).activate())
        
        Pipeline(
            UnixProcess("ffmpeg -i "+infile +" -f yuv4mpegpipe -y /dev/stdout"),
            2, YUV4MPEGToFrame(),
            50, MessageRateLimit(25,25),
            PublishTo("VIDEO"),
            Backplane("VIDEO"),
            StopSelector(waitForTrigger=True),
            ).activate()
            
        Pipeline(
            SubscribeTo("VIDEO"),
            TagWithSequenceNumber(),
            CutDetector(0.8),
            FormatOutput(),
            ConsoleEchoer(),
            ).activate()
    
        Pipeline(
            SubscribeTo("VIDEO"),
            VideoOverlay()
            ).run()
    
    