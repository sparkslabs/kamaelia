#!/usr/bin/python
#
# This code is designed soley for the purposes of demonstrating the tools
# for timeshifting.
#

from Kamaelia.Device.DVB.Core import DVB_Multiplex
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.Writing import SimpleFileWriter
import dvb3

freq = 505.833330 # 529.833330   # 505.833330
feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "coderate_HP" : dvb3.frontend.FEC_3_4,
    "coderate_LP" : dvb3.frontend.FEC_3_4,
}

#freq = 754.166670
#feparams = {
#    "inversion" : dvb3.frontend.INVERSION_AUTO,
#    "constellation" : dvb3.frontend.QAM_16,
#    "coderate_HP" : dvb3.frontend.FEC_3_4,
#    "coderate_LP" : dvb3.frontend.FEC_3_4,
#}

# SOURCE=DVB_Multiplex(freq, pids["BBC TWO"]+pids["EIT"], feparams), # BBC Channels + EIT dat
Pipeline(
   DVB_Multiplex(freq, [620, 621,18], feparams), # BBC THREE
   SimpleFileWriter("BBC_THREE.ts")
).run()

# RELEASE: MH, MPS
