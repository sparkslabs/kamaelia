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
            if self.beat != self.beatsPerBar:
                self.beat += 1
            else:
                self.beat = 1
                self.bar += 1
            self.lastBeatTime = self.lastBeatTime + self.beatLength
        self.pause(timeout = 0.0005)

    def beatPosition(self):
        return time.time() - self.lastBeatTime

    def bbfToTime(self, bars, beats, fractions):
        t = bars * self.beatsPerBar * self.beatLength
        t += beats * self.beatLength
        t += fractions * self.beatLength
        return t

    def timeToBbf(self, time):
        print "Warning: timeToBbf has not been tested yet!"
        beats = float(time * self.bpm)/60
        fractions = beats - floor(beats)
        beats = floor(beats)
        bars = floor(float(beats)/self.beatsPerBar)

