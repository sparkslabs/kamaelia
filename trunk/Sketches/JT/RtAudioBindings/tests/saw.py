import RtAudio
import numpy
import time

# ID of the output device.  You can find this from printIODevices.py
deviceId = 2

sampleRate = 44100
bufferSize = 1024

rate = 0.005

def sawGen(bufferSize):
    """ Make a numpy array with a saw wave in """
    lastValue = 0
    while 1:
        sawValues = []
        for i in range(bufferSize):
            sawValues.append(lastValue)
            lastValue += rate
            if lastValue > 1:
                lastValue -= 2
        arr = numpy.array(sawValues)
        yield arr

makeSaw = sawGen(1024)

def saw(oops):
    # Blank the output buffer
    sawWave = makeSaw.next()
    return sawWave

if __name__ == "__main__":
    io = RtAudio.RtAudio()
    io.openStream(deviceId, sampleRate, bufferSize)
    io.startStream()
    while 1:
        try:
            if io.needWrite() >= bufferSize:
                io.write(saw())
            else:
                time.sleep(float(bufferSize)/sampleRate)
        except KeyboardInterrupt:
            break
    io.stopStream()
    io.closeStream()
