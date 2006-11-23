#!/usr/bin/env python

from Axon.Component import component
import string
import struct
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Axon.AxonExceptions import noSpaceInBox

# based on ryan's PCMToWave component, modified to match WAVParser's formats for
# conveying samplerate, channels etc
#
# also takes binary sample data, instead of integer samples

class WavWriter(component):
    def __init__(self, channels, sample_format, sample_rate):
        super(WavWriter, self).__init__()
        if sample_format == "S8":
            self.bitsPerSample = 8
            self.bytespersample = 1
        elif sample_format == "S16_LE":
            self.bitsPerSample = 16
            self.bytespersample = 2
        else:
            raise "WavWriter can't handle sample format "+str(sample_format)+" at the moment"
        
        self.samplingfrequency = sample_rate
        self.channels = channels
        
    def handleControl(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) and not isinstance(self.shutdownMsg, shutdownMicroprocess):
                self.shutdownMsg = msg
            elif isinstance(msg, shutdownMicroprocess):
                self.shutdownMsg = msg

    def canStop(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, (producerFinished,shutdownMicroprocess))

    def mustStop(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, shutdownMicroprocess)
    
    def waitSend(self,data,boxname):
        while 1:
            try:
                self.send(data,boxname)
                return
            except noSpaceInBox:
                if self.mustStop():
                    raise "STOP"
                
                self.pause()
                yield 1
                
                if self.mustStop():
                    raise "STOP"

    def main(self):
        self.shutdownMsg=None
        
        try:
            #we don't know the length yet, so we say the file lasts an arbitrary (long) time 
            riffchunk = "RIFF" + struct.pack("<L", 0x0) + "WAVE"
            
            bytespersecond = self.bytespersample * self.channels * self.samplingfrequency
            
            formatchunk = "fmt "
            formatchunk += struct.pack("<L", self.bitsPerSample)
            formatchunk += struct.pack("<H", 0x01) #PCM/Linear quantization
            formatchunk += struct.pack("<H", self.channels) 
            formatchunk += struct.pack("<L", self.samplingfrequency)
            formatchunk += struct.pack("<L", bytespersecond)
            formatchunk += struct.pack("<H", self.bytespersample * self.channels)
            formatchunk += struct.pack("<H", self.bitsPerSample)
        
            datachunkheader = "data" + struct.pack("<L", 0x0) #again, an arbitrary (large) value
            
            for _ in self.waitSend(riffchunk + formatchunk + datachunkheader, "outbox"):
                yield 1
            
            running = True
            while running:
                yield 1
                
                while self.dataReady("inbox"): # we accept binary sample data in strings
                    sampledata = self.recv("inbox")
                    for _ in self.waitSend(sampledata, "outbox"):
                        yield 1
                    
                if self.canStop():
                    raise "STOP"
                        
                self.pause()

        except "STOP":
            self.send(self.shutdownMsg,"signal")

if __name__=="__main__":
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Chassis.Carousel import Carousel
    from WAV import WavParser
    from Kamaelia.File.Reading import RateControlledFileReader
    from Kamaelia.File.Writing import SimpleFileWriter
    
    Graphline(
        READ  = RateControlledFileReader("/usr/share/sounds/alsa/Front_Center.wav",readmode="bytes",rate=1000000),
        PARSE = WavParser(),
        ENC   = Carousel(lambda meta : WavWriter(**meta)),
        WRITE = SimpleFileWriter("test.wav"),
        linkages = {
            ("READ", "outbox") : ("PARSE", "inbox"),
            ("PARSE", "outbox") : ("ENC", "inbox"),
            ("PARSE", "all_meta") : ("ENC", "next"),
            ("ENC", "outbox") : ("WRITE", "inbox"),
            
            ("READ", "signal") : ("PARSE", "control"),
            ("PARSE", "signal") : ("ENC", "control"),
            ("ENC", "signal") : ("WRITE", "control"),
        },
    ).run()