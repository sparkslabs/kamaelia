#! /usr/bin/env python
#TODO:
# * Add timing compensation
# * Rewrite header docs for new scheduler, syncing etc
# * Test timing code hard
"""
======================
Music Timing Component
======================

This component provides a scheduler and a musical "clock", which keeps time in
beats and bars.  It is designed to be subclassed for use in creating components
to be used in the creation of music.

Example usage
-------------

A simple class which prints the beat and bar every half-beat

class HalfBeatPrint(MusicTimingComponent):
    def __init__(self):
        super(HalfBeatPrint, self).__init__()
        self.lastHalfBeatTime = self.startTime
        self.halfBeatLength = self.beatLength/2
        # Use priority=2 so beat/bar rolls over first
        self.sched.enterabs(self.lastHalfBeatTime + self.halfBeatLength, 2,
                            self.printPosition, ())

    def printPosition(self):
        print "Beat: %i, Bar: %i" % (self.beat, self.bar)
        self.lastHalfBeatTime = self.lastHalfBeatTime + self.halfBeatLength
        # Reschedule the event for the next half-beat
        self.sched.enterabs(self.lastHalfBeatTime + self.halfBeatLength, 2,
                            self.printPosition, ())
   
How does it work?
-----------------

When initialized the component creates a number of variables relating to the
time.  It then creates a scheduler from python's sched module.  An event is
scheduled to call updateBeat() after a beat has passed.  updateBeat() updates
the various timing variables, and then schedules a new event to wake the
component after another beat has passed.  When subclassed the child can add
events to the scheduler allowing it to sleep until something needs doing (e.g.
a note needs playing).

Currently there is no compensation for the lack of real-time scheduling, so
events are processed slightly later than the time which is specified to the
scheduler.

"""

import time
import sched

from Axon.SchedulingComponent import SchedulingComponent

class MusicTimingComponent(SchedulingComponent):
    """
    MusicTimingComponent() -> new MusicTimingComponent component.

    A threaded component consisting of a scheduler and a number of continually
    updating variables which give the time since the component was initialized
    in music timing (bars, beats etc)
    """
    #TODO: Fill in the blanks
    Inboxes = {"inbox":"",
               "control":"",
               "event":"",
               "sync":"",
              }

    sync = False
    bpm = 120
    beatsPerBar = 4
    beatUnit = 4
    loopBars = 4

    def __init__(self, **argd):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """

        super(MusicTimingComponent, self).__init__(**argd)
        
        self.beat = 0
        self.bar = 0
        self.loopBar = 0

    def main(self):
        """
        Main loop
        """
        if self.sync:
            self.timingSync()
        else:
            self.lastBeatTime = time.time()
        self.startBeat()


        #TODO: Make me shutdown properly
        while 1:
            # Keep running events until the component is supposed to shutdown
            if self.dataReady("event"):
                if self.recv("event") == "Beat":
                    self.updateBeat()
            if self.dataReady("sync"):
                self.recv("sync")
            if not self.anyReady():
                self.pause()

    def timingSync(self):
        """
        Wait for timing data on the "sync" inbox, and update __dict__ with the
        data received.  This is a bit of a hack, but it works fine, and would 
        be a PITA to change, so we'll live with it.
        """
        while 1:
            if self.dataReady("sync"):
                timing = self.recv("sync")
                self.__dict__.update(timing)
                break
            else:
                self.pause()

    def startBeat(self): #FIXME: Better name for me?
        """
        For use after syncing.  Update the beatLength variable and schedule
        the initial beat update
        """
        self.beatLength = float(60)/self.bpm
        self.scheduleAbs("Beat", self.lastBeatTime + self.beatLength, 1)
            
    def updateBeat(self):
        """
        Progress the timing by one beat, and update the number of bars, and
        the bar position within the loop
        """
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
        # Call this function again when the next beat has passed
        self.scheduleAbs("Beat", self.lastBeatTime + self.beatLength, 1)

class SyncMaster(MusicTimingComponent):
    """
    SyncMaster([externalSync]) -> new SyncMaster component.

    A master clock providing beat and bar information for other
    MusicTimingComponents to synchronise to.  It can also synchronise to key
    timing constants from an external source.
    """

    externalSync = False
    def main(self):
        """ Main loop """
        if self.externalSync:
            # The code to generate external sync messages is currently
            # not implemented.  This bit will probably end up looking pretty
            # similar
            while 1:
                if self.dataReady("inbox"):
                    data = self.recv("inbox")
                    self.beatsPerBar, self.beatUnit, self.loopBars = data
                    break
                else:
                    self.pause()
        self.lastBeatTime = time.time()
        self.startBeat()
        while 1:
            # Keep running events until the component is supposed to shutdown
            if self.dataReady("event"):
                if self.recv("event") == "Beat":
                    self.updateBeat()
                    timingData = {"bpm" : self.bpm,
                                  "beatsPerBar" : self.beatsPerBar,
                                  "beatUnit" : self.beatUnit,
                                  "loopBars" : self.loopBars,
                                  "beat" : self.beat,
                                  "bar" : self.bar,
                                  "loopBar" : self.loopBar,
                                  "lastBeatTime" : self.lastBeatTime}
                    self.send(timingData, "outbox")
            if not self.anyReady():
                self.pause()

if __name__ == "__main__":
    MusicTimingComponent().run()
