#!/usr/bin/python
#
# This code is designed soley for the purposes of demonstrating the tools
# for timeshifting.
#

from Kamaelia.Device.DVB.Core import DVB_Multiplex
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.Writing import SimpleFileWriter

import dvb3.frontend

import time

feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "code_rate_HP" : dvb3.frontend.FEC_3_4,
    "code_rate_LP" : dvb3.frontend.FEC_3_4,                                
}

Pipeline(
   DVB_Multiplex(505.833330, [0x12, 0x14], feparams), # capture EIT and TOT and TDT
   SimpleFileWriter("%04d-%02d-%02d %02d.%02d.%02d MUX1_EIT_TOT_TDT.ts" % time.localtime()[0:6])
).run()

# RELEASE: MH, MPS
