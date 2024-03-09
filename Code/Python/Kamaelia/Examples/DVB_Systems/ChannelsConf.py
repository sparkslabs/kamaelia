#!/usr/bin/python
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
"""Example showing how to parse a channels.conf file and use that to tune
and record a programme, using Kamaelia.Support.DVB.ChannelsConf"""

import sys   
import time
import pprint

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Device.DVB.Core import DVB_Multiplex
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Support.DVB.ChannelsConf import read_channel_configs

chan_by_name, chan_by_service, chans_by_frequency = read_channel_configs("channels.conf")

print() 
print()
print( "This demo/test harness records a given channel by name, as listed in your" )
print( "channels.conf file" )
print( 

if len(sys.argv)<2:
    print( "You didn't ask for a particular channel..." )
    print( "I know about the following channels:" )
    print( "   " )
    for chan in chan_by_name.keys():
        print( "'"+chan+"'", )
        
    sys.exit(0)
channel = sys.argv[1]

print( "You want channel", channel)
print( "Using the following tuning info")
print()
pprint.pprint(chan_by_name[channel])
print()

chan_info = chan_by_name[channel]

if chan_info["apid"] + chan_info["vpid"] == 0:
    print( "Sorry, I can't determine the audio & video pids for that channel")
    sys.exit(0)

X=time.localtime()
str_stamp = "%d%02d%02d%02d%02d" % (X.tm_year,X.tm_mon,X.tm_mday,X.tm_hour,X.tm_min)
filename = channel+ "." + str_stamp +".ts"

print( "Recording", channel, "to", filename)

from Kamaelia.Device.DVB.Parse.ParseTimeAndDateTable import TDT_PID
from Kamaelia.Device.DVB.Parse.ParseEventInformationTable import EIT_PID

Pipeline(
   DVB_Multiplex(0, [chan_info["apid"], chan_info["vpid"], EIT_PID, TDT_PID], chan_info["feparams"]), # BBC NEWS CHANNEL
   SimpleFileWriter( filename )
).run()



