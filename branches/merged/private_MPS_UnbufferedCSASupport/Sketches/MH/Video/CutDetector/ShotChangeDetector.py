#!/usr/bin/env python

# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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

from DetectShotChanges import DetectShotChanges


class FormatOutput(component):
    def main(self):
        self.send('<?xml version="1.0" encoding="ISO-8859-1"?>\n\n', "outbox")

        self.send('<detected_cuts xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="DetectedCuts.xsd">\n',"outbox")
        try:
            while 1:
                while self.dataReady("inbox"):
                    framenum,confidence = self.recv("inbox")
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

if __name__=="__main__":
    
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
        sys.stderr.write("Usage:\n\n    "+sys.argv[0]+" [--show] [threshold] videofile\n\n* threshold is a floating point value greater than zero (default=0.9)\n\n")
        sys.exit(1)
    
    
    infile=files[0].replace(" ","\ ")
    
    if not show:
        # simple cut detector
    
        Pipeline( UnixProcess("ffmpeg -i "+infile+" -f yuv4mpegpipe -y /dev/stdout",32768),
                2, YUV4MPEGToFrame(),
                1, TagWithSequenceNumber(),
                1, DetectShotChanges(threshold),
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
            CutDetector(threshold),
            FormatOutput(),
            ConsoleEchoer(),
            ).activate()
    
        Pipeline(
            SubscribeTo("VIDEO"),
            VideoOverlay()
            ).run()
    
    