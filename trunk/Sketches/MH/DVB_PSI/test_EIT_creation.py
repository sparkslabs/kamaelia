#!/usr/bin/env python
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
    
        