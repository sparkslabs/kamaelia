#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This code is designed soley for the purposes of demonstrating the tools
# for timeshifting. For more than one channel the DVB_Demuxer doesn't seem
# to be realtime.
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

from Kamaelia.Device.DVB.Core import DVB_Demuxer
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.File.Writing import SimpleFileWriter

Graphline(
    SOURCE=ReadFileAdaptor("BBC_MUX_1.ts"),
    DEMUX=DVB_Demuxer({
        640: ["NEWS24"],
        641: ["NEWS24"],
        600: ["BBCONE"],
        601: ["BBCONE"],
        610: ["BBCTWO"],
        611: ["BBCTWO"],
        620: ["CBBC"],
        621: ["CBBC"],
        18:  ["NEWS24", "BBCONE"],# "BBCTWO", "CBBC"],
    }),
    NEWS24=SimpleFileWriter("news24.data"),
    BBCONE=SimpleFileWriter("bbcone.data"),
    BBCTWO=SimpleFileWriter("bbctwo.data"),
    CBBC=SimpleFileWriter("cbbc.data"),
    linkages={
       ("SOURCE", "outbox"):("DEMUX","inbox"),
       ("DEMUX", "NEWS24"): ("NEWS24", "inbox"),
       ("DEMUX", "BBCONE"): ("BBCONE", "inbox"),
       ("DEMUX", "BBCTWO"): ("BBCTWO", "inbox"),
       ("DEMUX", "CBBC"): ("CBBC", "inbox"),
    }
).run()

# RELEASE: MH, MPS
