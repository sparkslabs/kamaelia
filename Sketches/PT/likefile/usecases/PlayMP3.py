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
        

