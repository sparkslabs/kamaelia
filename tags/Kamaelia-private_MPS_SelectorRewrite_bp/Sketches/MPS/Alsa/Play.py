#!/usr/bin/python

import Axon
import alsaaudio
import time

class SimpleReader(Axon.Component.component):
    def __init__(self, filename, chunksize=320):
        super(SimpleReader, self).__init__()
        self.filename = filename
        self.chunksize = chunksize
    def main(self):
        f = open(self.filename, "r")
        data = f.read(self.chunksize)
        while len(data) > 0:
            self.send(data, "outbox")
            yield 1
            data = f.read(self.chunksize)
        self.send(Axon.Ipc.producerFinished(), "signal")
        print "finished reading"

class AlsaPlayer(Axon.Component.component):
    def main(self):
        out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK)
        out.setchannels(2)
        out.setrate(44100)
        out.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        out.setperiodsize(160)
        loops = 10000
        shutdown = False
        while not shutdown or self.dataReady("inbox"):
            loops -= 1
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                out.write(data)
            if self.dataReady("control"):
                data = self.recv("control")
                if isinstance(data,Axon.Ipc.producerFinished):
                    self.send(data, "signal")
                    shutdown = True
            yield 1
        print "Shutdown :-)"

if __name__ == "__main__":
    from Kamaelia.Util.PipelineComponent import pipeline
    pipeline(
        SimpleReader("audio.raw"),
        AlsaPlayer(),
    ).run()
