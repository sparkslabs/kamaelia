#!/usr/bin/env python
"""
==============
Step Sequencer
==============

A simple step sequencer component for programming rhythmic patterns such as
drum beats.
"""

import time
import pygame

from Axon.SchedulingComponent import SchedulingComponent
from Kamaelia.UI.GraphicDisplay import PygameDisplay

from Kamaelia.Apps.Jam.Util.MusicTiming import MusicTimingComponent

class StepSequencer(MusicTimingComponent):
    """
    StepSequencer() -> new StepSequencer component

    A simple step sequencer for programming rhythmic patterns such as drum
    beats
    """

    Inboxes = {"inbox"    : "Receive events from Pygame Display",
               "remoteChanges"  : "Receive messages to alter the state of the XY pad",
               "event"    : "Scheduled events",
               "control"  : "For shutdown messages",
               "callback" : "Receive callbacks from Pygame Display",
              }
              
    Outboxes = {"outbox" : "XY positions emitted here",
                "localChanges" : "Messages indicating change in the state of the XY pad emitted here",
                "signal" : "For shutdown messages",
                "display_signal" : "Outbox used for communicating to the display surface"
               }

    def __init__(self, position=None, size=(500, 200)):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """

        super(StepSequencer, self).__init__()

        # Channel and Timing Init
        # -----------------------
        self.numChannels = 4
        self.stepsPerBeat = 1
        self.numSteps = self.beatsPerBar * self.loopBars * self.stepsPerBeat
        self.channels = []
        for i in range(self.numChannels):
            self.channels.append([])
            for j in range(self.numSteps):
                self.channels[i].append([0, None])

        self.step = 0

        self.stepLength = self.beatLength * self.stepsPerBeat
        self.lastStepTime = self.startTime
        
        self.scheduleAbs("Step", self.lastStepTime + self.stepLength, 2)

        # UI Init
        # --------
        self.position = position
        # Make the size fit the exact number of beats and channels
        self.size = (size[0] - size[0] % (self.beatsPerBar * self.loopBars),
                     size[1] - size[1] % len(self.channels))
        self.positionSize = (self.size[0]/self.numSteps, 25)
        self.stepSize = (self.size[0]/self.numSteps,
                         (self.size[1]-self.positionSize[1])/len(self.channels))

        self.dispRequest = {"DISPLAYREQUEST" : True,
                            "callback" : (self,"callback"),   
                            "events" : (self, "inbox"),
                            "size": self.size,
                           }

        if position:
            self.dispRequest["position"] = position

    def addStep(self, step, channel, velocity, send=False):
        self.channels[channel][step][0] = velocity
        self.scheduleStep(step, channel)
        if send:
            self.send(("Add", (step, channel, velocity)), "localChanges")

    def removeStep(self, step, channel, send=False):
        self.channels[channel][step][0] = 0
        self.cancelStep(step, channel)
        if send:
            self.send(("Remove", (step, channel)), "localChanges")

    def setVelocity(self, step, channel, velocity, send=False):
        self.channels[channel][step][0] = velocity
        if send:
            self.send(("Velocity", (step, channel, velocity)), "localChanges")

    ###
    # Timing Functions
    ###        

    def updateStep(self):
        if self.step < self.numSteps - 1:
            self.step += 1
        else:
            self.step = 0
        self.lastStepTime += self.stepLength
        if self.step == 0:
            prevStep = self.numSteps - 1
        else:
            prevStep = self.step - 1
        self.drawPositionRect(self.step, True)
        self.drawPositionRect(prevStep, False)
        self.scheduleAbs("Step", self.lastStepTime + self.stepLength, 2)

    def scheduleStep(self, step, channel):
        # Easier if we define some stuff here
        beat = self.beat + (self.loopBar * self.beatsPerBar)
        currentStep = beat * self.stepsPerBeat
        loopStart = self.lastStepTime - (self.step * self.stepLength)
        loopLength = self.numSteps * self.stepLength

        stepTime = loopStart + (step * self.stepLength)
        if step <= currentStep:
            stepTime += loopLength
        event = self.scheduleAbs(("StepActive", step, channel), stepTime, 3)
        self.channels[channel][step][1] = event

    def rescheduleStep(self, step, channel):
        stepTime = self.lastStepTime + self.numSteps * self.stepLength
        event = self.scheduleAbs(("StepActive", step, channel), stepTime, 3)
        self.channels[channel][step][1] = event

    def cancelStep(self, step, channel):
        self.cancelEvent(self.channels[channel][step][1])
        self.channels[channel][step][1] = None

    ###
    # UI Functions
    ###

    def drawStartingRects(self):
        for i in range(len(self.channels)):
            for j in range(self.numSteps):
                self.drawStepRect(j, i)
            self.drawPositionRect(0, True)
        for i in range(self.numSteps - 1):
            self.drawPositionRect(i + 1, False)
        self.send({"REDRAW":True, "surface":self.display}, "display_signal")

    def drawStepRect(self, step, channel):
        position = (step * self.stepSize[0], channel * self.stepSize[1] + self.positionSize[1])
        velocity = self.channels[channel][step][0]
        pygame.draw.rect(self.display, (255, 255*(1-velocity),
                                        255*(1-velocity)),
                         pygame.Rect(position, self.stepSize))
        pygame.draw.rect(self.display, (0, 0, 0),
                         pygame.Rect(position, self.stepSize), 1)

    def drawPositionRect(self, step, active):
        position = (step * self.stepSize[0], 0)
        if active:
            colour = (255, 255, 0)
        else:
            colour = (255, 255, 255)
        pygame.draw.rect(self.display, colour,
                         pygame.Rect(position, self.positionSize))
        pygame.draw.rect(self.display, (0, 0, 0),
                         pygame.Rect(position, self.positionSize), 1)
        self.send({"REDRAW":True, "surface":self.display}, "display_signal")

    def positionToStep(self, position):
        step = position[0]/self.stepSize[0]
        channel = (position[1]-self.positionSize[1])/self.stepSize[1]
        return step, channel

    def main(self):
        """Main loop."""
        displayService = PygameDisplay.getDisplayService()
        self.link((self,"display_signal"), displayService)

        self.send(self.dispRequest, "display_signal")

        # Wait until we get a display
        while not self.dataReady("callback"):
            self.pause()
        self.display = self.recv("callback")

        self.drawStartingRects()

        self.send({"ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN,
                   "surface" : self.display},
                  "display_signal")

        self.send({"ADDLISTENEVENT" : pygame.MOUSEBUTTONUP,
                   "surface" : self.display},
                  "display_signal")

        while 1:
            if self.dataReady("inbox"):
                for event in self.recv("inbox"):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        bounds = self.display.get_rect()
                        # Don't respond to clicks in the position bar
                        bounds.top += self.positionSize[1]
                        bounds.height -= self.positionSize[1]
                        if bounds.collidepoint(*event.pos):
                            step, channel = self.positionToStep(event.pos)
                            velocity = self.channels[channel][step][0]
                            if event.button == 1:
                                if velocity > 0:
                                    self.removeStep(step, channel, True) 
                                else:
                                    self.addStep(step, channel, 0.7, True)
                            if event.button == 4:
                                if velocity > 0 and velocity <= 0.95:
                                    velocity += 0.05
                                    self.setVelocity(step, channel, velocity,
                                                     True)
                            if event.button == 5:
                                if velocity > 0.05:
                                    velocity -= 0.05
                                    self.setVelocity(step, channel, velocity,
                                                     True)
                            self.drawStepRect(step, channel)
                            self.send({"REDRAW":True, "surface":self.display},
                                      "display_signal")

            if self.dataReady("remoteChanges"):
                data = self.recv("remoteChanges")
                if data[0] == "Add":
                    self.addStep(*data[1])
                if data[0] == "Remove":
                    self.removeStep(*data[1])
                if data[0] == "Velocity":
                    self.setVelocity(*data[1])
                step, channel = data[1][0], data[1][1]
                self.drawStepRect(step, channel)

            if self.dataReady("event"):
                data = self.recv("event")
                if data == "Beat":
                    self.updateBeat()
                elif data == "Step":
                    self.updateStep()
                elif data[0] == "StepActive":
                    message, step, channel = data
                    self.send(("On", channel), "outbox")
                    self.rescheduleStep(step, channel)

            if not self.anyReady():
                self.pause()


if __name__ == "__main__":
    StepSequencer().run()
    #from Kamaelia.Chassis.Graphline import Graphline
    #Graphline(ss1 = StepSequencer(), ss2 = StepSequencer(position=(600, 0)),
    #         linkages={("ss1","localChanges"):("ss2", "remoteChanges")}).run()
