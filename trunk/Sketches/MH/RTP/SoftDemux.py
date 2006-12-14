#!/usr/bin/env python

from MpegTsDemux import MpegTsDemux
import Axon.AdaptiveCommsComponent
import time

from Axon.Ipc import shutdownMicroprocess,producerFinished

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

    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                self.shuttingdown=True
        return self.shuttingdown


    def main(self):
        demuxer = MpegTsDemux(pidfilter = self.pidmap.keys())
        self.shuttingdown = False
        
        while (not self.shutdown()) or self.dataReady("inbox"):
            
            while self.dataReady("inbox"):
                demuxer.insert( self.recv("inbox") )
            
            packets = demuxer.fetch()
            for (pid, erroneous, scrambled, packet) in packets:
                if erroneous or scrambled:
                    continue

                # Send the packet to the outbox appropriate for this PID.
                # demuxer has been configured to only extract PIDs we're interested in
                for outbox in self.pidmap[ pid ]:
                    self.send(packet, outbox)
            
            self.pause()
            yield 1


if __name__ == "__main__":
    from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
    from Kamaelia.Chassis.Graphline import Graphline
    from Core import DVB_Demuxer

    import time
    
    from Axon.Component import component
    class NullDemuxer(component):
        def __init__(self, *args, **argsd):
            super(NullDemuxer,self).__init__()
        def main(self):
           while not self.dataReady("control") or self.dataReady("inbox"):
               while self.dataReady("inbox"):
                   self.recv("inbox")
               self.pause()
               yield 1
           self.recv("control")
    
    results = {}
    for demuxer in [NullDemuxer, DVB_Demuxer,DVB_SoftDemuxer]:
        print "Timing "+demuxer.__name__+" ..."
        start = time.time()
        for _ in range(3):
            Graphline(
                SOURCE=ReadFileAdaptor("/home/matteh/junction.ts",readmode="bitrate",bitrate=600000000000,chunkrate=600000000000/8/2048),
                DEMUX=demuxer( { 18 : ["_EIT_"], 20 : ["_DATETIME_"] } ),
                linkages={ ("SOURCE", "outbox"):("DEMUX","inbox"),
                           ("SOURCE", "signal"):("DEMUX","control"),
                         }
                ).run()
        timetaken = time.time()-start
        results[demuxer.__name__] = timetaken
        
    lowerbound = min(*results.values())
    for name in results:
        print name, results[name]-lowerbound, "out of",results[name]
