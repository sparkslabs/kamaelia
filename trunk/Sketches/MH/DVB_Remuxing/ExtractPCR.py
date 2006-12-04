#!/usr/bin/env python

# attempt to extract PCR (Programme Clock Reference) 'signal' from MPEG transport stream

# PCR is the 'timing' signal from which decoders/receivers can generate their clock
# thereby ensuring that the rate of playback is synchronised to the source of the
# transmission (rather than just free-running, which risks underruns/overflows)

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

import time


from AlignTSPackets import AlignTSPackets

class ExtractPCR(component):
    Inboxes = { "inbox" : "Individual tranport stream packets",
                "control" : "Shutdown signalling",
              }
    Outboxes = { "outbox" : "",
                 "signal" : "Shutdown signalling",
               }

    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg,(producerFinished,shutdownMicroprocess)):
                return True
        return False

    def main(self):
        shutdown = False
        while not shutdown:
            
            while self.dataReady("inbox"):
                self.parse(self.recv("inbox"))
            
            shutdown = shutdown or self.shutdown()
            
            if not shutdown and not self.anyReady():
                self.pause()
                
            yield 1
        
    def parse(self, tspacket):
        
        pid = ( (ord(tspacket[1])<<8) + ord(tspacket[2]) ) & 0x1fff
        adaptionflag = (ord(tspacket[3]) & 0x30) >> 4
        
        if adaptionflag == 2 or adaptionflag == 3:
            # adaption field starts at byte 4
            start=4
            
            af_len = ord(tspacket[start+0])
            
            # need at least 7 bytes in the adaption field for there to be PCR data
            if af_len >= 7:
                flags = ord(tspacket[start+1])
                
                if (flags & 16):
                    # PCR is present, so lets extract it
                    
                    # 48 bit field
                    pcr = (ord(tspacket[start+2]) << 40) + \
                          (ord(tspacket[start+3]) << 32) + \
                          (ord(tspacket[start+4]) << 24) + \
                          (ord(tspacket[start+5]) << 16) + \
                          (ord(tspacket[start+5]) <<  8) + \
                           ord(tspacket[start+5])
                    pcr_base = pcr>>15      # top 33 bits
                                            # middle 6 bits reserved
                    pcr_ext  = pcr & 0x1ff  # bottom 9 bits
                    
                    real_pcr = pcr_base * 300 + pcr_ext

                    self.send( (pid, real_pcr), "outbox")
                    
#                    self.send( "pid %4d : pcr = %10d . %3d\n" % (pid,pcr_base,pcr_ext), "outbox")
#                    print pid, pcr_base, pcr_ext
                    
                    
class MeasurePCRs(component):
                    
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg,(producerFinished,shutdownMicroprocess)):
                return True
        return False

    def main(self):
        shutdown = False
        pcrs = {}
        while not shutdown:
            
            while self.dataReady("inbox"):
                now = time.time()
                pid,pcr = self.recv("inbox")
                
                if not pcrs.has_key(pid):
                    pcrs[pid] = pcr, now
                else:
                    old_pcr, then = pcrs[pid]
                    rate = float(pcr-old_pcr) / float(now-then) / 1000000.0
                    print "pid %4d : approximating ... rate about %.5f MHz" % (pid, rate)
            
            shutdown = shutdown or self.shutdown()
            
            if not shutdown and not self.anyReady():
                self.pause()
                
            yield 1

if __name__ == "__main__":
    
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Device.DVB.Core import DVB_Multiplex
    
    import dvb3.frontend
    
    FREQUENCY = 505.833330
    FE_PARAMS = { "inversion" : dvb3.frontend.INVERSION_AUTO,
                  "constellation" : dvb3.frontend.QAM_16,
                  "coderate_HP" : dvb3.frontend.FEC_3_4,
                  "coderate_LP" : dvb3.frontend.FEC_3_4,
                }
                   
    Pipeline( DVB_Multiplex(FREQUENCY, [0x2000], FE_PARAMS),
              AlignTSPackets(),
              ExtractPCR(),
              MeasurePCRs(),
#              ConsoleEchoer(),
            ).run()
