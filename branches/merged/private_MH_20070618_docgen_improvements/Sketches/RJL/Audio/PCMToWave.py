from Axon.Component import component
import string
import struct
from Axon.Ipc import producerFinished, shutdown

class PCMToWave(component):
    def __init__(self, bytespersample, samplingfrequency):
        super(PCMToWave, self).__init__()
        self.bytespersample = bytespersample
        self.samplingfrequency = samplingfrequency
        
        if self.bytespersample not in [2,4]:
            print "Currently bytespersample must be 2 or 4"
            raise ValueError
        
        bytestofunction = { 2: self.sample2Byte, 4: self.sample4Byte }
        self.pack = bytestofunction[self.bytespersample]
        
    def sample2Byte(self, value):
        return struct.pack("<h", int(value * 32768.0))

    def sample4Byte(self, value):
        return struct.pack("<l", int(value * 2147483648.0))
                
    def main(self):
        #we don't know the length yet, so we say the file lasts an arbitrary (long) time 
        riffchunk = "RIFF" + struct.pack("<L", 0xEFFFFFFF) + "WAVE"
        
        bytespersecond = self.bytespersample * self.samplingfrequency
        
        formatchunk = "fmt "
        formatchunk += struct.pack("<L", 0x10) #16 for PCM
        formatchunk += struct.pack("<H", 0x01) #PCM/Linear quantization
        formatchunk += struct.pack("<H", 0x01) #mono
        formatchunk += struct.pack("<L", self.samplingfrequency)
        formatchunk += struct.pack("<L", bytespersecond)
        formatchunk += struct.pack("<H", self.bytespersample)
        formatchunk += struct.pack("<H", self.bytespersample * 8)
    
        self.send(riffchunk, "outbox")
        self.send(formatchunk, "outbox")
        datachunkheader = "data" + struct.pack("<L", 0xEFFFFFFF) #again, an arbitrary (large) value
        self.send(datachunkheader, "outbox")
        
        running = True
        while running:
            yield 1
            
            codedsamples = []
            while self.dataReady("inbox"): # we accept lists of floats
                samplelist = self.recv("inbox")
                
                for sample in samplelist:
                
                    if sample < -1:
                        sample = -1
                    elif sample > 1:
                        sample = 1
                    
                    codedsamples.append(self.pack(sample))
                
                del samplelist
                
            if codedsamples:
                self.send(string.join(codedsamples, ""), "outbox")
                
            while self.dataReady("control"): # we accept lists of floats
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdown):
                    return
                    
            self.pause()
