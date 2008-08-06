import numpy
import Axon
import time
from Axon.SchedulingComponent import SchedulingAdaptiveCommsComponent

class MonoMixer(SchedulingAdaptiveCommsComponent):
    channels = 8
    bufferSize = 1024
    sampleRate = 44100

    def __init__(self, **argd):
        super(MonoMixer, self).__init__(**argd)
        for i in range(self.channels):
            self.addInbox("in%i" % i)
        self.period = float(self.bufferSize)/self.sampleRate
        self.lastSendTime = time.time()
        self.scheduleAbs("Send", self.lastSendTime + self.period)


    def main(self):
        while 1:
            if self.dataReady("event"):
                output = numpy.zeros(self.bufferSize)
                self.recv("event")
                for i in range(self.channels):
                    if self.dataReady("in%i" % i):
                        data = self.recv("in%i" % i)
                        if data != None:
                            output += data
                output /= self.channels
                self.send(output, "outbox")
                self.lastSendTime += self.period
                self.scheduleAbs("Send", self.lastSendTime + self.period)
            else:
                self.pause()
