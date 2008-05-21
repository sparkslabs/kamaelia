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
===========================================
Parsing Time And Date Tables in DVB streams
===========================================

ParseTimeAndDateTable parses a reconstructed PSI table from a DVB MPEG
Transport Stream, and outputs the current time and date in UTC (GMT).

The purpose of the TDT and details of the fields within in are defined in the
DVB SI specification:

- ETSI EN 300 468 
  "Digital Video Broadcasting (DVB); Specification for Service Information (SI)
  in DVB systems"
  ETSI / EBU (DVB group)

The Time Offset Table (TOT) additionally contains information on the current
(and next) timezone offset that applies, as well as duplicating the datetime
information. See ParseTimeOffsetTable component.


Example Usage
-------------

A simple pipeline to receive, parse and display the Time and Date Table::

    FREQUENCY = 505.833330
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "code_rate_HP" : dvb3.frontend.FEC_3_4,
        "code_rate_LP" : dvb3.frontend.FEC_3_4,
    }
    
    TDT_PID = 0x14
    
    Pipeline( DVB_Multiplex(FREQUENCY, [TDT_PID], feparams),
              DVB_Demuxer({ TDT_PID:["outbox"]}),
              ReassemblePSITables(),
              ParseTimeAndDateTable(),
              PrettifyTimeAndDateTable(),
              ConsoleEchoer(),
            ).run()

The output will look like this::

    [2006, 12, 21, 15, 1, 3]
    [2006, 12, 21, 15, 1, 4]
    [2006, 12, 21, 15, 1, 5]
    [2006, 12, 21, 15, 1, 6]

    .....



Behaviour
---------

Send reconstructed PSI table 'sections' to the "inbox" inbox. When all sections
of the table have arrived, ParseServiceDescriptionTable will parse the table and
send it out of its "outbox" outbox.

The table is output every time it is received. In practice a multiplex is likely
to transmit about 1 instance of this table per second, giving a reasonably
accurate measure of the current time.

The value output is a simple list/tuple describing the current UTC (GMT) date
and time, in the form (year,month,day,hour,minute,second).

For example: 21st December 2006 15:01:03 GMT is represented as::

    [2006, 12, 21, 15, 1, 3]

If this data is sent on through a PrettifyTimeAndDateTable component, then the
equivalent output is a string of the following form::

    TDT received:
       UTC Date now (y,m,d) : 2006 12 21
       UTC Time now (h,m,s) : 15:01:03

If a shutdownMicroprocess or producerFinished message is received on the
"control" inbox, then it will immediately be sent on out of the "signal" outbox
and the component will then immediately terminate.

"""

from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess

from Kamaelia.Support.DVB.Descriptors import parseDescriptor
from Kamaelia.Support.DVB.CRC import dvbcrc
from Kamaelia.Support.DVB.DateTime import parseMJD, unBCD


TDT_PID = 0x14


class ParseTimeAndDateTable(component):
    """\
    ParseTimeAndDateTable() -> new ParseTimeAndDateTable component.

    Send reconstructed PSI table sections to the "inbox" inbox. When a complete
    table is assembled and parsed, the result is sent out of the "outbox" outbox
    in the form [year,month,day,hour,minute,second]. The times are UTC (GMT).
    """
    Inboxes = { "inbox" : "DVB PSI Packets from a single PID containing a TDT table",
                "control" : "Shutdown signalling",
              }
    Outboxes = { "outbox" : "Current date and time (UTC)",
                 "signal" : "Shutdown signalling",
               }
               
    def __init__(self):
        super(ParseTimeAndDateTable,self).__init__()


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
                e = [ord(data[i]) for i in range(0,3) ]

                table_id = e[0]
                if table_id != 0x70:
                    continue

                syntax = e[1] & 0x80
                if syntax:
                    continue

                # now were reasonably certain we've got a correct packet
                # we'll convert the rest of the packet
                section_length = ((e[1]<<8) + e[2]) & 0x0fff

                e = [ord(data[i]) for i in range(0,8) ]
                
                utc = list( parseMJD((e[3]<<8) + e[4]) )
                utc.extend( [unBCD(e[5]), unBCD(e[6]), unBCD(e[7])] )

                self.send(utc, "outbox")

            self.pause()
            yield 1


__kamaelia_components__ = ( ParseTimeAndDateTable, )

if __name__ == "__main__":
    
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    
    from Kamaelia.Device.DVB.Core import DVB_Multiplex, DVB_Demuxer
    from Kamaelia.Device.DVB.Parse.ReassemblePSITables import ReassemblePSITables
    from Kamaelia.Device.DVB.Parse.PrettifyTables import PrettifyTimeAndDateTable

    import dvb3.frontend
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "code_rate_HP" : dvb3.frontend.FEC_3_4,
        "code_rate_LP" : dvb3.frontend.FEC_3_4,
    }
    
    Pipeline( DVB_Multiplex(505833330.0/1000000.0, [0x2000], feparams),
              DVB_Demuxer({ TDT_PID:["outbox"]}),
              ReassemblePSITables(),
              ParseTimeAndDateTable(),
              PrettifyTimeAndDateTable(),
              ConsoleEchoer(),
            ).run()

