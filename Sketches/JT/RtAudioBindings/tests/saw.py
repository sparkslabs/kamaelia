import RtAudio
import numpy
import sys

# ID of the output device.  You can find this from printIODevices.py
deviceId = 0
# Use signed 16 bit ints
# Constant will eventually be defined in RtAudio
format = 0x2

sampleRate = 44100
bufferSize = 1024

rate = 0.005

def sawGen(bufferSize):
    """ Make a numpy array with a saw wave in """
    lastValue = 0
    print 1
    while 1:
        arr = numpy.array([])
        for i in range(bufferSize):
            arr = numpy.append(arr, lastValue)# * (2**15-1))
            lastValue += rate
            if lastValue > 1:
                lastValue -= 2
        yield arr

def saw(outputBuffer, inputBuffer, bufferSize, streamTime, status, sawGen):
    # Blank the output buffer
    outputBuffer *= 0
    outputBuffer += sawGen.next()

if __name__ == "__main__":

    io = RtAudio.RtAudio()
    io.openStream(deviceId, # Output device ID
                  1,        # Mono
                  0,        # No channel offset
                  0,        # Input device
                  1,        # Number of input channels
                  0,        # Input offset
                  format, sampleRate, bufferSize, # Sound options
                  saw, # The audio callback
                  sawGen(bufferSize))     # Extra data to the callback
    io.startStream()
    raw_input("Press a key to stop it!")
    io.stopStream()
    io.closeStream()
