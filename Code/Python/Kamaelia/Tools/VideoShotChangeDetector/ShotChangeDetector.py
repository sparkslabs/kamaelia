#!/usr/bin/env python;

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
==========================
Video Shot Change Detector
==========================

This is a simple command line tool to analyse a video file and output a list of
(probable) locations of cuts (shot-changes) in the video.

This can serve as useful input data to user controlled video manipulation or
editing applications where it is useful to be able to provide assistance to the
user in precisely identify where shot changes take place.



Getting Started
---------------

You must have an installed copy of the command line ffmpeg tool, which can be
obtained from here. Make sure you have all the codecs you need of course!

Run ShotChangeDetector.py from the command line and you'll get usage
information::

    > ./ShotChangeDetector.py

    Usage:

        ./ShotChangeDetector.py [--show] [threshold] videofile

    * threshold is a floating point value greater than zero (default=0.9)

So for example, if you run it with the following command line::

    > ./ShotChangeDetector.py myvideofile.avi

Then as the cut detector runs, XML listing the frame numbers of where probable
cuts (shot changes) have been detected will be sent to standard output, for
example::

    <?xml version="1.0" encoding="ISO-8859-1"?>

    <detected_cuts xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                      xsi:noNamespaceSchemaLocation="DetectedShotChanges.xsd">
        <cut frame="39" confidence="0.9469" />
        <cut frame="49" confidence="0.9820" />
        <cut frame="76" confidence="0.9009" />
        <cut frame="78" confidence="1.0142" />
        <cut frame="103" confidence="1.0033" />
        <cut frame="110" confidence="0.9777" />
        <cut frame="135" confidence="0.9613" />
        <cut frame="147" confidence="0.9953" />

            .... cut down for succinctness! ...

        <cut frame="45167" confidence="0.9209" />
        <cut frame="45168" confidence="0.9209" />
        <cut frame="45169" confidence="0.9209" />
        <cut frame="45170" confidence="0.9210" />
        <cut frame="45171" confidence="1.0389" />
    </detected_cuts>

The cuts are listed by frame number, starting from zero for the first frame.

The 'confidence' value is the confidence the algorithm has that what was
detected actually is a shot change. It is basically a measure of how much the
picture suddenly changed. The higher the value, the more likely it is to be a
shot change.



Options
-------

Sensitivity Threshold
~~~~~~~~~~~~~~~~~~~~~

You can specify the threshold value used for shot change detection. The default
is 0.9, meaning that any possible cuts with a confidence value of less than 0.9
are not output. Sensible values are probably about 0.75 or greater. The shot
change detector will not accept values less than or equal to zero.

Specify the threshold as a floating point value immediately before the video
filename, for example::

    > ./ShotChangeDetector.py 0.85 myvideofile.avi

The best choice of threshold value will vary depending of the type of video
content. The best way to choose is to experiment. Using 0.9 as the starting
point for this is probably a good idea.


Displaying the video
~~~~~~~~~~~~~~~~~~~~

You can optionally ask to be shown the video live (without sound unfortunately!)
as the shot change detection takes place. Use the ``--show`` command line option
to do this. For example:

    > ./ShotChangeDetector.py --show myvideofile.avi

The video will be rate limited to 25fps, irrespective of the actual frame rate
of the video. Detected shot changes will be sent to standard output as usual.

Bear in mind that becuase the detection algorithm needs to compare multiple
frames, the detected cuts will be output several frames after they were detected
- do not expect them to be displayed the moment the shot change happens in the
displayed video!
"""


from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

from Kamaelia.Video.DetectShotChanges import DetectShotChanges

import sys


class FormatOutput(component):
    def main(self):
        self.send('<?xml version="1.0" encoding="ISO-8859-1"?>\n\n', "outbox")

        self.send('<detected_cuts xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="DetectedShotChanges.xsd">\n',"outbox")
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
                        raise UserWarning("STOP")
                    else:
                        self.send(msg, "signal")

                    
                self.pause()
                yield 1
                    
        except UserWarning:
            self.send("</detected_cuts>\n\n","outbox")
            yield 1
            yield 1
            yield 1
            yield 1
            self.send(self.shutdownMsg,"signal")

if __name__=="__main__":
    
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Util.Detuple import SimpleDetupler
    
    from Kamaelia.Codec.YUV4MPEG import YUV4MPEGToFrame
    
    from Kamaelia.File.UnixProcess2 import UnixProcess2
    from Kamaelia.Util.TagWithSequenceNumber import TagWithSequenceNumber
    from Kamaelia.Experimental.Chassis import Pipeline
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
    
        Pipeline( UnixProcess2("ffmpeg -i "+infile+" -f yuv4mpegpipe -y /dev/stdout",32768),
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
            UnixProcess2("ffmpeg -i "+infile +" -f yuv4mpegpipe -y /dev/stdout"),
            2, YUV4MPEGToFrame(),
            50, MessageRateLimit(25,25),
            PublishTo("VIDEO"),
            Backplane("VIDEO"),
            StopSelector(waitForTrigger=True),
            ).activate()
            
        Pipeline(
            SubscribeTo("VIDEO"),
            TagWithSequenceNumber(),
            DetectShotChanges(threshold),
            FormatOutput(),
            ConsoleEchoer(),
            ).activate()
    
        Pipeline(
            SubscribeTo("VIDEO"),
            VideoOverlay()
            ).run()
    
    