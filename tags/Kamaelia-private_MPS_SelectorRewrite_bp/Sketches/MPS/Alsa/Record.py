#!/usr/bin/python

import Axon
import alsaaudio
import time

class AlsaRecorder(Axon.Component.component):
    def main(self):
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
        inp.setchannels(2)
        inp.setrate(44100)
        inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        inp.setperiodsize(160)
        loops = 1000000
        t = time.time()
        while 1:
            yield 1
            if time.time() - t > 0.001:
                # Read data from device
                l,data = inp.read()
                if l:
                  self.send(data, "outbox")
                t= time.time()




if __name__ == "__main__":
    from Kamaelia.File.Writing import SimpleFileWriter
    from Kamaelia.Util.PipelineComponent import pipeline
    
    pipeline(
        AlsaRecorder(),
        SimpleFileWriter("audio.raw")
    ).run()
