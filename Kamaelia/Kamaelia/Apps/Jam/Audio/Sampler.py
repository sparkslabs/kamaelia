"""
=========
Wav Voice
=========

A simple wave file player using the pygame mixer.  It can be controlled by
sending an ("On",) tuple to the "inbox" inbox, which starts the file playing
from the beginning.

Also contains a sampler component which links a number of wav voices, and
responds to ("On", channel) messages, where channel is the index of the voice.

Example Usage
-------------

Play the file Snare.wav once

Pipeline(DataSource(("On",)),
         WavVoice("Snare.wav")).run()

A playable four channel sampler

files = ["Ride.wav", "HH.wav", "Snare.wav", "Kick.wav"]

Pipeline(StepSequencer(),
         Sampler(files)).run()

"""

import time
import pygame
import Axon

from Kamaelia.Apps.Jam.Audio.Synth import Synth
from Kamaelia.Apps.Jam.Audio.Polyphony import Targetter

# FIXME: I probably play more than just Wavs now - rename me :)
class WavVoice(Axon.Component.component):
    """
    WavVoice(bufferSize, sampleRate) -> new WavVoice component

    A simple wave file player using the pygame mixer
    """
    bufferSize = 1024
    sampleRate = 44100

    def __init__(self, fileName, **argd):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """
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
        """ Main loop """
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
