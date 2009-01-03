"""
====================
Polyphony Components
====================

Two components for distributing note-on and note-off messages to individual voices.  The polyphoniser is designed for use with synthesized voices, routing messages received on its "inbox" inbox to the first available "voice" outbox (numbered voice0, voice1 ... voiceN-2, voiceN-1).  If no voices are available and the Polyphoniser receives a note-on message it is discarded.

The Targetter is designed for use with samples, routing messages received on its "inbox" inbox to "voice" outboxes based upon the first argument in an (address, (arguments)) tuple.  This is designed so it works simply with the OSC message format used throughout Kamaelia Jam.

Example usage
-------------
A 3 voice polyphonic sine synth

Graphline(pianoRoll = PianoRoll(),
          polyphoniser=Polyphoniser(polyphony=3),
          v0 = SineVoice(),
          v1 = SineVoice(),
          v2 = SineVoice(),
          linkages = {("pianoRoll", "outbox"):("polyphoniser", "inbox"),
                      ("polyphoniser", "voice0"):("v0", "inbox"),
                      ("polyphoniser", "voice1"):("v1", "inbox"),
                      ("polyphoniser", "voice2"):("v2", "inbox")})

A 4 channel sampler

Graphline(stepSequncer = StepSequencer(),
          polyphoniser=Targetter(polyphony=4),
          v0 = WavVoice("kick.wav"),
          v1 = WavVoice("snare.wav"),
          v2 = WavVoice("hh.wav"),
          v3 = "crash.wav",
          linkages = {("stepSequencer", "outbox"):("polyphoniser", "inbox"),
                      ("polyphoniser", "voice0"):("v0", "inbox"),
                      ("polyphoniser", "voice1"):("v1", "inbox"),
                      ("polyphoniser", "voice2"):("v2", "inbox"),
                      ("polyphoniser", "voice2"):("v2", "inbox")})

How the Polphoniser works
-------------------------
When the Polyphoniser receives a note-on message it finds the first instance
of None in a list of voices, and replaces this with the note number.  It then sends the messages through the "voice" outbox corresponding to the list index.  When a note-off message is received it finds the note in the list, send the message through the corresponding "voice" outbox, and replaces the note number with None.  If there is no instance of None in the voices list when a note-on message is received the message is ignored.
"""
import Axon

class Polyphoniser(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    """
    Polyphoniser([polyphony]) -> new Polyphoniser component.

    Routes note-on and off messages based upon their note-number.

    Keyword Arguments:

    - polyphony -- The number of simultaneous voices which can be played using
                   the polyphoniser
    """

    Inboxes = {"inbox" : "Note-on and note-off messages to route to the voices",
               "control": "NOT USED", #FIXME
              }
    Outboxes = {"outbox" : "NOT USED",
                "signal" : "NOT USED", #FIXME
               }
    polyphony = 8
    def __init__(self, **argd):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """
        super(Polyphoniser, self).__init__(**argd)
        self.voices = []
        for i in range(self.polyphony):
            self.addOutbox("voice%i" % i)
            self.voices.append(None)

    def main(self):
        """ Main loop """
        while 1:
            if self.dataReady("inbox"):
                address, arguments = self.recv("inbox")
                address = address.split("/")[-1]
                if address == "On":
                    noteNumber = arguments[0]
                    if None in self.voices:
                        # There is a voice available
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

class Targetter(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    """
    Targetter([polyphony]) -> new Targetter component.

    Routes note-on and off messages to a specific voice.

    Keyword Arguments:

    - polyphony -- The number of voices which can be targetted
    """

    Inboxes = {"inbox" : "Note-on and note-off messages to route to the voices",
               "control": "NOT USED", #FIXME
              }
    Outboxes = {"outbox" : "NOT USED",
                "signal" : "NOT USED", #FIXME
               }
    polyphony = 8
    def __init__(self, **argd):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """
        super(Targetter, self).__init__(**argd)
        for i in range(self.polyphony):
            self.addOutbox("voice%i" % i)

    def main(self):
        """ Main loop """
        while 1:
            if self.dataReady("inbox"):
                address, arguments = self.recv("inbox")
                address = address.split("/")[-1]
                if address == "On" or address == "Off":
                    index = arguments[0]
                    self.send((address, arguments), "voice%i" % index)
            if not self.anyReady():
                self.pause()
            yield 1

