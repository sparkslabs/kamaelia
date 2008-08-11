import pygame
import Numeric
import time
import Axon
from Axon.SchedulingComponent import SchedulingComponent
from Kamaelia.Apps.Jam.Audio.Synth import Synth

class SineOsc(SchedulingComponent):
    sampleRate = 44100
    bufferSize = 1024
    frequency = 440
    amplitude = 0.7 

    def __init__(self, **argd):
        super(SineOsc, self).__init__(**argd)
        ### HACK - Quick test to see whether decreasing the period will
        ### make playback smoother in SineVoice.
        self.period = float(self.bufferSize)/self.sampleRate/2
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

class SineVoice(Axon.Component.component):
    sampleRate = 44100
    bufferSize = 1024
    # The longest a note can be, for use in an ugly hack to prevent buffering
    # problems
    maxNoteLength = 4 * 4 * 60 / 120 # beats * bars * (60 secs) / bpm

    def __init__(self, **argd):
        super(SineVoice, self).__init__(**argd)
        if not pygame.mixer.get_init():
            pygame.mixer.init(self.sampleRate, -16, 1, self.bufferSize)
            pygame.mixer.set_num_channels(0)
        numChannels = pygame.mixer.get_num_channels() + 1
        pygame.mixer.set_num_channels(numChannels)
        self.channel = pygame.mixer.Channel(numChannels - 1)

    def generateSample(self, frequency, amplitude):
        """
        Generates one sample of a sine wave with a given frequency, amplitude
        and phase offset
        """
        # Working from the formula y(t) = Asin(wt + c)
        numSamples = self.sampleRate/frequency
        # w
        angularFreq = 2 * Numeric.pi * frequency
        # t
        sampleLength = 1.0/self.sampleRate
        # wt for each sample
        sample = Numeric.arange(numSamples) * angularFreq * sampleLength
        # sin(wt + c) for each sample
        sample = Numeric.sin(sample)
        # Asin(wt + c) for each sample
        sample *= amplitude
        return sample

    def main(self):
        while 1:
            if self.dataReady("inbox"):
                address, arguments = self.recv("inbox")
                address = address.split("/")[-1]
                if address == "On":
                    noteNumber, frequency, velocity = arguments
                    self.frequency = frequency
                    self.amplitude = velocity
                    sample = self.generateSample(self.frequency,
                                                 self.amplitude * (2**15 - 1))
                    sample = sample.astype("i")
                    # Hacky - Resize the single sample to the length of the
                    # all the bars.  Prevents a whole multitude of buffering
                    # issues, at the expense of memory and not being a great
                    # big horrible hack...
                    numSamples = self.sampleRate * self.maxNoteLength
                    sample = Numeric.resize(sample, (numSamples,))

                    self.sound = pygame.sndarray.make_sound(sample)
                    self.channel.play(self.sound)
                elif address == "Off":
                    self.channel.stop()
            if not self.anyReady():
                self.pause()
            yield 1

def SineSynth(polyphony=8, **argd):
    def voiceGenerator():
        for i in range(polyphony):
            yield SineVoice(**argd)
    return Synth(voiceGenerator, polyphony=polyphony, **argd)

if __name__ == "__main__":
    from Kamaelia.Apps.Jam.UI.PianoRoll import PianoRoll
    from Kamaelia.Chassis.Pipeline import Pipeline

    Pipeline(PianoRoll(), SineSynth()).run()
