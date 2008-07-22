import time
import wave
import pygame
import numpy
import Axon

from Axon.SchedulingComponent import SchedulingComponent
from Kamaelia.Apps.Jam.Audio.Synth import Synth
from Kamaelia.Apps.Jam.Audio.Polyphony import Targetter

class WavVoice(SchedulingComponent):
    bufferSize = 1024
    def __init__(self, fileName, **argd):
        super(WavVoice, self).__init__(**argd)

        self.on = False

        self.wavFile = wave.open(fileName)
        self.sampleRate = self.wavFile.getframerate()
        self.period = float(self.bufferSize)/self.sampleRate

        self.frame = 0

        self.lastSendTime = time.time()
        self.scheduleAbs("Send", self.lastSendTime + self.period)

    def main(self):
        while 1:
            if self.dataReady("inbox"):
                address, arguments = self.recv("inbox")
                address = address.split("/")[-1]
                if address == "On":
                    self.on = True
                    self.wavFile.rewind()
                    self.frame = 0
                if address == "Off":
                    self.on = False

            if self.dataReady("event"):
                self.recv("event")
                if self.on:
                    if self.frame < self.wavFile.getnframes():
                        sample = self.wavFile.readframes(self.bufferSize)
                        sample = numpy.frombuffer(sample, dtype="int16")
                        self.frame += len(sample)
                        if len(sample) < self.bufferSize:
                            # Pad with zeroes
                            padSize = self.bufferSize - len(sample)
                            sample = numpy.append(sample, numpy.zeros(padSize))
                        # Convert to float
                        sample = sample.astype("float64")
                        # Scale to -1 - 1
                        sample /= 2**(8 * self.wavFile.getsampwidth() - 1)
                    else:
                        sample = numpy.zeros(self.bufferSize)
                else:
                    sample = numpy.zeros(self.bufferSize)
                self.send(sample, "outbox")
                self.lastSendTime += self.period
                self.scheduleAbs("Send", self.lastSendTime + self.period)

            if not self.anyReady():
                self.pause()

def Sampler(fileList):
    def voiceGenerator():
        for fileName in fileList:
            yield WavVoice(fileName)
    return Synth(voiceGenerator, polyphoniser=Targetter,
                 polyphony=len(fileList))
    

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Apps.Jam.Util.Numpy import TypeConverter
    from Kamaelia.Codec.Vorbis import AOAudioPlaybackAdaptor
    from Kamaelia.Util.PureTransformer import PureTransformer
    from Kamaelia.Apps.Jam.UI.StepSequencer import StepSequencer
    from Kamaelia.Apps.Jam.Audio.Synth import Synth
    from Kamaelia.Apps.Jam.Audio.Polyphony import Targetter

    files = ["Ride", "HH", "Snare", "Kick"]
    files = ["/home/joe/Desktop/%s.wav"%fileName for fileName in files]

    Pipeline(StepSequencer(stepsPerBeat=4), Sampler(files),
             PureTransformer(lambda x:x*(2**15-1)),
             TypeConverter(type="int16"), AOAudioPlaybackAdaptor()).run()
    
                
            
