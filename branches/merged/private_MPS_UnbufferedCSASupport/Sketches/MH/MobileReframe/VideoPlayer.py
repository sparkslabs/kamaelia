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
#

from Kamaelia.Util.Detuple import SimpleDetupler

import sys
sys.path.append("../Video/")
from YUV4MPEG import YUV4MPEGToFrame
from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay
from Kamaelia.Audio.PyMedia.Output import Output

import sys
from UnixProcess import UnixProcess
from Chassis import Pipeline,Graphline,Carousel
from StopSelector import StopSelector

from Kamaelia.Util.RateFilter import MessageRateLimit
sys.path.append("../audio/")
from WAV import WAVParser

from Kamaelia.Util.Console import ConsoleEchoer

infile="/home/matteh/Documents/Skylife presentation/Daily Politics.avi"
infile=infile.replace(" ","\ ")

Graphline( DECODE = UnixProcess(
               "ffmpeg -i "+infile+" -f yuv4mpegpipe -y vidpipe.yuv -f wav -y audpipe.wav",
               outpipes={"vidpipe.yuv":"video","audpipe.wav":"audio"}
               ),
           VIDEO = Pipeline(
               2,  YUV4MPEGToFrame(),
               50, MessageRateLimit(25,25),
               VideoOverlay(),
               ),
           AUDIO = Graphline(
               PARSE = WAVParser(),
               OUT   = Carousel(lambda format :
                           Output(format['sample_rate'],format['channels'],format['sample_format']), boxsize=5),
               linkages = {
                   ("","inbox")         : ("PARSE","inbox"),
                   ("PARSE","outbox")   : ("OUT","inbox"),
                   ("PARSE","all_meta") : ("OUT","next"),
                           
                   ("","control")     : ("PARSE","control"),
                   ("PARSE","signal") : ("OUT","control"),
                   ("OUT", "signal")  : ("","signal"),
               },
               boxsizes = { ("PARSE","inbox") : 2, },
               ),
           DEBUG = ConsoleEchoer(),
           linkages = {
               ("DECODE", "video") : ("VIDEO", "inbox"),
               ("DECODE", "audio") : ("AUDIO", "inbox"),
               ("DECODE", "outbox") : ("DEBUG", "inbox"),
                       
               ("DECODE", "signal") : ("AUDIO", "control"),
               ("AUDIO", "signal") : ("VIDEO", "control"),
           },
        ).run()
            
            
            
    
    
    