#!/usr/bin/env python

import dvb3.soft_dmx
import Axon.AdaptiveCommsComponent
import time

class DVB_SoftDemuxer(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
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
        super(DVB_SoftDemuxer, self).__init__()
        self.pidmap = pidmap
        for pid in pidmap: # This adds an outbox per pid
            # This allows for the PIDs to be split or remultiplexed
            # together.
            for outbox in pidmap[pid]:
                if not self.outboxes.has_key(outbox):
                    self.addOutbox(outbox)


    def main(self):
        demuxer = dvb3.soft_dmx.SoftDemux()
        while 1:
            yield 1
            while self.dataReady("inbox"):
                yield 1
                demuxer.insert( self.recv("inbox") )
                result = True
                while result:
                    yield 1
                    result = demuxer.pop()
                    if result:
                        pid,erroneous,scrambled,packet = result
                        time.sleep(0.01)
                        if erroneous or scrambled:
                            continue
        
                        # Send the packet to the outbox appropriate for this PID.
                        # "Fail" silently for PIDs we don't know about and weren't
                        # asked to demultiplex
                        try:
                           for outbox in self.pidmap[ str(pid) ]:
                               self.send(packet, outbox)
                        except KeyError:
                            pass
            self.pause()
