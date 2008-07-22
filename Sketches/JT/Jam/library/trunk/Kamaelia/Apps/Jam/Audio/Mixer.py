import numpy
import Axon

class MonoMixer(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    channels = 8
    bufferSize = 1024

    def __init__(self, **argd):
        super(MonoMixer, self).__init__(**argd)
        for i in range(self.channels):
            self.addInbox("in%i" % i)

    def main(self):
        while 1:
            output = numpy.zeros(self.bufferSize)
            for i in range(self.channels):
                if self.dataReady("in%i" % i):
                    output += self.recv("in%i" % i)
            output /= self.channels
            self.send(output, "outbox")
            if not self.anyReady():
                self.pause()
            yield 1

