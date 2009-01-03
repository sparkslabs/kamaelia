"""
==========
Mono Mixer
==========

A simple n-channel mono audio mixer.  Send 1D numpy arrays of a fixed length 
to the "in" inboxs (in0, in1 ... inN-2, inN-1) and they will be mixed and sent
as a single numpy array to the "outbox" outbox.  Incoming buffers must be sent
at the correct rate (i.e. intervals of buffer size/sample rate).  If a channel
has no audio to be mixed you can either send an array of zeros, None, or send
no data at all.

Example Usage
-------------
Mixing two sine tones at different frequencies (or how I learned to stop
worrying and love additive synthesis)

Graphline(s1=SineOsc(frequency=440),
          s2=SineOsc(frequency=880),
          mixer=MonoMixer(channels=2),
          output=RTOutput(),
          linkages={("s1", "outbox"), ("mixer", "in0"),
                    ("s2", "outbox"), ("mixer", "in1"),
                    ("mixer", "outbox"), ("output", "in1")).run()
                    

How it works
------------
The mixer is a scheduling component which is regular woken when new data needs
to be send to the output.  When data is received on one of its "in" inboxes it
is added to a numpy array if it is not None.  When the send event is received
on the "event" inbox each value in the ouput array is divided by the number of
channels, and the array is sent to the "outbox" outbox.  The array is then
reset to zeros, and the process starts again.
"""



import numpy
import Axon
import time
from Axon.SchedulingComponent import SchedulingAdaptiveCommsComponent

class MonoMixer(SchedulingAdaptiveCommsComponent):
    channels = 8
    bufferSize = 1024
    sampleRate = 44100

    def __init__(self, **argd):
        super(MonoMixer, self).__init__(**argd)
        for i in range(self.channels):
            self.addInbox("in%i" % i)
        self.period = float(self.bufferSize)/self.sampleRate
        self.lastSendTime = time.time()
        self.scheduleAbs("Send", self.lastSendTime + self.period)


    def main(self):
        output = None
        while 1:
            if self.dataReady("event"):
                self.recv("event")
                if output != None:
                    output /= self.channels
                    self.send(output, "outbox")
                    output = None
                self.lastSendTime += self.period
                self.scheduleAbs("Send", self.lastSendTime + self.period)
            elif self.dataReady("control"):
                # TODO: Do stuff here
                self.recv("control")
            else:
                # Message came from one of the inboxes
                for i in range(self.channels):
                    if self.dataReady("in%i" % i):
                        data = self.recv("in%i" % i)
                        if output != None:
                            output += data
                        else:
                            output = data
            if not self.anyReady():
                self.pause()

if __name__ == "__main__":
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Apps.Jam.Audio.SineSynth import SineOsc
    from Kamaelia.Apps.Jam.Audio.PyGameOutput import PyGameOutput
    Graphline(s1=SineOsc(frequency=440),
              s2=SineOsc(frequency=880),
              mixer=MonoMixer(channels=2),
              output=PyGameOutput(),
              linkages={("s1", "outbox"):("mixer", "in0"),
                        ("s2", "outbox"):("mixer", "in1"),
                        ("mixer", "outbox"):("output", "inbox")}).run()
