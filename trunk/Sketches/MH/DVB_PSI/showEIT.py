#!/usr/bin/env python

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
