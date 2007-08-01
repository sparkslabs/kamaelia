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

from Audio.PyMedia.Output import Output
from Audio.Codec.PyMedia.Decoder import Decoder

test = 1

if test==1:
    from Kamaelia.File.Reading import RateControlledFileReader
    from Kamaelia.Chassis.Pipeline import Pipeline
    
    Pipeline( RateControlledFileReader("/home/matteh/music/Radiohead - Creep.mp3", readmode="bytes", rate=8*44100*2*2, chunksize=1024),
            Decoder("MP3"),
            Output(sample_rate=4*22050, channels=2, format="S16_LE"),
            ).run()

elif test==2:
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.File.Reading import PromptedFileReader
    
    Graphline( READER = PromptedFileReader("/home/matteh/music/Radiohead - Creep.mp3", readmode="bytes"),
            DECODE = Decoder("MP3"),
            OUTPUT = Output(sample_rate=2*22050, channels=2, format="S16_LE"),
            linkages = {
                ("READER", "outbox") : ("DECODE", "inbox"),
                ("DECODE", "outbox") : ("OUTPUT", "inbox"),
    
                ("DECODE", "needData") : ("READER", "inbox"),
    
                ("", "control") : ("READER", "control"),
                ("READER", "signal") : ("DECODE", "control"),
                ("DECODE", "signal") : ("OUTPUT", "control"),
                ("OUTPUT", "signal") : ("", "signal"),
            }
            ).run()
