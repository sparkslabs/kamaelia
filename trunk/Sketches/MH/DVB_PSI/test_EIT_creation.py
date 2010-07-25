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
# -------------------------------------------------------------------------


from CreatePSI import SerialiseEITSection
from Axon.Component import component

class CreateEventInformationTable(component):
    def __init__(self):
        super(CreateEventInformationTable,self).__init__()
        self.serialiser = SerialiseEITSection()
        
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True
        return False

    def main(self):
        while not self.shutdown():
            
            while self.dataReady("inbox"):
                section = self.recv("inbox")
                serialisedSection = self.serialiser.serialise(section)
                self.send(serialisedSection,"outbox")
            
            self.pause()
            yield 1


if __name__ == "__main__":
    
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.File.Reading import RateControlledFileReader
    from Kamaelia.Device.DVB.Core import DVB_Demuxer
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Device.DVB.Parse.ParseEventInformationTable import ParseEventInformationTable_Subset
    from Kamaelia.Device.DVB.Parse.PrettifyTables import PrettifyEventInformationTable
    from Kamaelia.Device.DVB.SoftDemux import DVB_SoftDemuxer
    from Kamaelia.Device.DVB.Parse.ReassemblePSITables import ReassemblePSITables
    from Kamaelia.Util.PureTransformer import PureTransformer
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Util.Comparator import Comparator
    from Kamaelia.Util.Splitter import Plug, PlugSplitter
    from Kamaelia.Util.PassThrough import PassThrough
    from Kamaelia.File.Writing import SimpleFileWriter
    
    TS_FILE = "/home/matteh/dvb/2008-05-16 11.27.13 MUX1_EIT_TOT_TDT.ts"
    
#    def AddInVersion():
#        def transf(x):
#            x["version"] = 0
#            return x
#        return PureTransformer(transf)
    
    print "run a diff over the two output files to compare the results"
    
    splitter=PlugSplitter()
    
    Pipeline(
        RateControlledFileReader(TS_FILE, readmode="bytes", rate=1000*1000, chunksize=188),
        DVB_SoftDemuxer( {0x12:["outbox"]} ),
        ReassemblePSITables(),
        ParseEventInformationTable_Subset( \
            actual_presentFollowing = True,
            other_presentFollowing = True,
            actual_schedule = True,
            other_schedule = True,
            ),
        splitter
    ).activate()
    
    Plug(splitter, Pipeline(
        PrettifyEventInformationTable(),
        SimpleFileWriter("original_eit_parsed.text"),
    )).activate()
    
    Plug(splitter, Pipeline(
        CreateEventInformationTable(),
        ParseEventInformationTable_Subset( \
            actual_presentFollowing = True,
            other_presentFollowing = True,
            actual_schedule = True,
            other_schedule = True,
            ),
        PrettifyEventInformationTable(),
        SimpleFileWriter("regenerated_eit_parsed.text"),
    )).run()
    
        