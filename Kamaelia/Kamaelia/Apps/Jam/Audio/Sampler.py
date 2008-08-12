import time
import wave
import pygame
import numpy
import Axon

from Kamaelia.Apps.Jam.Audio.Synth import Synth
from Kamaelia.Apps.Jam.Audio.Polyphony import Targetter

class WavVoice(Axon.Component.component):
    bufferSize = 1024
    sampleRate = 44100

    def __init__(self, fileName, **argd):
        super(WavVoice, self).__init__(**argd)
        if not pygame.mixer.get_init():
            pygame.mixer.init(self.sampleRate, -16, 1, self.bufferSize)
            pygame.mixer.set_num_channels(0)
        # Make a new channel
        numChannels = pygame.mixer.get_num_channels() + 1
        pygame.mixer.set_num_channels(numChannels)
        self.channel = pygame.mixer.Channel(numChannels - 1)
        self.sound = pygame.mixer.Sound(fileName)

    def main(self):
        while 1:
            if self.dataReady("inbox"):
                address, arguments = self.recv("inbox")
                address = address.split("/")[-1]
                if address == "On":
                    self.channel.play(self.sound)
            if not self.anyReady():
                self.pause()
            yield 1

def Sampler(fileList, **argd):
    def voiceGenerator():
        for fileName in fileList:
            yield WavVoice(fileName, **argd)
    return Synth(voiceGenerator, polyphoniser=Targetter,
                 polyphony=len(fileList), **argd)
    

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Apps.Jam.UI.StepSequencer import StepSequencer

    files = ["Ride", "HH", "Snare", "Kick"]
    files = ["/home/joe/Desktop/%s.wav"%fileName for fileName in files]

    Pipeline(StepSequencer(stepsPerBeat=4), Sampler(files)).run()
