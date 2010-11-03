#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This code is designed soley for the purposes of demonstrating the tools
# for timeshifting.
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
#

import time
import dvb3
from Kamaelia.Device.DVB.Core import DVB_Demuxer,DVB_Multiplex
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.File.Reading import RateControlledFileReader
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Apps.Macro.Macro import ChannelTranscoder

location = "manchester"

if location == "london": # Crystal Palace
    freq = 505.833330 # 529.833330   # 505.833330
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "code_rate_HP" : dvb3.frontend.FEC_3_4,
        "code_rate_LP" : dvb3.frontend.FEC_3_4,
    }
elif location == "manchester": # WinterHill
    freq = 754.166670
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "code_rate_HP" : dvb3.frontend.FEC_3_4,
        "code_rate_LP" : dvb3.frontend.FEC_3_4,
    }

params={}
params["LO"] = {
    "mencoder_options" : " -ovc lavc -oac mp3lame -ffourcc DX50 -lavcopts acodec=mp3:vbitrate=200:abitrate=128 -vf scale=320:-2 -",
    "dir_prefix" : "200",
    }
params["HI"] = {
    "mencoder_options" : " -ovc lavc -oac mp3lame -ffourcc DX50 -lavcopts acodec=mp3:vbitrate=512:abitrate=128 -vf scale=640:-2 -",
    "dir_prefix" : "512"
    }

pids = { "BBC ONE" : [600,601],
         "BBC TWO" : [610,611],
         "CBEEBIES": [201,401],
         "CBBC"    : [620,621],
         "EIT"     : [18],
       }

service_ids = { "BBC ONE": 4164,
                "BBC TWO": 4228,
                "CBEEBIES":16960,
                "CBBC":4671,
              }

print "-----STARTING MACRO----- time =",time.time()

Graphline(
    SOURCE=DVB_Multiplex(freq, pids["BBC TWO"]+pids["EIT"], feparams), # BBC Channels + EIT data
    DEMUX=DVB_Demuxer({
        610: ["BBCTWO"],
        611: ["BBCTWO"],
        18: ["BBCTWO"],   # BBCONE","BBCONE_2","BBCTWO","BBCTWO_2", "CBEEBIES"
    }),
    BBCTWO_HI = ChannelTranscoder(service_ids["BBC TWO"], **params["HI"]),
    linkages={
       ("SOURCE", "outbox"):("DEMUX","inbox"),
       ("DEMUX", "BBCTWO"): ("BBCTWO_HI", "inbox"),
    }
).run()

# RELEASE: MH, MPS
