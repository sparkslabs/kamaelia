#! /usr/bin/env python
import time

from Kamaelia.Apps.Jam.MusicTiming import MusicTimingComponent

class SendQuantizer(MusicTimingComponent):
    def __init__(self, beatQuantize=(0, 1, 0), *args, **kwargs):
        super(SendQuantizer, self).__init__(*args, **kwargs)
        self.buffer = []
        self.quantizeLength = self.bbfToTime(*beatQuantize)

    def main(self):
        # Wait 'til we hit the start of a bar before we start quantizing
        while self.beat != 1:
            self.updateTiming()
        self.lastSendTime = self.lastBeatTime
        while 1:
            if time.time() >= self.lastSendTime + self.quantizeLength:
                self.sendBuffer()
                self.lastSendTime += self.quantizeLength
            if self.dataReady("inbox"):
                self.buffer.append(self.recv("inbox"))
            self.updateTiming()

    def sendBuffer(self):
        for item in self.buffer:
            self.send(item, "outbox")
        self.buffer = []

