#!/usr/bin/python
#
# This code is designed soley for the purposes of demonstrating the tools
# for timeshifting.
#

from Kamaelia.Device.DVB.Core import DVB_Multiplex
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.File.Writing import SimpleFileWriter

import dvb3

freq = 505.833330 # 529.833330   # 505.833330
feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "coderate_HP" : dvb3.frontend.FEC_3_4,
    "coderate_LP" : dvb3.frontend.FEC_3_4,
}

pipeline(
   DVB_Multiplex(freq, [0x2000],feparams), # BBC Multiplex 1, whole transport stream
   SimpleFileWriter("BBC_MUX_1.ts"),
).run()
