#!/usr/bin/env python
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
=====================
Kamaelia Video Player
=====================

This is a command line tool that plays video clips - both the sound and
pictures.



Getting Started
---------------


Pre-requisites
~~~~~~~~~~~~~~

You must have an installed copy of the command line ffmpeg tool, which can be
obtained from here. Make sure you have all the codecs you need of course!


Running VideoPlayer.py
~~~~~~~~~~~~~~~~~~~~~~

Run it from the command line and you'll get usage information::

    > ./VideoPlayer.py

    Usage:

        ./VideoPlayer.py <videofile>

To play a video simply name the video file as the command line argument. For
example::

    ./VideoPlayer.py myvideofile.avi

VideoPlayer is rather rudimentary at the moment - there are no controls whilst
the video is playing. To quit, control-C the program from the command prompt.
"""

from Kamaelia.Util.Detuple import SimpleDetupler

from Kamaelia.Codec.YUV4MPEG import YUV4MPEGToFrame
from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay
try:

    from Kamaelia.Audio.PyMedia.Output import Output
except ImportError:
    print "Sorry, this code requires Pymedia to work."
    print "If you want to use this, you'll need to get that, install it and try again"
 
from Kamaelia.File.UnixProcess2 import UnixProcess2
from Kamaelia.Experimental.Chassis import Pipeline
from Kamaelia.Experimental.Chassis import Graphline
from Kamaelia.Experimental.Chassis import Carousel
from Kamaelia.Experimental.Chassis import InboxControlledCarousel

from Kamaelia.Util.RateFilter import ByteRate_RequestControl
from Kamaelia.Util.Detuple import SimpleDetupler
from Kamaelia.Util.TwoWaySplitter import TwoWaySplitter
from Kamaelia.Util.FirstOnly import FirstOnly
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.Util.PromptedTurnstile import PromptedTurnstile
from Kamaelia.Codec.WAV import WAVParser

from Kamaelia.Util.Console import ConsoleEchoer

from Kamaelia.UI.Pygame.Display import PygameDisplay

from Kamaelia.Video.PixFormatConversion import ToRGB_interleaved
from Kamaelia.UI.Pygame.VideoSurface import VideoSurface

import pygame

import sys
if len(sys.argv)!=2:
    sys.stderr.write("Usage:\n\n    "+sys.argv[0]+" <videofile>\n\n")
    sys.exit(1)
else:
    infile=sys.argv[1]
    infile=infile.replace(" ","\ ")



def FrameRateLimitedPlayback(player):
    def RateLimitedPlayback(frame):
        fps = frame["frame_rate"]
        x,y = tuple(frame["size"])
        print "Frames per second:",fps
        print "(width,height):",(x,y)
        
        pgd = PygameDisplay(width=x,height=y).activate()
        PygameDisplay.setDisplayService(pgd)

        return Graphline( \
            LIMIT = PromptedTurnstile(),
            RATE  = ByteRate_RequestControl(rate=fps, chunksize=1.0, allowchunkaggregation=False),
            PLAY  = player,
            linkages = {
                ("",      "inbox" ) : ("LIMIT", "inbox"),
                ("LIMIT", "outbox") : ("PLAY",  "inbox"),
                ("PLAY",  "outbox") : ("",      "outbox"),
                
                ("RATE", "outbox" ) : ("LIMIT", "next"),

                ("",      "control") : ("RATE",  "control"),
                ("RATE",  "signal" ) : ("LIMIT", "control"),
                ("LIMIT", "signal" ) : ("PLAY",  "control"),
                ("PLAY",  "signal" ) : ("",      "signal"),
            },
            boxsizes = {
                ("LIMIT","inbox") : 2,
            },
        )

    return Graphline(\
        SPLIT = TwoWaySplitter(),
        FIRST = FirstOnly(),
        PLAY  = Carousel(RateLimitedPlayback),
        linkages = {
            ("",      "inbox"  ) : ("SPLIT", "inbox"),
            ("SPLIT", "outbox" ) : ("FIRST", "inbox"),
            ("FIRST", "outbox" ) : ("PLAY",  "next"),
            
            ("SPLIT", "outbox2") : ("PLAY",  "inbox"),
            ("PLAY",  "outbox" ) : ("",      "outbox"),
        
            ("",      "control") : ("SPLIT", "control"),
            ("SPLIT", "signal" ) : ("FIRST", "control"),
            ("SPLIT", "signal2") : ("PLAY",  "control"),
            ("PLAY",  "signal" ) : ("",      "signal"),
        },
        boxsizes = {
            ("SPLIT","inbox") : 1,
        },
    )

Graphline( DECODE = UnixProcess2(
               "ffmpeg -i "+infile+" -f yuv4mpegpipe -y vidpipe.yuv -f wav -y audpipe.wav",
               outpipes={"vidpipe.yuv":"video","audpipe.wav":"audio"},
               buffersize=131072,
               ),
           VIDEO = Pipeline(
               1, YUV4MPEGToFrame(),
               FrameRateLimitedPlayback(VideoOverlay()),
               ),
           AUDIO = Graphline(
               PARSE = WAVParser(),
               OUT   = Carousel(lambda format :
                   Output(format['sample_rate'],format['channels'],format['sample_format'],maximumLag=0.5)),
               linkages = {
                   ("","inbox")         : ("PARSE","inbox"),
                   ("PARSE","outbox")   : ("OUT","inbox"),
                   ("PARSE","all_meta") : ("OUT","next"),
                          
                   ("","control")     : ("PARSE","control"),
                   ("PARSE","signal") : ("OUT","control"),
                   ("OUT", "signal")  : ("","signal"),
               },
               boxsizes = { ("PARSE","inbox") : 5, },
               ),
           DEBUG = ConsoleEchoer(),
           linkages = {
               ("DECODE", "video") : ("VIDEO", "inbox"),
               ("DECODE", "audio") : ("AUDIO", "inbox"),
               ("DECODE", "outbox") : ("DEBUG", "inbox"),
#               ("DECODE", "error") : ("DEBUG", "inbox"),
                       
               ("DECODE", "signal") : ("AUDIO", "control"),
               ("AUDIO", "signal") : ("VIDEO", "control"),
           },
        ).run()
