#! /usr/bin/env python
#TODO:
# * Document me
# * Test timing code hard
import time
import sched

from math import floor
from Axon.ThreadedComponent import threadedcomponent

class MusicTimingComponent(threadedcomponent):
    def __init__(self, bpm=120, beatsPerBar=4, beatUnit=4, loopBars=4):
        super(MusicTimingComponent, self).__init__()
        self.bpm = bpm
        self.beatsPerBar = beatsPerBar
        self.beatUnit = beatUnit
        self.loopBars = loopBars

        self.playing = 1
        self.beat = 0
        self.bar = 0
        self.loopBar = 0

        self.startTime = time.time()
        self.lastBeatTime = self.startTime

        self.beatLength = float(60)/self.bpm

        self.sched = sched.scheduler(time.time, time.sleep)

        self.sched.enterabs(self.lastBeatTime + self.beatLength, 1, self.updateBeat, ())

    def main(self):
        while 1:
            self.sched.run()
            
    def updateBeat(self):
        if self.beat != self.beatsPerBar - 1:
            self.beat += 1
        else:
            self.beat = 0
            self.bar += 1
            if self.loopBar != self.loopBars - 1:
                self.loopBar += 1
            else:
                self.loopBar = 0
        self.lastBeatTime += self.beatLength
        self.sched.enterabs(self.lastBeatTime + self.beatLength, 1, self.updateBeat, ())

if __name__ == "__main__":
    MusicTimingComponent().run()
