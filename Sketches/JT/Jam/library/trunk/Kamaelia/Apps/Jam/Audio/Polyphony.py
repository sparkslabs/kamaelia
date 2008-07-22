import Axon

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
                    if None in self.voices:
                        index = self.voices.index(None)
                        self.voices[index] = noteNumber
                        self.send((address, arguments), "voice%i" % index)
                    else:
                        # Verbose - we ignore the note if the level of polyphony
                        # isn't high enough
                        pass
                elif address == "Off":
                    noteNumber, frequency = arguments
                    if noteNumber in self.voices:
                        index = self.voices.index(noteNumber)
                        self.voices[index] = None
                        self.send((address, arguments), "voice%i" % index)
            if not self.anyReady():
                self.pause()
            yield 1

