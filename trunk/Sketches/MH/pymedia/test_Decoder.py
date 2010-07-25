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
