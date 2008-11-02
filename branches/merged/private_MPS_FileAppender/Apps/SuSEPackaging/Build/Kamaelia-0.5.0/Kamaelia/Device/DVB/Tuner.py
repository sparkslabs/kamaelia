#!/usr/bin/env python
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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

# DVB Tuner ... where the PIDs of packets to be output can be changed at runtime
# and the card can be specified (if multiple dvb receiver cards present)


import os
import dvb3.frontend
import dvb3.dmx
import time
import struct

from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import shutdownMicroprocess,producerFinished
from Kamaelia.Chassis.Graphline import Graphline


DVB_PACKET_SIZE = 188
DVB_RESYNC = "\x47"
    
    
class Tuner(threadedcomponent):
    """\
    This is a DVB Multiplex Tuner.

    This tunes the given DVB card to the given frequency. This then sets
    up the dvr0 device node to recieve the data recieved on a number of
    PIDs.

    A special case use of these is to tune to 2 specific PIDs - the audio
    and video for a specific TV channel. If you pass just 2 PIDs then
    you're tuning to a specific channel.

    NOTE 1: This multiplex tuner deliberately does not know what
    frequency the multiplex is on, and does not know what PIDs are
    inside that multiplex. You are expected to find out this information
    independently.

    NOTE 2: This means also that producing a mock for the next stages in
    this system should be relatively simple - we run this code once and
    dump to disk. 
    """
    def __init__(self, freq, feparams={},card=0):
        self.freq = freq
        self.feparams = feparams
        self.card = card
        super(Tuner, self).__init__()
        
    
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True
        return False

    def main(self):
        # Open the frontend of card 0 (/dev/dvb/adaptor0/frontend0)
        self.fe = dvb3.frontend.Frontend(self.card, blocking=0)
        self.tune_DVBT(self.freq, self.feparams)
        
        while self.notLocked():
            time.sleep(0.1)
            #yield 1  # could sleep for, say, 0.1 seconds.
            
        demuxers = {}
        
        # This is then a file reader, actually.
        # Should be a little more system friendly really
        fd = os.open("/dev/dvb/adapter"+str(self.card)+"/dvr0", os.O_RDONLY | os.O_NONBLOCK)
        while not self.shutdown():
            
            while self.dataReady("inbox"):
                cmd = self.recv("inbox")
                demuxers = self.handleCommand(cmd, demuxers)
            
            if demuxers:
                try:
                    data = os.read(fd, 2048)
                    self.send(data, "outbox")
                except OSError:
                    self.sync()
            else:
                self.sync()


    def tune_DVBT(self, frequency, feparams={}):
        # Build the tuning parameters (DVB-T)
        params = dvb3.frontend.OFDMParameters()
        params.frequency = frequency * 1000 * 1000
        # load up any extra params specified for the frontend
        for key in feparams:
            params.__dict__[key] = feparams[key]
    
        # Start the tuning
        self.fe.set_frontend(params)
        
    
    def notLocked(self):
        """\
        Wait for lock, if it's not available, yield a true value.
        If it is, exit with a StopIteration. (allows use in a for
        loop)
        """
        return (self.fe.read_status() & dvb3.frontend.FE_HAS_LOCK) != 0
    
    def addPID(self,pid):
        """\
        Adds the given PID to the transport stream that will be available
        in "/dev/dvb/adapter0/dvr0"
        """
        demuxer = dvb3.dmx.Demux(self.card, blocking = 0)
        demuxer.set_pes_filter( pid,
                                dvb3.dmx.DMX_IN_FRONTEND,
                                dvb3.dmx.DMX_OUT_TS_TAP,
                                dvb3.dmx.DMX_PES_OTHER,
                                dvb3.dmx.DMX_IMMEDIATE_START )
        return demuxer
    
    
    def handleCommand(self,cmd,demuxers):
        if cmd[0] == "ADD":
            pidlist = cmd[1]          # dest = (component,inboxname)
            
            for pid in pidlist:
                if pid not in demuxers:
                    demuxers[pid] = self.addPID(pid)
                    
            return demuxers
            
        elif cmd[0] == "REMOVE":
            pidlist = cmd[1]
            
            for pid in pidlist:
                if pid in demuxers:
                    demuxers[pid].stop()
                    del demuxers[pid]
                    
            return demuxers


