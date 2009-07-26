#!/usr/bin/python

#
# Example from:
#
# http://www.kamaelia.org/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeAndDateTable
#

import dvb3

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Device.DVB.Core import DVB_Multiplex, DVB_Demuxer
from Kamaelia.Device.DVB.Parse.ReassemblePSITables import ReassemblePSITables
from Kamaelia.Device.DVB.Parse.ParseTimeAndDateTable import ParseTimeAndDateTable
from Kamaelia.Device.DVB.Parse.PrettifyTables import PrettifyTimeAndDateTable
from Kamaelia.Util.Console import ConsoleEchoer

FREQUENCY = 754.166670
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
