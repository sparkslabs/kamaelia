#!/usr/bin/env python
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
"""\
==================================
Parsing of Linux-DVB channels.conf
==================================

Parses lines from a linux-dvb channels.conf file.

"""

from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished

import dvb3.frontend

class ParseChannelsConf(component):
    """\
    ParseChannelsConf() -> new ParseChannelsConf component

    Parses channels.conf file fed, line by line, as strings into the
    "inbox" inbox and outputs (channelname, dict(tuning params),dict(pids))
    pairs out of the "outbox" outbox.
    """

    def __init__(self):
        super(ParseChannelsConf,self).__init__()
        self.shutdownMsg = None

    def main(self):
        while 1:
            while self.dataReady("inbox"):
                line = self.recv("inbox")
                data = self.parse(line)
                if data is not None:
                    for _ in self.safesend(data,"outbox"): yield _

            if self.checkShutdown():
                self.send(self.shutdownMsg,"signal")
                return
            
            self.pause()
            yield 1
            
            
    def parse(self,line):
        try :
            line = line.strip()
            if not line:
                return None
            name, freq, inv, bw, fec_hi, fec_lo, qam, tm, gi, h, vpid, apid, sid = line.split(":")
            return name, \
                {   "frequency"             : float(freq)/1000.0/1000.0,
                    "inversion"             : _inversion[inv.upper()],
                    "bandwidth"             : _bandwidth[bw.upper()],
                    "code_rate_HP"          : _fec[fec_hi.upper()],
                    "code_rate_LP"          : _fec[fec_lo.upper()],
                    "constellation"         : _qam[qam.upper()],
                    "transmission_mode"     : _tm[tm.upper()],
                    "guard_interval"        : _gi[gi.upper()],
                    "hierarchy_information" : _h[h.upper()],
                }, \
                {   "video_pid" : int(vpid),
                    "audio_pid" : int(apid),
                    "service_id" : int(sid),
                }
        except:
            return None


    def checkShutdown(self):
        """\
        Collects any new shutdown messages arriving at the "control" inbox, and
        returns "NOW" if immediate shutdown is required, or "WHENEVER" if the
        component can shutdown when it has finished processing pending data.
        """
        while self.dataReady("control"):
            newMsg = self.recv("control")
            if isinstance(newMsg, shutdownMicroprocess):
                self.shutdownMsg = newMsg
            elif self.shutdownMsg is None and isinstance(newMsg, producerFinished):
                self.shutdownMsg = newMsg
        if isinstance(self.shutdownMsg, shutdownMicroprocess):
            return "NOW"
        elif self.shutdownMsg is not None:
            return "WHENEVER"
        else:
            return None

    def safesend(self, data, boxname):
        """\
        Generator.
        
        Sends data out of the named outbox. If the destination is full
        (noSpaceInBox exception) then it waits until there is space and retries
        until it succeeds.
        
        If a shutdownMicroprocess message is received, returns early.
        """
        while 1:
            try:
                self.send(data, boxname)
                return
            except noSpaceInBox:
                if self.checkShutdown() == "NOW":
                    return
                self.pause()
                yield 1


_inversion = {
    "INVERSION_OFF" : dvb3.frontend.INVERSION_OFF,
    "INVERSION_ON" : dvb3.frontend.INVERSION_ON,
    "INVERSION_AUTO" : dvb3.frontend.INVERSION_AUTO,
}

_bandwidth = {
    "BANDWIDTH_8_MHZ" : dvb3.frontend.BANDWIDTH_8_MHZ,
    "BANDWIDTH_7_MHZ" : dvb3.frontend.BANDWIDTH_7_MHZ,
    "BANDWIDTH_6_MHZ" : dvb3.frontend.BANDWIDTH_6_MHZ,
    "BANDWIDTH_AUTO" : dvb3.frontend.BANDWIDTH_AUTO,
}

_fec = {
    "FEC_NONE" : dvb3.frontend.FEC_NONE,
    "FEC_1_2" : dvb3.frontend.FEC_1_2,
    "FEC_2_3" : dvb3.frontend.FEC_2_3,
    "FEC_3_4" : dvb3.frontend.FEC_3_4,
    "FEC_4_5" : dvb3.frontend.FEC_4_5,
    "FEC_5_6" : dvb3.frontend.FEC_5_6,
    "FEC_6_7" : dvb3.frontend.FEC_6_7,
    "FEC_7_8" : dvb3.frontend.FEC_7_8,
    "FEC_8_9" : dvb3.frontend.FEC_8_9,
    "FEC_AUTO" : dvb3.frontend.FEC_AUTO,
}

_qam = {
    "QPSK" : dvb3.frontend.QPSK,
    "QAM_16" : dvb3.frontend.QAM_16,
    "QAM_32" : dvb3.frontend.QAM_32,
    "QAM_64" : dvb3.frontend.QAM_64,
    "QAM_128" : dvb3.frontend.QAM_128,
    "QAM_256" : dvb3.frontend.QAM_256,
    "QAM_AUTO" : dvb3.frontend.QAM_AUTO,
}

_tm = {
    "TRANSMISSION_MODE_2K" : dvb3.frontend.TRANSMISSION_MODE_2K,
    "TRANSMISSION_MODE_8K" : dvb3.frontend.TRANSMISSION_MODE_8K,
    "TRANSMISSION_MODE_AUTO" : dvb3.frontend.TRANSMISSION_MODE_AUTO,
}

_gi = {
    "GUARD_INTERVAL_1_32" : dvb3.frontend.GUARD_INTERVAL_1_32,
    "GUARD_INTERVAL_1_16" : dvb3.frontend.GUARD_INTERVAL_1_16,
    "GUARD_INTERVAL_1_8" : dvb3.frontend.GUARD_INTERVAL_1_8,
    "GUARD_INTERVAL_1_4" : dvb3.frontend.GUARD_INTERVAL_1_4,
    "GUARD_INTERVAL_AUTO" : dvb3.frontend.GUARD_INTERVAL_AUTO,
}

_h = {
    "HIERARCHY_NONE" : dvb3.frontend.HIERARCHY_NONE,
    "HIERARCHY_1" : dvb3.frontend.HIERARCHY_1,
    "HIERARCHY_2" : dvb3.frontend.HIERARCHY_2,
    "HIERARCHY_4" : dvb3.frontend.HIERARCHY_4,
    "HIERARCHY_AUTO" : dvb3.frontend.HIERARCHY_AUTO,
}



if __name__ == "__main__":
  
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.File.Reading import RateControlledFileReader
    from Kamaelia.Util.Console import ConsoleEchoer
    
    import sys
    
    if len(sys.argv) != 2:
      print "Usage:"
      print
      print "    %s <channels.conf file>" % sys.argv[0]
      print
      sys.exit(1)
    
    channelsConfFile = sys.argv[1]
    
    Pipeline(
        RateControlledFileReader(channelsConfFile, readmode="lines", rate=1000, chunksize=1),
        ParseChannelsConf(),
        ConsoleEchoer(),
    ).run()
    