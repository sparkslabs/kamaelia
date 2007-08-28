#!/usr/bin/python
#
# This code is designed soley for the purposes of demonstrating the tools
# for timeshifting.
#

import sys
import time
import dvb3
import Axon
from Kamaelia.Device.DVB.Core import DVB_Multiplex
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.Writing import SimpleFileWriter

freq = 834.166670
feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_64,
    "coderate_HP" : dvb3.frontend.FEC_2_3,
    "coderate_LP" : dvb3.frontend.FEC_1_2,
}


print sys.argv
if len(sys.argv)>1:
    channels = [ int(x) for x in sys.argv[1:] ]
else:
    channels = [600,601,18]

print "RECORDING CHANNELS", channels

class DieAtTime(Axon.Component.component):
    delay = 10
    def main(self):
        now = time.time()
        while 1:
            if (time.time() -now) >self.delay:
                raise "AARRRRGGGHHH"
            yield 1

DieAtTime(delay=7500).activate()
Pipeline(
   DVB_Multiplex(freq, channels, feparams), # BBC TWO
   SimpleFileWriter("Programme"+str(channels)+(str(time.time()))+".ts")
).run()

# RELEASE: MH, MPS
