"""
================
Sine Synthesizer
================

Components for playing sine waves.  SineOsc produces a continuous sine 
tone, whereas SineVoice can be turned on and off and change its frequency by
sending messages to its "inbox" inbox.  Turn the voice on by sending a
("On", (noteNumber, frequency, velocity)) tuple.  The noteNumber argument
is used for linking with a polyphoniser, and is ignored in the component. Turn
the voice off by sending a tuple with "Off" as its first item.

SineSynth is a prefab which creates a number of Sine Voices connected in a
synth

Example Usage
-------------

Play a continuous sine tone at 1kHz

SineOsc(frequency=1000).run()

A playable monophonic synth

Pipeline(PianoRoll(), SineVoice()).run()

A playable polyphonic synth

Pipeline(PianoRoll(), SineSynth()).run()

How it works
------------

The oscillator and voice components initialise the pygame mixer, then set up a
regular event which calls every time more data is needed (i.e. every
bufferSize/sampleRate).  They fill the pygame buffer and queue, then whenever
there is a message on their "event" inbox they make an array of samples, and
queue them in the mixer channel.  The SineVoice component only plays if it is
turned on, storing the frequency and velocity which are provided in the
note-on message.
"""
import pygame
import Numeric
import time

from Axon.Apps.Jam.SchedulingComponent import SchedulingComponent
from Kamaelia.Apps.Jam.Audio.Synth import Synth

class SineOsc(SchedulingComponent):
    Inboxes = {"inbox" : "NOT USED",
               "control" : "NOT USED", # FIXME
               "event" : "Messages indicating data is needed",
              }
    Outboxes = {"outbox" : "NOT USED",
                "signal" : "NOT USED", # FIXME
               }
    sampleRate = 44100
    bufferSize = 1024
    frequency = 440
    amplitude = 0.7 

    def __init__(self, **argd):
        super(SineOsc, self).__init__(**argd)
        self.period = float(self.bufferSize)/self.sampleRate
        self.phase = 0

        if not pygame.mixer.get_init():
            pygame.mixer.init(self.sampleRate, -16, 1, self.bufferSize)
            pygame.mixer.set_num_channels(0)
        numChannels = pygame.mixer.get_num_channels() + 1
        pygame.mixer.set_num_channels(numChannels)
        self.channel = pygame.mixer.Channel(numChannels - 1)

        self.lastSendTime = time.time()
        self.scheduleAbs("Send", self.lastSendTime + self.period)

    def generateSample(self, frequency, amplitude, phase):
        """
        Generates one sample of a sine wave with a given frequency, amplitude
        and phase offset
        """ 
        # Working from the formula y(t) = Asin(wt + c)
        # w
        angularFreq = 2 * Numeric.pi * frequency
        # t
        sampleLength = 1.0/self.sampleRate
        # wt for each sample
        sample = Numeric.arange(self.bufferSize) * angularFreq * sampleLength
        # c for each sample
        phaseArray = Numeric.ones(self.bufferSize) * phase
        # wt + c for each sample
        sample += phaseArray
        # sin(wt + c) for each sample
        sample = Numeric.sin(sample)
        # Asin(wt + c) for each sample
        sample *= self.amplitude
        # Update the phase
        phase += angularFreq * sampleLength * self.bufferSize
        phase %= (2 * Numeric.pi)
        return sample, phase

    def main(self):
        while 1:
            if self.dataReady("event"):
                self.recv("event")
                sample, phase = self.generateSample(self.frequency,
                                                    self.amplitude,
                                                    self.phase)
                self.phase = phase
                sample *= 2**15-1
                sample = sample.astype("i")
                sample = Numeric.asarray(sample)
                self.channel.queue(pygame.sndarray.make_sound(sample))

                self.lastSendTime += self.period
                self.scheduleAbs("Send", self.lastSendTime + self.period)
                
            if not self.anyReady():
                self.pause()

class SineVoice(SineOsc):
    Inboxes = {"inbox" : "Note-on and note-off messages",
               "control" : "NOT USED", # FIXME
               "event" : "Messages indicating data is needed",
              }
    Outboxes = {"outbox" : "NOT USED",
                "signal" : "NOT USED", # FIXME
               }

    def __init__(self, **argd):
        super(SineVoice, self).__init__(**argd)
        self.on = False
        if not pygame.mixer.get_init():
            pygame.mixer.init(self.sampleRate, -16, 1, self.bufferSize)
            pygame.mixer.set_num_channels(0)
        numChannels = pygame.mixer.get_num_channels() + 1
        pygame.mixer.set_num_channels(numChannels)
        self.channel = pygame.mixer.Channel(numChannels - 1)

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
                    while self.channel.get_queue() == None:
                        sample, phase = self.generateSample(self.frequency,
                                                            self.amplitude,
                                                            self.phase)
                        self.phase = phase
                        sample *= 2**15-1
                        sample = sample.astype("i")
                        self.channel.queue(pygame.sndarray.make_sound(sample))
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
    from Kamaelia.Chassis.Pipeline import Pipeline
    
    if 0:
        SineOsc().run()

    Pipeline(PianoRoll(), SineSynth()).run()
