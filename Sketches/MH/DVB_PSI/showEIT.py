#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from Kamaelia.Device.DVB.Parse.ParseEventInformationTable import *
from Kamaelia.Device.DVB.Parse.ParseTimeAndDateTable import *
from Kamaelia.Device.DVB.Parse.PrettifyTables import *
from Kamaelia.Device.DVB.SoftDemux import DVB_SoftDemuxer
from Kamaelia.Device.DVB.Parse.ReassemblePSITables import ReassemblePSITables

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.Reading import RateControlledFileReader
from Kamaelia.Util.Console import ConsoleEchoer

import sys
sys.path.append("../Introspection")
from Profiling import FormattedProfiler

#TS_FILE = "2008-05-16 11.27.13 MUX1_EIT_TOT_TDT.ts"
import sys

if len(sys.argv) != 2:
    print "Usage:"
    print "    %s <ts_file_containing_eit>" % sys.argv[0]
    print
    sys.exit(1)
    
TS_FILE = sys.argv[1]


from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Splitter import Plug, PlugSplitter

def Tee(*destinations):
  splitter = PlugSplitter()
  plugs = {}
  i = 1
  for dest in destinations:
      plugs[str(i)] = Plug(splitter, dest)
      i = i + 1

  return Graphline(splitter = splitter, 
    linkages = {
      ("","inbox") : ("splitter", "inbox"),
      ("","control") : ("splitter", "control"),
      ("splitter", "outbox") : ("", "outbox"),
      ("splitter", "signal") : ("", "signal")
    },
    **plugs
    )

#Pipeline( FormattedProfiler(10.0, 1.0),
#          ConsoleEchoer(),
#        ).activate()


Pipeline( RateControlledFileReader(TS_FILE, "bytes", rate=2500000, chunksize=188, allowchunkaggregation=True),
#          Tee( 
#              Pipeline( DVB_SoftDemuxer({0x14 : ["outbox"]}),
#                        ReassemblePSITables(),
#                        ParseTimeAndDateTable(),
#                        PrettifyTimeAndDateTable(),
#                        ConsoleEchoer(),
#                      ),
#          ),
          DVB_SoftDemuxer({0x12 : ["outbox"]}),
          ReassemblePSITables(),
          ParseEventInformationTable_Subset(actual_presentFollowing=True),
          PrettifyEventInformationTable(),
          ConsoleEchoer()
        ).run()
