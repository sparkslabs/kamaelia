#!/usr/bin/python
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

print 
print
print "This demo/test harness records a given channel by name, as listed in your"
print "channels.conf file"
print 

if len(sys.argv)<2:
    print "You didn't ask for a particular channel..."
    print "I know about the following channels:"
    print "   "
    for chan in chan_by_name.keys():
        print "'"+chan+"'",
        
    sys.exit(0)
channel = sys.argv[1]

print "You want channel", channel
print "Using the following tuning info"
print
pprint.pprint(chan_by_name[channel])
print

chan_info = chan_by_name[channel]

if chan_info["apid"] + chan_info["vpid"] == 0:
    print "Sorry, I can't determine the audio & video pids for that channel"
    sys.exit(0)

X=time.localtime()
str_stamp = "%d%02d%02d%02d%02d" % (X.tm_year,X.tm_mon,X.tm_mday,X.tm_hour,X.tm_min)
filename = channel+ "." + str_stamp +".ts"

print "Recording", channel, "to", filename

Pipeline(
   DVB_Multiplex(0, [chan_info["apid"], chan_info["vpid"]], chan_info["feparams"]), # BBC NEWS CHANNEL
   SimpleFileWriter( filename )
).run()



