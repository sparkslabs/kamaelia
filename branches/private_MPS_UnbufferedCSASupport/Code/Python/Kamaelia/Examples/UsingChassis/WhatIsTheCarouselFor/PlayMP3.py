#!/usr/bin/env python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

from Kamaelia.File.Reading import RateControlledFileReader
from Kamaelia.Audio.Codec.PyMedia.Decoder import Decoder
from Kamaelia.Audio.PyMedia.Output import Output
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Carousel import Carousel

import sys
if len(sys.argv) != 2:
    sys.stderr.write("Usage:\n\n    PlayMP3.py <filename>\n\n")
    sys.exit(1)
    
filename=sys.argv[1]

def makeAudioOutput(metadata):
  return Output( metadata["sample_rate"],
                 metadata["channels"],
                 metadata["format"]
               )

Graphline( READ = RateControlledFileReader( filename, readmode="bytes", rate=256000/8),
           DECODE = Decoder("mp3"),
           OUTPUT = Carousel( makeAudioOutput ),
           linkages = {
               ("READ",   "outbox") : ("DECODE", "inbox"),
               ("DECODE", "outbox") : ("OUTPUT", "inbox"),
               ("DECODE", "format") : ("OUTPUT", "next"),
               
               ("READ",   "signal") : ("DECODE", "control"),
               ("DECODE", "signal") : ("OUTPUT", "control"),
           }
         ).run()
        

