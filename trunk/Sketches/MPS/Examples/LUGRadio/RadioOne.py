#!/usr/bin/python
#
# This code is designed soley for the purposes of demonstrating the tools
# for timeshifting.
#

from Kamaelia.Device.DVB.Core import DVB_Multiplex
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.Writing import SimpleFileWriter
import dvb3

# Transmitters for Wolverhampton:
# The Wrekin
# The WrekinB
# Sutton Coldfields

freq = 850.166670
feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "coderate_HP" : dvb3.frontend.FEC_3_4,
    "coderate_LP" : dvb3.frontend.FEC_3_4,
}

Pipeline(
   DVB_Multiplex(freq, [6210], feparams), # RADIO ONE
   SimpleFileWriter("RADIO_ONE.ts")
).run()
