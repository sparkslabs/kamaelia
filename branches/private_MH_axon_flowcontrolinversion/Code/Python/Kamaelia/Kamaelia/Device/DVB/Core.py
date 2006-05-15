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
from Axon.ThreadedComponent import threadedcomponent

DVB_PACKET_SIZE = 188
DVB_RESYNC = "\x47"
import Axon.AdaptiveCommsComponent
    
def tune_DVBT(fe, frequency):
    # Build the tuning parameters (DVB-T)
    params = dvb3.frontend.OFDMParameters()
    params.frequency = frequency * 1000 * 1000

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
        while notLocked(fe): time.sleep(0.1) #yield 1  # could sleep for, say, 0.1 seconds.
        demuxers = addPIDS(self.pids)        

        # This is then a file reader, actually.
        # Should be a little more system friendly really
        fd = os.open("/dev/dvb/adapter0/dvr0", os.O_RDONLY) # | os.O_NONBLOCK)
        tosend = []
        tosend_len =0
        while True:
            try:
               data = os.read(fd, 2048)
               tosend.append(data) # Ensure we're sending collections of packets through Axon, not single ones
               tosend_len += len(data)
               if tosend_len > 2048:
                   self.send("".join(tosend), "outbox")
                   tosend = []
                   tosend_len = 0
               #self.send(data, "outbox")
            except OSError:
               pass

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
            for outbox in pidmap[pid]:
                if not self.outboxes.has_key(outbox):
                    self.addOutbox(outbox)

    def errorIndicatorSet(self, packet):  return ord(packet[1]) & 0x80
    def scrambledPacket(self, packet):    return ord(packet[3]) & 0xc0

    def main(self):
        buffer = ""
        while 1:
            yield 1
            if self.dataReady("inbox"):
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
                      for outbox in self.pidmap[ str(pid) ]:
                          self.send(packet, outbox)
#                          print "X", outbox
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
           DVB_Multiplex(754, [640, 641, 620, 621, 622, 610, 611, 612, 600, 601, 602, 18]),
           SimpleFileWriter("multiplex_new.data")
        ).run()
    if 1:
        Graphline(
            SOURCE=ReadFileAdaptor("multiplex.data"),
            DEMUX=DVB_Demuxer({
                "640": ["NEWS24"],
                "641": ["NEWS24"],
                "600": ["BBCONE"],
                "601": ["BBCONE"],
                "610": ["BBCTWO"],
                "611": ["BBCTWO"],
                "620": ["CBBC"],
                "621": ["CBBC"],
                "18":  ["NEWS24", "BBCONE", "BBCTWO", "CBBC"],
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
