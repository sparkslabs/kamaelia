#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This code is designed soley for the purposes of demonstrating the tools
# for timeshifting.
#
# Note this used PID 0x2000 to specify that the whole raw transport stream
# should be captured. NOT supported by all DVB-T tuner devices.
#
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
#


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

