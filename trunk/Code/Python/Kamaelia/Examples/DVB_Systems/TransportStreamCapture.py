#!/usr/bin/python
#
# This code is designed soley for the purposes of demonstrating the tools
# for timeshifting.
#
# Note this used PID 0x2000 to specify that the whole raw transport stream
# should be captured. NOT supported by all DVB-T tuner devices.

from Kamaelia.Device.DVB.Core import DVB_Multiplex
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.Writing import SimpleFileWriter

import dvb3

freq = 505.833330 # 529.833330   # 505.833330
feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "code_rate_HP" : dvb3.frontend.FEC_3_4,
    "code_rate_LP" : dvb3.frontend.FEC_3_4,
}

Pipeline(
   # FIXME: Hmm. Need to check whether 0x2000 is supported by freecom DVB-T stick
   # FIXME: If it isn't need to change this to grab the pids manually, as it used to.
   # FIXME: Though that could be a different example...
   DVB_Multiplex(freq, [0x2000],feparams), # BBC Multiplex 1, whole transport stream
   SimpleFileWriter("BBC_MUX_1.ts"),
).run()

# RELEASE: MH, MPS

