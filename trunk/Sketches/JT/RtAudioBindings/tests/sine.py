import RtAudio
import numpy
import time

# ID of the output device.  You can find this from printIODevices.py
deviceId = 2

sampleRate = 44100
bufferSize = 1024

frequency = 440

def sineGen(bufferSize):
    """ Make a numpy array with a saw wave in """
    phase = 0
    while 1:
        # Working from the formula y(t) = Asin(wt + c)
        # w
        angularFreq = 2 * numpy.pi * frequency
        # t
        sampleLength = 1.0/sampleRate
        # wt for each sample
        sample = numpy.arange(bufferSize) * angularFreq * sampleLength
        # c for each sample
        phaseArray = numpy.ones(bufferSize) * phase
        # wt + c for each sample
        sample += phaseArray
        # sin(wt + c) for each sample
        sample = numpy.sin(sample)
        # Update the phase
        phase += angularFreq * sampleLength * bufferSize
        phase %= (2 * numpy.pi)
        yield sample

makeSine = sineGen(1024)

def sine():
    # Blank the output buffer
    sineWave = makeSine.next()
    return sineWave

if __name__ == "__main__":
    io = RtAudio.RtAudio()
    io.openStream(deviceId, sampleRate, bufferSize)
    io.startStream()
    while 1:
        try:
            if io.needWrite() >= bufferSize:
                io.write(sine())
            else:
                time.sleep(float(bufferSize)/sampleRate)
        except KeyboardInterrupt:
            break
    io.stopStream()
    io.closeStream()
