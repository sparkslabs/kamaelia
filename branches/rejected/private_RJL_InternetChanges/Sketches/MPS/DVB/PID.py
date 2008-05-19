#!/usr/bin/python
#
# DVB Transport stream should pick out entire DVB services and send those to
# named outboxes. (Send DVB Services to a Kamaelia Service...(!))
#


import os
import dvb3.frontend
import dvb3.dmx
import time
import struct

from Axon.Component import component
DVB_PACKET_SIZE = 188
DVB_RESYNC = "\x47"
import Axon.AdaptiveCommsComponent
    
def tune_DVBT(fe, frequency):
    # Build the tuning parameters (DVB-T)
    params = dvb3.frontend.OFDMParameters()
    params.frequency = frequency * 1000 * 1000
    
    params.inversion = dvb3.frontend.INVERSION_AUTO
    params.constellation = dvb3.frontend.QAM_16
    params.coderate_HP = dvb3.frontend.FEC_2_3
    params.coderate_LP = dvb3.frontend.FEC_2_3

    # Start the tuning
    fe.set_frontend(params)

def notLocked(fe):
    """\
    Wait for lock, if it's not available, yield a true value.
    If it is, exit with a StopIteration. (allows use in a for
    loop)
    """
    return (fe.read_status() & dvb3.frontend.FE_HAS_LOCK) != 0

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

from Axon.ThreadedComponent import threadedcomponent

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
    def __init__(self, freq, pids):
        self.freq = freq
        self.pids = pids
        super(DVB_Multiplex, self).__init__()
        

    def main(self):
        # Open the frontend of card 0 (/dev/dvb/adaptor0/frontend0)
        fe = dvb3.frontend.Frontend(0, blocking=0)
        tune_DVBT(fe, self.freq)
        while notLocked(fe): time.sleep(0.1)  #yield 1  # could sleep for, say, 0.1 seconds.
        demuxers = addPIDS(self.pids)        

        # This is then a file reader, actually.
        # Should be a little more system friendly really
        fd = os.open("/dev/dvb/adapter0/dvr0", os.O_RDONLY) # | os.O_NONBLOCK)
        while True:
            try:
               data = os.read(fd, 2048)
               self.send(data, "outbox")
            except OSError:
               pass
#            yield 1
            # XXX: We should add the following:
            # XXX: Handle shutdown messages
            # XXX: Pass on shutdown messages/errors

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
            if not self.outboxes.has_key(pidmap[pid]):
                self.addOutbox(pidmap[pid])

    def errorIndicatorSet(self, packet):  return ord(packet[1]) & 0x80
    def scrambledPacket(self, packet):    return ord(packet[3]) & 0xc0

    def main(self):
        buffer = ""
        while 1:
            yield 1
            while self.dataReady("inbox"):
              buffer += self.recv("inbox")

            while len(buffer) >= DVB_PACKET_SIZE:
                  yield 1
                  i = buffer.find(DVB_RESYNC)
                  if i == -1: # if not found
                      "we have a dud"
                      buffer = ""
                      continue 
                  if i>0:
                      # if found remove all bytes preceeding that point in the buffers
                      # And try again
                      buffer = buffer[i:]
                      continue
                  # packet is the first 188 bytes in the buffer now
                  packet, buffer = buffer[:DVB_PACKET_SIZE], buffer[DVB_PACKET_SIZE:]

                  if self.errorIndicatorSet(packet): continue
                  if self.scrambledPacket(packet):   continue

                  pid = struct.unpack(">H", packet[1: 3])[0] & 0x1fff

                  # Send the packet to the outbox appropriate for this PID.
                  # "Fail" silently for PIDs we don't know about and weren't
                  # asked to demultiplex
                  try:
#                      print ".", self.pidmap, str(pid)
                      self.send(packet, self.pidmap[ str(pid) ])
                  except KeyError:
                      pass
                  
            self.pause()

#
# XXX
#
# This is where we may wish to think about piping the results to something like
# mencoder, perhaps via a named pipe, since that will *probably* work. We'll have to
# check that though :-/
#
# For XTech, we can see if we can coax Mencoder into taking our output direct
# and doing something useful/interesting... (At least then we're up and running)
#

class PIDHandler:

    counter = None
    pes_dirty = False
    pes = None

    def process_ts_packet(self, packet):
        x = ord(packet[3])
        counter = x & 0x0f
        adaptation = (x & 0x30) >> 4

        if adaptation == 0:
            # "ITU-T Rec. H2.222.0 | ISO/IEC 13818-1 decoders shall discard
            # Transport Stream packets with the adaptation_field_control field
            # set to a value of '00'".
            return

        if adaptation != 1 and ord(packet[4]) > 0:
            discontinuity = ((ord(packet[5]) & 0x80) == 0x80)
        else:
            discontinuity = False
        if self.counter is None:
            self.counter = counter
        elif adaptation & 1:
            self.counter = (self.counter + 1) & 0xf

        if self.counter != counter:
            if not discontinuity:
                self.pes_dirty = True
            self.counter = counter

        if ord(packet[1]) & 0x40:
            # Payload Unit Start Indicator (PUSI) is set, so a new packet has
            # started.  Throw the old one down to the PES processor.
            if self.pes is not None and not self.pes_dirty:
                self.process_pes_packet("".join(self.pes))
            self.pes_dirty = False
            self.pes = None

        if adaptation == 1:
            chunk = packet[4: ]
        elif adaptation == 3:
            chunk = packet[5 + ord(packet[4]): ]
        elif adaptation == 2:
            # No interesting data.
            return

        if len(chunk) > 0:
            if self.pes is None:
                self.pes = [chunk]
            else:
                self.pes.append(chunk)

if __name__ == "__main__":
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.File.Writing import SimpleFileWriter
    from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
    from Kamaelia.Util.Graphline import Graphline

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
    if 0:
        pipeline(
           DVB_Multiplex(754, [640, 641, 620, 621, 622, 610, 611, 612, 600, 601, 602, 12]),
           SimpleFileWriter("multiplex_new.data")
        ).run()
    if 1:
        Graphline(
            SOURCE=ReadFileAdaptor("multiplex.data"),
            DEMUX=DVB_Demuxer({
                "640": "NEWS24",
                "641": "NEWS24",
                "600": "BBCONE",
                "601": "BBCONE",
                "610": "BBCTWO",
                "611": "BBCTWO",
                "620": "CBBC",
                "621": "CBBC",
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
#            if not self.outboxes.has_key(pidmap[pid]):
#                self.addOutbox(pidmap[pid])
