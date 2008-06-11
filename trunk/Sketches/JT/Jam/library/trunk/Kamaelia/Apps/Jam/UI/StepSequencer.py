#!/usr/bin/env python
"""
==============
Step Sequencer
==============

A simple step sequencer component for programming rhythmic patterns such as
drum beats.
"""

import time
from Kamaelia.Apps.Jam.Util.MusicTiming import MusicTimingComponent

class StepSequencer(MusicTimingComponent):
    """
    StepSequencer() -> new StepSequencer component

    A simple step sequencer for programming rhythmic patterns such as drum
    beats
    """

    def __init__(self):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """

        super(StepSequencer, self).__init__()

        self.steps = {"1" : [1, 0, 0, 0]*self.loopBars,
                      "2" : [0, 0, 1, 0]*self.loopBars,
                      "3" : [0, 1]*2*self.loopBars}
        self.stepsPerBeat = 1
        self.nextStep = 0
        # Number of steps between the last and next active steps
        self.deltaSteps = 0

        self.stepLength = self.beatLength * self.stepsPerBeat
        self.lastStepTime = self.startTime
        
        sleepTime = self.deltaSteps * self.stepLength
        self.sched.enterabs(self.lastStepTime + sleepTime, 2, self.updateStep,
                            ())

        
    def updateStep(self):
        """
        Play the current active steps, and schedule to wake up when the next
        active step is due
        """
        self.lastStepTime += self.deltaSteps * self.stepLength
        for channel in self.steps:
            if self.steps[channel][self.nextStep] == 1:
                print "Step active", channel, self.beat
                self.send((channel, 1), "outbox")
        self.deltaSteps = self.findNextStep(self.nextStep)
        if self.deltaSteps:
            self.nextStep += self.deltaSteps
            self.nextStep %= len(self.steps.items()[0][1])
        sleepTime =  (self.deltaSteps * self.stepLength)
        self.sched.enterabs(self.lastStepTime + sleepTime, 2, self.updateStep,
                            ())


    def findNextStep(self, startingStep):
        """
        Find the position of the next step from a certain starting position.
        Returns the number of steps between the starting step and the next
        step

        Arguments:

        - startingStep -- the step to begin searching from
        """
        if startingStep != len(self.steps.items()[0][1]) - 1:
            step = startingStep + 1
        else:
            step = 0
        stepCount = 1
        while step != startingStep:
            for channel in self.steps:
                if self.steps[channel][step] == 1:
                    return stepCount
            if step != len(self.steps.items()[0][1]) - 1:
                step += 1
            else:
                step = 0
            stepCount += 1


if __name__ == "__main__":
    StepSequencer().run()
