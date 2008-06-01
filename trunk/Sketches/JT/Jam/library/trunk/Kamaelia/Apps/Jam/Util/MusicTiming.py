#! /usr/bin/env python
#TODO:
# * Document me
# * Test timing code hard
import time

from math import floor
from Axon.ThreadedComponent import threadedcomponent

class MusicTimingComponent(threadedcomponent):
    def __init__(self, bpm=120, beatsPerBar=4, beatUnit=4):
        super(MusicTimingComponent, self).__init__()
        self.bpm = bpm
        self.beatsPerBar = beatsPerBar
        self.beatUnit = beatUnit

        self.playing = 1
        self.beat = 1
        self.bar = 1

        self.lastBeatTime = time.time()

        self.beatLength = float(60)/self.bpm

    def updateTiming(self):
        t = time.time()
        if t >= self.lastBeatTime + self.beatLength:
            # Debug - print the delay between updating the beat and the actual
            # beat time.  ~3ms on eli (P4 3GHz) - would be nice if this was
            # lower
            # print t - (self.lastBeatTime + self.beatLength)
            if self.beat != self.beatsPerBar:
                self.beat += 1
            else:
                self.beat = 1
                self.bar += 1
            self.lastBeatTime = self.lastBeatTime + self.beatLength
        time.sleep(0.0005)


