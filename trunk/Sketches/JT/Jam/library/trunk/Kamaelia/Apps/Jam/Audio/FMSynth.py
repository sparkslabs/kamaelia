import pygame
import Axon
from Axon.SchedulingComponent import SchedulingComponent
import numpy
import time

class FMSineOsc(Axon.SchedulingComponent.SchedulingComponent):
    pass

class SineOsc(Axon.SchedulingComponent.SchedulingComponent):
    sampleRate = 44100
    bufferSize = 1024
    polyphony = 8
    
    def __init__(self, **argd):
        super(FMSynth, self).__init__(**argd)
        self.notes = {}
        self.period = float(self.bufferSize)/self.sampleRate
        self.lastSendTime = time.time()
        self.scheduleAbs("Send", self.lastSendTime + self.period)

    def generateSine(self, frequency, amplitude, phase):
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
        sample *= amplitude
        # Update the phase
        phase += angularFreq * sampleLength * self.bufferSize
        phase %= (2 * numpy.pi)
        return (sample, phase)

    def main(self):
        while 1:
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                address = data[0].split("/")[-1]
                if address == "On":
                    noteNumber, frequency, velocity = data[1]
                    self.notes[noteNumber] = {"frequency" : frequency,
                                              "velocity" : velocity,
                                              "phase": 0}

                elif address == "Off":
                    noteNumber, frequency = data[1]
                    if self.notes.has_key(noteNumber):
                        del self.notes[noteNumber]

            if self.dataReady("event"):
                if self.recv("event") == "Send":
                    output = numpy.zeros(self.bufferSize)
                    for noteNumber, note in self.notes.items():
                        sample, phase = self.generateSine(note["frequency"],
                                                 note["velocity"] * (2**15 - 1),
                                                          note["phase"])
                        output += sample
                        self.notes[noteNumber]["phase"] = phase
                    output = output.astype("int16")
                    self.send(output, "outbox")
                    self.lastSendTime += self.period
                    self.scheduleAbs("Send", self.lastSendTime + self.period)

            if not self.anyReady():
                self.pause()

class SineOsc(Axon.SchedulingComponent.SchedulingComponent):
    sampleRate = 44100
    bufferSize = 1024
    frequency = 440
    amplitude = 0.7 * (2**15 - 1)

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
                    self.amplitude = velocity * (2**15 - 1)
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
                    sample = numpy.zeros(self.bufferSize)
                self.send(sample, "outbox")

                self.lastSendTime += self.period
                self.scheduleAbs("Send", self.lastSendTime + self.period)
            if not self.anyReady():
                self.pause()

class Polyphoniser(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    polyphony = 8
    def __init__(self, **argd):
        super(Polyphoniser, self).__init__(**argd)
        self.voices = []
        for i in range(self.polyphony):
            self.addOutbox("voice%i" % i)
            self.voices.append(None)

    def main(self, **argd):
        while 1:
            if self.dataReady("inbox"):
                address, arguments = self.recv("inbox")
                address = address.split("/")[-1]
                if address == "On":
                    noteNumber = arguments[0]
                    if None in a:
                        index = self.voices.index[None]
                        self.voices[index] = noteNumber
                        self.send((address, arguments), "voice%i" % index)
                    else:
                        # Verbose - we ignore the note if the level of polyphony
                        # isn't high enough
                        pass
                elif address == "Off":
                    noteNumber, frequency = arguments
                    if noteNumber in self.voices:
                        index = self.voices.index[noteNumber]
                        self.voices[index] = None
                        self.send((address, arguments), "voice%i" % index)
            if not self.anyReady():
                self.pause()
            yield 1

class NumpyTypeConverter(Axon.Component.component):
    type = None
    def main(self):
        while 1:
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                if self.type != None:
                    self.send(data.astype(self.type), "outbox")
            if not self.anyReady():
                self.pause()
            yield 1
            

if __name__ == "__main__":
    from Kamaelia.Apps.Jam.UI.PianoRoll import PianoRoll
    from Kamaelia.Codec.Vorbis import AOAudioPlaybackAdaptor
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.File.Writing import SimpleFileWriter
    from Kamaelia.Codec.WAV import WAVWriter

    Pipeline(PianoRoll(), SineVoice(), NumpyTypeConverter(type="int16"), AOAudioPlaybackAdaptor()).run()
#    Pipeline(PianoRoll(), SimpleSine(), AOAudioPlaybackAdaptor()).run()
#    Pipeline(SimpleSine(), WAVWriter(1, "S16_LE", 44100), SimpleFileWriter("test.wav")).run()


