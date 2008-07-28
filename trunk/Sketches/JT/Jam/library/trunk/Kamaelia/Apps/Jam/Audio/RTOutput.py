import Axon
import RtAudio

class RTOutput(Axon.Component.component):
    channels = 2
    type = 0x2 # INT16 - will add these into binding
    sampleRate = 44100
    bufferSize = 1024

    def __init__(self, **argd):
        super(RTOutput, self).__init__(**argd)
        self.io = RtAudio.RtAudio()
        self.io.showWarnings()
        self.io.openStream(0, self.channels, 0, 0, 2, 0, self.type,
                           self.sampleRate, self.bufferSize,
                           self.callback, None)
        self.buffer = None
        self.io.startStream()

    def callback(self, outputBuffer, inputBuffer, bufferSize, streamTime,
                 extraData):
        print "ZOMGGGGGGGGGGGGGGGGGG"
        outputBuffer *= 0
        outputBuffer += self.buffer
        return 5

    def main(self):
        while 1:
            if self.dataReady("inbox"):
                self.buffer = self.recv("inbox")
            if not self.anyReady():
                self.pause()
            yield 1
