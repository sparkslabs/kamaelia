#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Example from:
#
# http://www.kamaelia.org/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeAndDateTable
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
