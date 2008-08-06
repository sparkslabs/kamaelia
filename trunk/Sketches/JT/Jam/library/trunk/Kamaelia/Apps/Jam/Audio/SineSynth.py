import pygame
import Axon
from Axon.SchedulingComponent import SchedulingComponent
import numpy
import time
from Kamaelia.Apps.Jam.Audio.Synth import Synth

class SineOsc(Axon.SchedulingComponent.SchedulingComponent):
    sampleRate = 44100
    bufferSize = 1024
    frequency = 440
    amplitude = 0.7 

    def __init__(self, **argd):
        super(SineOsc, self).__init__(**argd)
        self.period = float(self.bufferSize)/self.sampleRate
        self.phase = 0
        self.lastSendTime = time.time()
        self.scheduleAbs("Send", self.lastSendTime + self.period)

    def generateSample(self, frequency, amplitude, phase):
        """
        Generates one sample of a sine wave with a given frequency, amplitude
        and phase offset
        """ 
        # Working from the formula y(t) = Asin(wt + c)
        # w
        angularFreq = 2 * numpy.pi * frequency
        # t
        sampleLength = 1.0/self.sampleRate
        # wt for each sample
        sample = numpy.arange(self.bufferSize) * angularFreq * sampleLength
        # c for each sample
        phaseArray = numpy.ones(self.bufferSize) * phase
        # wt + c for each sample
        sample += phaseArray
        # sin(wt + c) for each sample
        sample = numpy.sin(sample)
        # Asin(wt + c) for each sample
        sample *= self.amplitude
        # Update the phase
        phase += angularFreq * sampleLength * self.bufferSize
        phase %= (2 * numpy.pi)
        return sample, phase

    def main(self):
        while 1:
            if self.dataReady("event"):
                self.recv("event")
                sample, phase = self.generateSample(self.frequency,
                                                    self.amplitude,
                                                    self.phase)
                self.phase = phase
                self.send(sample, "outbox")

                self.lastSendTime += self.period
                self.scheduleAbs("Send", self.lastSendTime + self.period)
                
            if not self.anyReady():
                self.pause()

class SineVoice(SineOsc):
    def __init__(self, **argd):
        super(SineVoice, self).__init__(**argd)
        self.on = False

    def main(self):
        while 1:
            if self.dataReady("inbox"):
                address, arguments = self.recv("inbox")
                address = address.split("/")[-1]
                if address == "On":
                    self.on = True
                    noteNumber, frequency, velocity = arguments
                    self.frequency = frequency
                    self.amplitude = velocity
                elif address == "Off":
                    self.on = False
                
            if self.dataReady("event"):
                self.recv("event")
                if self.on:
                    sample, phase = self.generateSample(self.frequency,
                                                        self.amplitude,
                                                        self.phase)
                    self.phase = phase
                else:
                    sample = None
                self.send(sample, "outbox")

                self.lastSendTime += self.period
                self.scheduleAbs("Send", self.lastSendTime + self.period)
            if not self.anyReady():
                self.pause()

def SineSynth(polyphony=8, **argd):
    def voiceGenerator():
        for i in range(polyphony):
            yield SineVoice(**argd)
    return Synth(voiceGenerator, polyphony=polyphony, **argd)

if __name__ == "__main__":
    from Kamaelia.Apps.Jam.UI.PianoRoll import PianoRoll
    from Kamaelia.Apps.Jam.Audio.Synth import Synth
    from Kamaelia.Apps.Jam.Util.Numpy import TypeConverter
    from Kamaelia.Apps.Jam.Audio.RTOutput import RTOutput
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.PureTransformer import PureTransformer

    Pipeline(PianoRoll(), SineSynth(),
             RTOutput(outputDevice=0)).run()
