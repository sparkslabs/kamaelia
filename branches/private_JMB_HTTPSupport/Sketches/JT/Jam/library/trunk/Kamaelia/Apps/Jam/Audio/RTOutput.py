import Axon
from Axon.SchedulingComponent import SchedulingComponent
import RtAudio
import numpy
import time

class RTOutput(Axon.ThreadedComponent.threadedcomponent):
    outputDevice = 0
    sampleRate = 44100
    bufferSize = 1024

    def __init__(self, **argd):
        super(RTOutput, self).__init__(**argd)
        self.io = RtAudio.RtAudio()
        self.io.openStream(self.outputDevice, self.sampleRate, self.bufferSize)
        self.io.startStream()

    def main(self):
        while 1:
            if self.dataReady("inbox"):
                while not self.io.needWrite() >= self.bufferSize:
                    time.sleep(0.001)
                self.io.write(self.recv("inbox"))
            if not self.anyReady():
                self.pause()

class SchedulingRTOutput(SchedulingComponent):
    outputDevice = 0
    sampleRate = 44100
    internalBufferSize = 1024
    outputBufferSize = 1024


    def __init__(self, **argd):
        super(SchedulingRTOutput, self).__init__(**argd)
        self.io = RtAudio.RtAudio()
        self.io.openStream(self.outputDevice, self.sampleRate,
                           self.outputBufferSize)
        self.period = float(self.internalBufferSize)/self.sampleRate
        self.lastSendTime = time.time()
        self.scheduleAbs("Send", self.lastSendTime + self.period)
        self.io.startStream()

    def main(self):
        while 1:
            if self.dataReady("event"):
                if self.dataReady("inbox"):
                    while not self.io.needWrite() >= self.internalBufferSize:
                        time.sleep(0.001)
                    data = self.recv("inbox")
                    self.io.write(data)
                    # TODO: Maybe correct for the sleeping above here - test me
                    self.lastSendTime += self.period
                    self.scheduleAbs("Send", self.lastSendTime + self.period)
            else:
                self.pause()

if __name__ == "__main__":
    from Kamaelia.Apps.Jam.Audio.SineSynth import SineOsc
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    Pipeline(SineOsc(), RTOutput(outputDevice=2)).run()

