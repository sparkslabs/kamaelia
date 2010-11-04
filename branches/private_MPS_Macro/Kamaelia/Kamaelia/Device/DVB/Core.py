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
# -------------------------------------------------------------------------
"""\
==========================================
SimpleDVB-T (Digital Terrestrial TV) Tuner
==========================================

DVB_Multiplex tunes to the specified DVB-T multiplex and outputs received MPEG
Transport Stream packets that have a PID in the list of PIDs specified.

If you need to change which PIDs you receive at runtime, consider using
Kamaelia.Device.DVB.Tuner



Example Usage
-------------

Receiving PIDs 600 and 601 from MUX 1 broadcast from Crystal Palace in the UK
(this should, effectively, receive the video and audio for the channel
'BBC ONE')::
  
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Device.DVB.Core import DVB_Multiplex
    from Kamaelia.File.Writing import SimpleFileWriter
    import dvb3.frontend

    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "code_rate_HP" : dvb3.frontend.FEC_3_4,
        "code_rate_LP" : dvb3.frontend.FEC_3_4,
    }

    Pipeline( DVB_Multiplex(505.833330, [600,601], feparams),
              SimpleFileWriter("BBC ONE.ts"),
            ).run()

Receive and record the whole multiplex (all pids)::

    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Device.DVB.Core import DVB_Multiplex
    from Kamaelia.File.Writing import SimpleFileWriter
    import dvb3.frontend

    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "code_rate_HP" : dvb3.frontend.FEC_3_4,
        "code_rate_LP" : dvb3.frontend.FEC_3_4,
    }

    Pipeline( DVB_Multiplex(505.833330, [0x2000], feparams),
              SimpleFileWriter("BBC ONE.ts"),
            ).run()



How does it work?
-----------------

DVB_Multiplex tunes, using the specified tuning parameters to a DVB-T
transmitted multiplex.

It will output received transport stream packets out of its "outbox" outbox for
those packets with a PID in the list of PIDs specified at initialization.

Most DVB tuner devices understand a special packet ID of 0x2000 to request the
entire transport stream of all packets with all IDs. Specify a list containing
only this PID to receive the whole transport stream.

This component will terminate if a shutdownMicroprocess or producerFinished
message is sent to the "control" inbox. The message will be forwarded on out of
the "signal" outbox just before termination.



============================================
SimpleDVB-T (Digital Terrestrial TV) Demuxer
============================================

DVB_Demuxer take in MPEG transport stream packets and routes them to different
outboxes, as specified in a mapping table.

If you need to change which PIDs you receive at runtime, consider using
Kamaelia.Device.DVB.DemuxerService.



Example Usage
-------------

Receiving PIDs 600 and 601 from MUX 1 broadcast from Crystal Palace in the UK
(this should, effectively, receive the video and audio for the channel
'BBC ONE') and write them to separate files, plus also to a combined file. Plus
also record PIDS 610 and 611 (audio and video for 'BBC TWO') to a fourth file::

    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Device.DVB.Core import DVB_Multiplex
    from Kamaelia.Device.DVB.Core import DVB_Demuxer
    from Kamaelia.File.Writing import SimpleFileWriter
    import dvb3.frontend

    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "code_rate_HP" : dvb3.frontend.FEC_3_4,
        "code_rate_LP" : dvb3.frontend.FEC_3_4,
    }

    Graphline(
        RECV   = DVB_Multiplex(505.833330, [600,601, 610,611], feparams),
        DEMUX  = DVB_Demuxer( { 600 : ["outbox","video"],
                                601 : ["outbox","audio"],
                                610 : ["two"],
                                611 : ["two"] } ),
        REC_A  = SimpleFileWriter("audio.ts"),
        REC_V  = SimpleFileWriter("video.ts"),
        REC_AV = SimpleFileWriter("audio_and_video.ts"),
        REC_2  = SimpleFileWriter("audio_and_video2.ts"),
        
        linkages = { ("RECV",  "outbox")  : ("DEMUX",  "inbox"),
        
                     ("DEMUX", "outbox") : ("REC_AV", "inbox"),
                     ("DEMUX", "audio")  : ("REC_A",  "inbox"),
                     ("DEMUX", "video")  : ("REC_V",  "inbox"),
                     
                     ("DEMUX", "two")    : ("REC_2",  "inbox"),
                   }
    ).run()



How does it work?
-----------------

DVB_Demuxer takes MPEG transport stream packets, sent to its "inbox" inbox
and determines the packet ID (PID) of each, then distributes them to different
outboxes according to a mapping dictionary specified at intialization.

The dictionary maps individual PIDs to lists of outbox names (the outboxes to
which packets with that given PID should be sent), for example::
  
    {
      600 : ["outbox","video"],
      601 : ["outbox","audio"],
      610 : ["two"],
      611 : ["two"]
    }

This example mapping specified that packets with 600 and 601 should be sent to
the "outbox" outbox. Packets with PID 600 should also be sent to the "video"
outbox and packets with PID 601 should also be sent to the "audio" outbox.
Finally, packets with PIDs 610 and 611 should b sent to the "two" outbox.

The relevant outboxes are automatically created.

If a packet arrives with a PID not featured in the mapping table, that packet
will be discarded.

As in the above example, a packet with a given PID can be mapped to more than
one destination outbox. It will be sent to all outboxes to which it is mapped.

Packets which have their 'error' or 'scrambled' flag bits set will be discarded.

This component will terminate if a shutdownMicroprocess or producerFinished
message is sent to the "control" inbox. The message will be forwarded on out of
the "signal" outbox just before termination.

"""

