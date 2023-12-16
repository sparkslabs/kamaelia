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
# -------------------------------------------------------------------------
"""\
======================================================
Support functions for parsing a DVB channels.conf file
======================================================



Example Usage
-------------

A simple application to record a DVB Channel by a given name. ::
    
    import sys   
    import pprint
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Device.DVB.Core import DVB_Multiplex
    from Kamaelia.File.Writing import SimpleFileWriter
    from Kamaelia.Support.DVB.ChannelsConf import read_channel_configs

    if len(sys.argv)<2:
        print ("You didn't ask for a particular channel...")
        sys.exit(0)
    channel = sys.argv[1]

    chan_by_name, chan_by_service, chans_by_frequency = read_channel_configs("channels.conf")

    print ("Tuning info for", channel, "\n", pprint.pformat(chan_by_name[channel]))

    chan_info = chan_by_name[channel]

    if chan_info["apid"] + chan_info["vpid"] == 0:
        print ("Sorry, I can't determine the audio & video pids for that channel")
        print ("If this code was more intelligent it could parse the service description table, but it isn't")
        sys.exit(0)

    Pipeline(
       DVB_Multiplex(0, [chan_info["apid"], chan_info["vpid"]], chan_info["feparams"]),
       SimpleFileWriter(channel+ ".ts")
    ).run()            

This tunes to a given channel, and dumps out a file with the channel
therein. (or rather the specified audio & video pids)


How To Use
----------

If should be clear from this that the key API here is the following
function call::

    chan_by_name, chan_by_service, chans_by_frequency = read_channel_configs("channels.conf")


This searches some sensible places for a channels.conf file::

    .                (cwd)
    ~                (home)
    ~/.kamaelia
    /usr/local/etc/
    /etc/

As well as some known other locations::

    /usr/local/etc/mplayer/
    /etc/mplayer/

It then parses the contents to get channel definitions. It then provides 3
lookup mechanisms for channels.

Channel Definition
------------------

An example, parsed, channel definition looks like this::

    {'apid': 402,
     'bandwidth': 0,
     'code_rate_HP': 2,
     'code_rate_LP': 1,
     'constellation': 3,
     'feparams': {'bandwidth': 0,
                  'code_rate_HP': 2,
                  'code_rate_LP': 1,
                  'constellation': 3,
                  'frequency': 801833000,
                  'guard_interval': 0,
                  'hierarchy_information': 0,
                  'inversion': 2,
                  'transmission_mode': 1},
     'freq_mhz': 801.83299999999997,
     'frequency': 801833000,
     'guard_interval': 0,
     'hierarchy_information': 0,
     'inversion': 2,
     'name': 'CBeebies',
     'serviceid': 4672,
     'transmission_mode': 1,
     'vpid': 401}

Obviously some information is duplicated here. This is a temporary measure
at present. The primary reason for the duplication is so that you can tune 
a DVB front end as follows::

    chan_by_name, chan_by_service, chans_by_frequency = read_channel_configs("channels.conf")

    fe = dvb3.frontend.Frontend(0)
    build_params_type = fe.get_dvbtype()
    params = build_params_type(**chan_by_name["BBC ONE"]["feparams"])

Or more practically::

    chan_by_name, chan_by_service, chans_by_frequency = read_channel_configs("channels.conf")

    chan_info = chan_by_name["BBC ONE"]

    Pipeline(
       DVB_Multiplex(0, [chan_info["apid"], chan_info["vpid"]], chan_info["feparams"]),
       SimpleFileWriter(channel+ "." + str_stamp +".ts")
    ).run()


How does it Work?
-----------------

Details to be written.


References
----------

To be written.

"""
raise NotImplementedError("Due to drift/bit rot, DVB libraries need updating")

import dvb3.frontend
import os.path

debug = False

search_path = [
      ".",
      os.path.expanduser("~"),
      os.path.expanduser("~/.kamaelia"),
      "/usr/local/etc/",
      "/etc/"
]

def open_config(config_file, extra_search = []):
    f = None
    for path in search_path + extra_search:
        try:
            f = open(os.path.join(path,config_file))
            if debug:
                print ("Opened", config_file, "from", path)
            break # Successfully opened a config file
        except IOError:
            e = sys.exc_info()[1]
            if e.errno !=2:
                raise

    if f == None:
        raise IOError("No " +str(config_file) +" file found on search path")

    return f

def read_config(config_file, extra_search = []):
    f = open_config(config_file, extra_search)
    slurp = f.read()
    f.close()   
    return slurp

def getdvb(symbol, default=None):
    if default:
        try:
            R = getattr(dvb3.frontend, symbol)
            # print ("    symbol", symbol, R)
            return R
        except AttributeError:
            # print ("----default", symbol, default)
            return default
    else:
        return getattr(dvb3.frontend, symbol)

