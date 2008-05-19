#!/usr/bin/env python
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""\
=========================================
Parsing Time Offset Tables in DVB streams
=========================================

ParseTimeOffsetTable parses a reconstructed PSI table from a DVB MPEG
Transport Stream, and outputs the current time and date in UTC (GMT) aswell as
the current time offset, and when the next change will be (due to daylight
saving).

The purpose of the TOT and details of the fields within in are defined in the
DVB SI specification, including the possible 'descriptor' fields that feature in
the table:

- ETSI EN 300 468 
  "Digital Video Broadcasting (DVB); Specification for Service Information (SI)
  in DVB systems"
  ETSI / EBU (DVB group)



Example Usage
-------------

A simple pipeline to receive, parse and display the Time Offset Table::

    FREQUENCY = 505.833330
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "coderate_HP" : dvb3.frontend.FEC_3_4,
        "coderate_LP" : dvb3.frontend.FEC_3_4,
    }
    
    TOT_PID = 0x14
    
    Pipeline( DVB_Multiplex(FREQUENCY, [TOT_PID], feparams),
              DVB_Demuxer({ TOT_PID:["outbox"]}),
              ReassemblePSITables(),
              ParseTimeOffsetDateTable(),
              PrettifyTimeOffsetDateTable(),
              ConsoleEchoer(),
            ).run()



Behaviour
---------

Send reconstructed PSI table 'sections' to the "inbox" inbox. When all sections
of the table have arrived, ParseTimeOffsetTable will parse the table and send it
out of its "outbox" outbox.

The table is output every time it is received. In practice a multiplex is likely
to transmit about 1 instance of this table per second, giving a reasonably
accurate measure of the current time.

The parsed table is sent out as a dictionary data structure, similar to this::

    {
        'table_type' : 'TOT',
        'country'    : 'GBR'
        'region'     : 0,
        'offset'     : (0, 0),
        'next'       : { 'when'  : [2007, 3, 25, 1, 0, 0],
                         'offset': (1, 0)
                       },
        'UTC_now'    : [2006, 12, 21, 16, 16, 8],
    }

If this data is sent on through a PrettifyTimeOffsetTable component, then the
equivalent output is a string of the following form::

    TOT received:
       DateTime now (UTC)         : 2006-12-21 16:16:08
       Current local offset (h,m) : 00:00
       Country & region in it     : GBR (0)
       Next change of offset:
           Changes to             : 01:00
           Changes on (y,m,d)     : 2007-03-25 01:00:00

Note that this not only includes the current date, time, location and offset
from UTC (GMT), but it also tells you when the next change of offset will happen
(due to Daylight Saving time) and what that new offset will be.

The above example output shows that it is currently 21st December 2006 16:16:08
GMT but that at 1am on 25th March 2007 it will change to GMT+0100.

If a shutdownMicroprocess or producerFinished message is received on the
"control" inbox, then it will immediately be sent on out of the "signal" outbox
and the component will then immediately terminate.

"""

from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess

from Kamaelia.Support.DVB.Descriptors import parseDescriptor
from Kamaelia.Support.DVB.CRC import dvbcrc
from Kamaelia.Support.DVB.DateTime import parseMJD, unBCD

TOT_PID = 0x14


class ParseTimeOffsetTable(component):
    """
    Parses a TOT table.
    
    Receives table sections from PSI packets. Outputs the current time and date
    (UTC) and time zone offset.
    
    """
    Inboxes = { "inbox"   : "DVB PSI Packets from a single PID containing a TOT table",
                "control" : "Shutdown signalling",
              }
    Outboxes = { "outbox" : "Current date and time (UTC) and time zone offset",
                 "signal" : "Shutdown signalling",
               }
               
    def __init__(self):
        super(ParseTimeOffsetTable,self).__init__()


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
                data = self.recv("inbox")

                # extract basic info from this PSI packet - enough to work
                # out what table it is; what section, and the version
                e = [ord(data[i]) for i in range(0,10) ]

                table_id = e[0]
                if table_id != 0x73:
                    continue

                syntax = e[1] & 0x80
                if syntax:
                    continue

                section_length = ((e[1]<<8) + e[2]) & 0x0fff

                if not dvbcrc(data[:3+section_length]):
                    continue
                
                timeNow = list( parseMJD((e[3]<<8) + e[4]) )
                timeNow.extend( [unBCD(e[5]), unBCD(e[6]), unBCD(e[7])] )
                
                descriptors_length = ((e[8]<<8) + e[9]) & 0x0fff
                i = 10
                descriptors_end = i + descriptors_length
                while i < descriptors_end:
                    (dtype,descriptor),i = parseDescriptor(i,data)
                    if descriptor['type'] == "local_time_offset":
                        table = { "table_type" : "TOT",
                                  "UTC_now"    : timeNow,
                                  "offset"     : descriptor['offset'],
                                  "next"       : { "offset" : descriptor['nextOffset'],
                                                   "when"   : descriptor['timeOfChange'],
                                                 },
                                  "country"    : descriptor['country'],
                                  "region"     : descriptor['region'],
                                }

                        self.send(table, "outbox")

            self.pause()
            yield 1


__kamaelia_components__ = ( ParseTimeOffsetTable, )

if __name__ == "__main__":
    
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    
    from Kamaelia.Device.DVB.Core import DVB_Multiplex, DVB_Demuxer
    from Kamaelia.Device.DVB.Parse.ReassemblePSITables import ReassemblePSITables
    from Kamaelia.Device.DVB.Parse.PrettifyTables import PrettifyTimeOffsetTable

    from Kamaelia.Device.DVB.NowNext import NowNextProgrammeJunctionDetect
    from Kamaelia.Device.DVB.NowNext import NowNextServiceFilter
    
    import dvb3.frontend
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "coderate_HP" : dvb3.frontend.FEC_3_4,
        "coderate_LP" : dvb3.frontend.FEC_3_4,
    }
    
    Pipeline( DVB_Multiplex(505833330.0/1000000.0, [0x2000], feparams),
              DVB_Demuxer({ TOT_PID:["outbox"]}),
              ReassemblePSITables(),
              ParseTimeOffsetTable(),
              PrettifyTimeOffsetTable(),
              ConsoleEchoer(),
            ).run()