import os
import dvb3.frontend
import dvb3.dmx
import time
import struct

from Axon.Component import component
from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import shutdownMicroprocess,producerFinished

DVB_PACKET_SIZE = 188
DVB_RESYNC = "\x47"
import Axon.AdaptiveCommsComponent
    
def tune_DVB(fe, frequency, feparams={}):
    # Build the tuning parameters - no longer assumes DVB-T
    build_params_type = fe.get_dvbtype()

    if "frequency" not in feparams:
        params = build_params_type(
            frequency = frequency * 1000 * 1000,
            **feparams
            )
    else:
        params = build_params_type(**feparams)

    # Start the tuning
    fe.set_frontend(params)

def notLocked(fe):
    """\
    Returns True if the frontend is not yet locked.
    Returns False if it is locked.
    """
    return (fe.read_status() & dvb3.frontend.FE_HAS_LOCK) == 0

def addPIDS(pids):
    """\
    Adds the given PID to the transport stream that will be available
    in "/dev/dvb/adapter0/dvr0"
    """
    demuxers = [dvb3.dmx.Demux(0, blocking = 0) for _ in pids]
    for p in xrange(len(pids)):
        demuxers[p].set_pes_filter(pids[p],
                                   dvb3.dmx.DMX_IN_FRONTEND,
                                   dvb3.dmx.DMX_OUT_TS_TAP,
                                   dvb3.dmx.DMX_PES_OTHER,
                                   dvb3.dmx.DMX_IMMEDIATE_START)
    return demuxers

class DVB_Multiplex(threadedcomponent):
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
    def __init__(self, freq, pids, feparams={},card=0):
        if freq == 0:
            if feparams.get("frequency", None) is None:
                 raise ValueError("frequency not given explicitly nor in feparams - must be non-zero")
            
            freq = feparams.get("frequency", None)/(1000*1000) # Freq has always been defined as MHz not Hz.

        self.freq = freq
        self.feparams = feparams
        self.pids = pids
        self.card = card
        super(DVB_Multiplex, self).__init__()
        
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True
        return False

    def main(self):
        # Open the frontend of card 0 (/dev/dvb/adaptor0/frontend0)
        fe = dvb3.frontend.Frontend(self.card, blocking=0)
        tune_DVB(fe, self.freq, self.feparams)
        while notLocked(fe): time.sleep(0.1) #yield 1  # could sleep for, say, 0.1 seconds.
        demuxers = addPIDS(self.pids)        

        # This is then a file reader, actually.
        # Should be a little more system friendly really
        fd = os.open("/dev/dvb/adapter"+str(self.card)+"/dvr0", os.O_RDONLY) # | os.O_NONBLOCK)
        tosend = []
        tosend_len =0
        while not self.shutdown():
            try:
               data = os.read(fd, 188000)
               self.send(data, "outbox")
            except OSError:
               print "PASS"

