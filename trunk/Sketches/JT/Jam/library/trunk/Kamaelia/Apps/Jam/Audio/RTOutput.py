import Axon
import RtAudio
import numpy

class RTOutput(Axon.Component.component):
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
                if self.io.needWrite() >= self.bufferSize:
                    self.io.write(self.recv("inbox"))
                else:
                    print "Overflow"
                    self.recv("inbox")
            if not self.anyReady():
                self.pause()
            yield 1

if __name__ == "__main__":
    from Kamaelia.Apps.Jam.Audio.SineSynth import SineOsc
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    Pipeline(SineOsc(), RTOutput(outputDevice=2)).run()