def tokenise_channels_config(raw_config):
    raw_chans = raw_config.split("\n")
    unparsed_chans = [ x.split(":") for x in raw_chans if x != ""]
    return unparsed_chans

def parse_channel_config(unparsed_chans):

    chan_by_name = {}
    chan_by_service = {}
    chans_by_frequency = {}

    for chan in unparsed_chans:
        name = chan[0].lower()
        freq_mhz = int(chan[1])/1000000.0    # Frequency in MHz
        frequency = int(chan[1])             # No processing   
        inversion    = getdvb(chan[2], dvb3.frontend.INVERSION_AUTO)
        bandwidth    = getdvb(chan[3], dvb3.frontend.BANDWIDTH_AUTO)  # Bandwidth in MHz
        code_rate_HP = getdvb(chan[4], dvb3.frontend.FEC_AUTO)
        code_rate_LP = getdvb(chan[5], dvb3.frontend.FEC_AUTO)
        constellation = getdvb(chan[6], dvb3.frontend.QAM_AUTO) # QAM setting
        transmission_mode = getdvb(chan[7], dvb3.frontend.TRANSMISSION_MODE_AUTO)
        guard_interval = getdvb(chan[8], dvb3.frontend.GUARD_INTERVAL_AUTO)
        hierarchy = getdvb(chan[9], dvb3.frontend.HIERARCHY_NONE)
        vpid =  int(chan[10])
        apid =  int(chan[11])         # Apid and Vpid are incomplete, but starting points
        serviceid = int(chan[12])
        channel_summary = {
            "name" : name, 
            "freq_mhz" : freq_mhz,
            "frequency" : frequency,
            "inversion" : inversion,
            "bandwidth" : bandwidth,
            "code_rate_HP" : code_rate_HP,
            "code_rate_LP" : code_rate_LP,
            "constellation" : constellation,
            "transmission_mode" : transmission_mode,
            "guard_interval" : guard_interval,
            "hierarchy_information" : hierarchy,
            "vpid" : vpid,
            "apid" : apid,
            "serviceid" : serviceid,
        }
        #
        feparams = dict(channel_summary)
        feparam_fields = [ "frequency", "inversion", "bandwidth",
                           "code_rate_HP","code_rate_LP", "constellation",
                           "transmission_mode","guard_interval", "hierarchy_information"]

        for arg in ["apid", "vpid", "serviceid", "freq_mhz", "name"]:
            del feparams[arg]

        channel_summary["feparams"] = feparams
        #
        chan_by_name[name] = channel_summary
        chan_by_service[serviceid] = channel_summary
        try:
            chans_by_frequency[frequency].append(channel_summary)
        except:
            chans_by_frequency[frequency] = [ channel_summary ]

    return chan_by_name, chan_by_service, chans_by_frequency

def read_channel_configs(filename = "channels.conf"):
    raw_config = read_config(filename, ["/usr/local/etc/mplayer/", "/etc/mplayer/"] )
    unparsed_chans = tokenise_channels_config(raw_config)
    chan_by_name, chan_by_service, chans_by_frequency = parse_channel_config(unparsed_chans)
    return chan_by_name, chan_by_service, chans_by_frequency


if __name__ == "__main__":
    import pprint
    import sys   
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Device.DVB.Core import DVB_Multiplex
    from Kamaelia.File.Writing import SimpleFileWriter
    import time

    chan_by_name, chan_by_service, chans_by_frequency = read_channel_configs("channels.conf")

    print ("") 
    print ("")
    print ("This demo/test harness records a given channel by name, as listed in your")
    print ("channels.conf file")
    print ("")
    
    if len(sys.argv)<2:
        print ("You didn't ask for a particular channel...")
        print ("I know about the following channels:")
        print ("   ")
        for chan in chan_by_name.keys():
            print ("'"+chan+"'")
            
        sys.exit(0)
    channel = sys.argv[1]

    print ("You want channel", channel)
    print ("Using the following tuning info")
    print ("")
    pprint.pprint(chan_by_name[channel])
    print ("")

    chan_info = chan_by_name[channel]

    if chan_info["apid"] + chan_info["vpid"] == 0:
        print ("Sorry, I can't determine the audio & video pids for that channel")
        sys.exit(0)

    X=time.localtime()
    str_stamp = "%d%02d%02d%02d%02d" % (X.tm_year,X.tm_mon,X.tm_mday,X.tm_hour,X.tm_min)
    filename = channel+ "." + str_stamp +".ts"

    print ("Recording", channel, "to", filename)
    
    Pipeline(
       DVB_Multiplex(0, [chan_info["apid"], chan_info["vpid"]], chan_info["feparams"]), # BBC NEWS CHANNEL
       SimpleFileWriter( filename )
    ).run()