import dvbpacket
class DVB_Demuxer(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    """\
    This demuxer expects to recieve the output from a DVB_Multiplex
    component on its primary inbox. It is also provided with a number
    of pids. For each pid that it knows about, it forwards the data
    received on that PID to an appropriate outbox. Data associated with
    unknown PIDs in the datastream is thrown away.
    
    The output here is still transport stream packets. Another layer
    is required to decide what to do with these - to yank out the PES
    and ES packets.
    """
    Inboxes = {
        "inbox" : "This is where we expect to recieve a transport stream",
        "control" : "We will receive shutdown messages here",
    }
    def __init__(self, pidmap):
        super(DVB_Demuxer, self).__init__()
        self.pidmap = pidmap
        for pid in pidmap: # This adds an outbox per pid
            # This allows for the PIDs to be split or remultiplexed
            # together.
            for outbox in pidmap[pid]:
                if not self.outboxes.has_key(outbox):
                    self.addOutbox(outbox)
        if "default" in pidmap:
            self.forwardothers = True
        else:
            self.forwardothers = False

    def errorIndicatorSet(self, packet):  return ord(packet[1]) & 0x80
    def scrambledPacket(self, packet):    return ord(packet[3]) & 0xc0

    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                self.shuttingdown=True
        return self.shuttingdown
    
    def main(self):
        buffer = ""
        buffers = []
        self.shuttingdown=False
        while (not self.shutdown()) or self.dataReady("inbox"):
            for buffer in self.Inbox("inbox"):
                buffers.append(buffer)
            for buffer in buffers:
                packets = dvbpacket.packetise(buffer)
                for packet in packets:

                      if self.errorIndicatorSet(packet): continue
                      if self.scrambledPacket(packet):   continue
                      pid = struct.unpack(">H", packet[1: 3])[0] & 0x1fff

                      # Send the packet to the outbox appropriate for this PID.
                      # "Fail" silently for PIDs we don't know about and weren't
                      # asked to demultiplex
                      try:
                          for outbox in self.pidmap[ pid ]:
                              self.send(packet, outbox)
                      except KeyError:
                          if self.forwardothers:
                              for outbox in self.pidmap[ "default" ]:
                                  self.send(packet, outbox)
                          pass
            buffers = []
            if not self.anyReady():
               self.pause()

            yield 1

__kamaelia_components__ = ( DVB_Multiplex, DVB_Demuxer, )

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.File.Writing import SimpleFileWriter
    from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
    from Kamaelia.Chassis.Graphline import Graphline

    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "code_rate_HP" : dvb3.frontend.FEC_3_4,
        "code_rate_LP" : dvb3.frontend.FEC_3_4,
    }

    channels_london =  {
           "MORE4+1" : (   538, #MHz
                         [ 701, 702 ] # PID (programme ID) for video and PID for audio
                       )
    }
    services = {
           "NEWS24": (754, [640, 641]),
           "MORE4+1": (810, [701,702]),
           "TMF": (810, [201,202])
    }
    if 1:
        Pipeline(
           DVB_Multiplex(508, [640, 641, 620, 621, 622, 610, 611, 612, 600, 601, 602, 18],feparams),
           SimpleFileWriter("multiplex_new.data")
        ).run()
    if 0:
        Graphline(
            SOURCE=ReadFileAdaptor("multiplex_new.data"),
            DEMUX=DVB_Demuxer({
                640: ["NEWS24"],
                641: ["NEWS24"],
                600: ["BBCONE"],
                601: ["BBCONE"],
                610: ["BBCTWO"],
                611: ["BBCTWO"],
                620: ["CBBC"],
                621: ["CBBC"],
                18:  ["NEWS24", "BBCONE", "BBCTWO", "CBBC"],
            }),
            NEWS24=SimpleFileWriter("news24.data"),
            BBCONE=SimpleFileWriter("bbcone.data"),
            BBCTWO=SimpleFileWriter("bbctwo.data"),
            CBBC=SimpleFileWriter("cbbc.data"),
            linkages={
               ("SOURCE", "outbox"):("DEMUX","inbox"),
               ("DEMUX", "NEWS24"): ("NEWS24", "inbox"),
               ("DEMUX", "BBCONE"): ("BBCONE", "inbox"),
               ("DEMUX", "BBCTWO"): ("BBCTWO", "inbox"),
               ("DEMUX", "CBBC"): ("CBBC", "inbox"),
            }
        ).run()

# RELEASE: MH, MPS
