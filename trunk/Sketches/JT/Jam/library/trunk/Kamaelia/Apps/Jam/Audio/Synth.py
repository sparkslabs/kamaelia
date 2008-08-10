import Axon
from Kamaelia.Apps.Jam.Audio.Polyphony import Polyphoniser

class Synth(Axon.Component.component):
    polyphony = 8
    polyphoniser = Polyphoniser

    def __init__(self, voiceGenerator, **argd):
        super(Synth, self).__init__(**argd)
        polyphoniser = self.polyphoniser(**argd).activate()
        self.link((self, "inbox"), (polyphoniser, "inbox"), passthrough=1)

        for index, voice in enumerate(voiceGenerator()):
            voice = voice.activate()
            self.link((polyphoniser, "voice%i" % index), (voice, "inbox"))

    def main(self):
        while 1:
            if not self.anyReady():
                self.pause()
            yield 1
