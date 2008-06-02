#!/usr/bin/env python
import time
from Kamaelia.Apps.Jam.Util.MusicTiming import MusicTimingComponent


class StepSequencer(MusicTimingComponent):
    def __init__(self):
        super(StepSequencer, self).__init__()

        self.steps = {"1" : [1, 0, 0, 0]*self.loopBars,
                      "2" : [0, 0, 1, 0]*self.loopBars,
                      "3" : [0, 1]*2*self.loopBars}
        self.stepsPerBeat = 1
        self.nextStep = 0
        self.deltaSteps = 0

        self.stepLength = self.beatLength * self.stepsPerBeat
        self.lastStepTime = self.startTime

        self.sched.enterabs(self.lastStepTime + (self.deltaSteps * self.stepLength),
                                2, self.updateStep, ())

        
    def updateStep(self):
        self.lastStepTime += self.deltaSteps * self.stepLength
        for channel in self.steps:
            if self.steps[channel][self.nextStep] == 1:
                print "Step active", channel, self.beat
                self.send((channel, 1), "outbox")
        self.deltaSteps = self.findNextStep(self.nextStep)
        if self.deltaSteps:
            self.nextStep += self.deltaSteps
            self.nextStep %= len(self.steps.items()[0][1])
        self.sched.enterabs(self.lastStepTime + (self.deltaSteps * self.stepLength),
                                2, self.updateStep, ())


    def findNextStep(self, startingStep):
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
