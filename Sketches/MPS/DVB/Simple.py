#!/usr/bin/python
#
# DVB Transport stream should pick out entire DVB services and send those to
# named outboxes. (Send DVB Services to a Kamaelia Service...(!))
#


import os
import dvb3.frontend
import dvb3.dmx
import time

from Axon.Component import component

class DVB_Channel_Tuner(component):
    def __init__(self, freq, pids):
        self.freq = freq
        self.pids = pids
        super(DVB_Channel_Tuner, self).__init__()

    def main(self):
        # Open the frontend of card 0 (/dev/dvb/adaptor0/frontend0)
        fe = dvb3.frontend.Frontend(0, blocking=0)

        # Build the tuning parameters (DVB-T)
        params = dvb3.frontend.OFDMParameters()
        params.frequency = self.freq * 1000 * 1000

        # Start the tuning
        fe.set_frontend(params)

        # wait for lock
        while (fe.read_status() & dvb3.frontend.FE_HAS_LOCK) == 0:
           time.sleep(0.1)

        demuxers = [dvb3.dmx.Demux(0, blocking = 0) for _ in self.pids]
        for p in xrange(len(self.pids)):
            demuxers[p].set_pes_filter(self.pids[p], dvb3.dmx.DMX_IN_FRONTEND,
                                  dvb3.dmx.DMX_OUT_TS_TAP,
                                  dvb3.dmx.DMX_PES_OTHER,
                                  dvb3.dmx.DMX_IMMEDIATE_START)

        fd = os.open("/dev/dvb/adapter0/dvr0", os.O_RDONLY | os.O_NONBLOCK)

        while True:
            try:
               data = os.read(fd, 2048)
               self.send(data, "outbox")
            except OSError:
               pass
            yield 1

if __name__ == "__main__":
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.File.Writing import SimpleFileWriter

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
    pipeline(
       DVB_Channel_Tuner(*(channels_london["MORE4+1"])),
       SimpleFileWriter("channelx.data")
    ).run()

