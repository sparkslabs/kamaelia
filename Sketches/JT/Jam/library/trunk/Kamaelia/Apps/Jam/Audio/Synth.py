import Axon
from Kamaelia.Apps.Jam.Audio.Polyphony import Polyphoniser
from Kamaelia.Apps.Jam.Audio.Mixer import MonoMixer

class Synth(Axon.Component.component):
    polyphony = 8
    polyphoniser = Polyphoniser

    def __init__(self, voiceGenerator, **argd):
        super(Synth, self).__init__(**argd)
        polyphoniser = self.polyphoniser(polyphony=self.polyphony).activate()
        mixer = MonoMixer(channels=self.polyphony).activate()
        self.link((self, "inbox"), (polyphoniser, "inbox"), passthrough=1)
        self.link((mixer, "outbox"), (self, "outbox"), passthrough=2)

        for index, voice in enumerate(voiceGenerator()):
            voice = voice.activate()
            self.link((polyphoniser, "voice%i" % index), (voice, "inbox"))
            self.link((voice, "outbox"), (mixer, "in%i" % index))

    def main(self):
        while 1:
            if not self.anyReady():
                self.pause()
            yield 1
