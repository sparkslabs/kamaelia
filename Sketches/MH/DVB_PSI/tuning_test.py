#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import dvb3
import dvb3.frontend
import dvb3.dmx

frequency = 505.833330
feparams = {
    "frequency" : frequency*1000000,
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "code_rate_HP" : dvb3.frontend.FEC_3_4,
    "code_rate_LP" : dvb3.frontend.FEC_3_4,
#    "guard_interval" : dvb3.frontend.GUARD_INTERVAL_1_32,
#    "hierarchy_information" :dvb3.frontend.HIERARCHY_NONE,
#    "transmission_mode" : dvb3.frontend.TRANSMISSION_MODE_2K,
#    "bandwidth" : dvb3.frontend.BANDWIDTH_8_MHZ
}



fe = dvb3.frontend.Frontend(0, blocking=0)



#params = dvb3.frontend.OFDMParameters(**feparams)
params = dvb3.frontend.OFDMParameters()
params.frequency = frequency * 1000 * 1000
for key in feparams:
    params.__dict__[key] = feparams[key]

# Start the tuning
fe.set_frontend(params)

print params

import time

def status(fes):
    o = []
    for (mask,name) in { dvb3.frontend.FE_HAS_SIGNAL  : "SIGNAL",
                         dvb3.frontend.FE_HAS_CARRIER : "CARRIER",
                         dvb3.frontend.FE_HAS_VITERBI : "VITERBI",
                         dvb3.frontend.FE_HAS_SYNC    : "SYNC",
                         dvb3.frontend.FE_HAS_LOCK    : "LOCK",
                         dvb3.frontend.FE_TIMEDOUT    : "TIMEDOUT",
                         dvb3.frontend.FE_REINIT      : "REINIT",
                       }.items():
        if fes & mask:
            o.append(name)
        else:
            o.append(" "*len(name))
    return " ".join(o)


while True:
    time.sleep(0.5)
    fes = fe.read_status()
    print "%8d    %s" % (fes, status(fes))
    print "%8f    %8f    %8f" % (fe.read_signal_strength(), fe.read_snr(), fe.read_ber())
    