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

