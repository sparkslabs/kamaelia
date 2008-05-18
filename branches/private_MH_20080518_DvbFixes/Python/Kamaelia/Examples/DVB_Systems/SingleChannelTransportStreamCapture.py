#!/usr/bin/python
#
# This code is designed soley for the purposes of demonstrating the tools
# for timeshifting.
#

from Kamaelia.Device.DVB.Core import DVB_Multiplex
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.Writing import SimpleFileWriter

feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "code_rate_HP" : dvb3.frontend.FEC_3_4,
    "code_rate_LP" : dvb3.frontend.FEC_3_4,
}

Pipeline(
   DVB_Multiplex(754-754+505.8, [640, 641], feparams), # BBC NEWS 24
   SimpleFileWriter("BBC_NEWS_24.ts")
).run()

# RELEASE: MH, MPS
