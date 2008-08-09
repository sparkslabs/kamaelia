import numpy
import Numeric
import pygame
import Axon
import time

class PyGameOutput(Axon.ThreadedComponent.threadedcomponent):
    bufferSize = 1024
    sampleRate = 44100
    def __init__(self, **argd):
        super(PyGameOutput, self).__init__(**argd)
        pygame.mixer.init(self.sampleRate, -16, 1, self.bufferSize)
    
    def main(self):
        while 1:
            if not pygame.mixer.get_init():
                pygame.mixer.init(self.sampleRate, -16, 1, self.bufferSize)
            else:
                if self.dataReady("inbox"):
                    numpyArray = self.recv("inbox")
                    # Scale to 16 bit int
                    numpyArray *= 2**15-1
                    numpyArray = numpyArray.astype("int16")
                    numericArray = Numeric.asarray(numpyArray)
                    sound = pygame.sndarray.make_sound(numericArray)
                    sound.play()

            if not self.anyReady():
                self.pause()

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Apps.Jam.Audio.SineSynth import SineOsc

    Pipeline(SineOsc(), PyGameOutput()).run()
