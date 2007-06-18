#!/usr/bin/python

import Axon
import alsaaudio
import time

class AlsaRecorder(Axon.Component.component):
    def main(self):
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
        inp.setchannels(1)
        inp.setrate(11025)
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

class AlsaPlayer(Axon.Component.component):
    def main(self):
        out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK)
        out.setchannels(1)
        out.setrate(11025)
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
