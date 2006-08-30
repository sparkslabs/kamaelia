#!/usr/bin/env python
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

from Axon.Component import component

from AudioFrameMarshalling import AudioFrameMarshaller, AudioFrameDeMarshaller
from Kamaelia.Util.RateFilter import VariableByteRate_RequestControl as VariableRateControl
from Kamaelia.File.Reading import PromptedFileReader as ReadFileAdapter

from AudioDecoder import AudioDecoder
from SoundOutput import SoundOutput

from Kamaelia.Util.PipelineComponent import pipeline

filepath = "/opt/kde3/share/apps/khangman/sounds/new_game.ogg"
extn = filepath[-3:].lower()

class BitRateExtractor(component):
    Inboxes  = { "inbox":"",  "control":"" }
    Outboxes = { "outbox":"", "signal":"", "bitratechange":""  }

    def __init__(self):
        super(BitRateExtractor, self).__init__()
        self.bitrate = None

    def main(self):
        while not self.dataReady("control"):
            yield 1
            while self.dataReady("inbox"):
                frame = self.recv("inbox")
                if frame.bitrate != self.bitrate:
                    self.bitrate = frame.bitrate
                    self.send( self.bitrate, "bitratechange" )
                self.send( frame, "outbox" )
                
        self.send( self.recv("control"), "signal")

rc = VariableRateControl(rate=4096, chunksize=1024)
rfa = ReadFileAdapter(filename=filepath, readmode="bytes")
be = BitRateExtractor()

p=pipeline(rc,
         rfa,
         AudioDecoder(extn),
         be,
         AudioFrameMarshaller(),
         AudioFrameDeMarshaller(),
         SoundOutput()
        )

rc.link( (be, "bitratechange"), (rc, "inbox") )

p.link( (p, "signal"), (p, "control") )  # loopback for shutdown of RC

p.activate()
p.run()

