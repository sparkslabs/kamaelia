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
import Axon

from Axon.SchedulingComponent import SchedulingComponent
from Kamaelia.UI.GraphicDisplay import PygameDisplay

from Kamaelia.Apps.Jam.Util.MusicTiming import MusicTimingComponent

class StepSequencer(MusicTimingComponent):
    """
    StepSequencer([numChannels, stepsPerBeat, position, messagePrefix,
                   size]) -> new StepSequencer component

    A simple step sequencer for programming rhythmic patterns such as drum
    beats

    Keyword arguments (all optional):
    numChannels   -- The number of channels in the step sequencer (default=4)
    stepsPerBeat  -- The number of steps for each beat in the loop.  Setting
                     this to 2 for example will allow quavers to be played
                     (default=1)
    position      -- (x,y) position of top left corner in pixels
    messagePrefix -- string to be prepended to all messages
    size          -- (w,h) in pixels (default=(500, 200))
    """

    Inboxes = {"inbox"    : "Receive events from Pygame Display",
               "remoteChanges"  : "Receive messages to alter the state of the XY pad",
               "event"    : "Scheduled events",
               "sync"     : "Timing synchronisation",
               "control"  : "For shutdown messages",
               "callback" : "Receive callbacks from Pygame Display",
              }
              
    Outboxes = {"outbox" : "XY positions emitted here",
                "localChanges" : "Messages indicating change in the state of the XY pad emitted here",
                "signal" : "For shutdown messages",
                "display_signal" : "Outbox used for communicating to the display surface"
               }
    
    numChannels = 4
    stepsPerBeat = 1
    position=None
    messagePrefix=""
    size=(500, 200)

    def __init__(self, **argd):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """

        super(StepSequencer, self).__init__(**argd)

        # Channel init
        # ------------
        self.numSteps = self.beatsPerBar * self.loopBars * self.stepsPerBeat
        self.channels = []
        for i in range(self.numChannels):
            self.channels.append([])
            for j in range(self.numSteps):
                self.channels[i].append([0, None])

        # UI Init
        # --------
        # Make the size fit the exact number of beats and channels
        self.size = (self.size[0] - self.size[0] % (self.numSteps) + 1,
                     self.size[1] - self.size[1] % len(self.channels) + 2)
        self.positionSize = ((self.size[0]/self.numSteps), 25)
        self.stepSize = (self.size[0]/self.numSteps,
                         (self.size[1]-self.positionSize[1])/len(self.channels))

        self.dispRequest = {"DISPLAYREQUEST" : True,
                            "callback" : (self,"callback"),   
                            "events" : (self, "inbox"),
                            "size": self.size,
                           }

        if self.position:
            self.dispRequest["position"] = self.position

    def addStep(self, step, channel, velocity, send=False):
        """
        Turn a step on with a given velocity and add it to the scheduler.  If
        the send argument is true then also send a message indicating the step
        has been activated to the "localChanges" outbox
        """
        self.channels[channel][step][0] = velocity
        self.scheduleStep(step, channel)
        if send:
            self.send((self.messagePrefix + "Add", (step, channel, velocity)),
                      "localChanges")

    def removeStep(self, step, channel, send=False):
        """
        Turn a step off and remove it from the scheduler.  If the send argument
        is true then also send a message indicating the step has been removed
        to the "localChanges" outbox
        """
        self.channels[channel][step][0] = 0
        self.cancelStep(step, channel)
        if send:
            self.send((self.messagePrefix + "Remove", (step, channel)),
                      "localChanges")

    def setVelocity(self, step, channel, velocity, send=False):
        """
        Change the velocity of a step.   If the send argument is true then also
        send a message indicating the velocity has changed to the
        "localChanges" outbox
        """
        self.channels[channel][step][0] = velocity
        if send:
            self.send((self.messagePrefix + "Velocity",
                       (step, channel, velocity)), "localChanges")

    ###
    # Timing Functions
    ###

    def startStep(self): # FIXME: Could maybe do with a better name?
        """
        For use after any clock synchronising.  Update the various timing
        variables, and schedule an initial step update.
        """
        self.step = (self.loopBar * self.beatsPerBar + self.beat) * self.stepsPerBeat   
        self.lastStepTime = self.lastBeatTime
        self.stepLength = self.beatLength / self.stepsPerBeat
        self.scheduleAbs("Step", self.lastStepTime + self.stepLength, 2)
 

    def updateStep(self):
        """
        Increment, and roll over if necessary, the step position counter, then
        update the position display.
        """
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
        """
        Schedule a step which has been just been activated
        """
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
        """
        Reschedule a step to occur again in a loop's time
        """
        stepTime = self.lastStepTime + self.numSteps * self.stepLength
        event = self.scheduleAbs(("StepActive", step, channel), stepTime, 3)
        self.channels[channel][step][1] = event

    def cancelStep(self, step, channel):
        """
        Delete a step event from the scheduler
        """
        self.cancelEvent(self.channels[channel][step][1])
        self.channels[channel][step][1] = None

    ###
    # UI Functions
    ###

    def drawMarkings(self):
        self.display.fill((255, 255, 255))
        pygame.draw.line(self.display, (0, 0, 0),
                         (0, 0), (self.size[0], 0))
        for i in range(self.numChannels + 1):
            pygame.draw.line(self.display, (0, 0, 0),
                             (0, self.positionSize[1] + i * self.stepSize[1]),
                             (self.size[0], self.positionSize[1] + i * self.stepSize[1]))
        for i in range(self.numSteps + 1):
            if i % (self.stepsPerBeat * self.loopBars) == 0:
                colour = (0, 0, 0)
            elif i % (self.stepsPerBeat) == 0:
                colour = (127, 127, 127)
            else:
                colour = (190, 190, 190)
            pygame.draw.line(self.display, colour,
                             (i * self.stepSize[0], 0),
                             (i * self.stepSize[0], self.size[1]))
        self.send({"REDRAW":True, "surface":self.display}, "display_signal")

    def drawStepRect(self, step, channel):
        """
        Render a single step with a colour corresponding to its velocity
        """
        position = (step * self.stepSize[0]+1, channel * self.stepSize[1] + self.positionSize[1] + 1)
        size = (self.stepSize[0] - 1, self.stepSize[1]-1)
        velocity = self.channels[channel][step][0]
        pygame.draw.rect(self.display, (255, 255*(1-velocity),
                                        255*(1-velocity)),
                         pygame.Rect(position, size))

    def drawPositionRect(self, step, active):
        """
        Render a single step in the position display, using colour if the
        position is active
        """
        position = (step * self.stepSize[0]+1, 1)
        size = (self.positionSize[0] - 1, self.positionSize[1] - 1)
        if active:
            colour = (255, 255, 0)
        else:
            colour = (255, 255, 255)
        pygame.draw.rect(self.display, colour,
                         pygame.Rect(position, size))
        self.send({"REDRAW":True, "surface":self.display}, "display_signal")

    def positionToStep(self, position):
        """
        Convert an (x, y) tuple from the mouse position to a (step, channel)
        tuple
        """
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

        self.drawMarkings()

        self.send({"ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN,
                   "surface" : self.display},
                  "display_signal")

        self.send({"ADDLISTENEVENT" : pygame.MOUSEBUTTONUP,
                   "surface" : self.display},
                  "display_signal")

        # Timing init
        # In main because timingSync needs the scheduler to be working
        if self.sync:
            self.timingSync()
        else:
            self.lastBeatTime = time.time()
        self.startBeat()
        self.startStep()

        while 1:
            if self.dataReady("inbox"):
                for event in self.recv("inbox"):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        bounds = self.display.get_rect()
                        # Don't respond to clicks in the position bar
                        bounds.top += self.positionSize[1]
                        bounds.height -= self.positionSize[1]
                        # Don't respond to clicks on the bottom or right border
                        bounds.width -= 1
                        bounds.height -= 1
                        if bounds.collidepoint(*event.pos):
                            step, channel = self.positionToStep(event.pos)
                            velocity = self.channels[channel][step][0]
                            if event.button == 1:
                                # Left click
                                if velocity > 0:
                                    # Step off
                                    self.removeStep(step, channel, True) 
                                else:
                                    # Step on
                                    self.addStep(step, channel, 0.7, True)
                            if event.button == 4:
                                # Scroll up
                                if velocity > 0 and velocity <= 0.95:
                                    velocity += 0.05
                                    self.setVelocity(step, channel, velocity,
                                                     True)
                            if event.button == 5:
                                # Scroll down
                                if velocity > 0.05:
                                    velocity -= 0.05
                                    self.setVelocity(step, channel, velocity,
                                                     True)
                            self.drawStepRect(step, channel)
                            self.send({"REDRAW":True, "surface":self.display},
                                      "display_signal")

            if self.dataReady("remoteChanges"):
                data = self.recv("remoteChanges")
                # Only the last part of an OSC address
                address = data[0].split("/")[-1]
                if address == "Add":
                    self.addStep(*data[1])
                if address == "Remove":
                    self.removeStep(*data[1])
                if address == "Velocity":
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
                    velocity = self.channels[channel][step][0]
                    self.send((self.messagePrefix + "On", (channel, velocity)),
                              "outbox")
                    self.rescheduleStep(step, channel)

            if self.dataReady("sync"):
                # Ignore any sync messages once as we have already synced by
                # now
                self.recv("sync")

            if not self.anyReady():
                self.pause()

class StepSequencerMidiConverter(Axon.Component.component):
    channel = 0
    mapping = {3:36, # Bass drum
               2:38, # Snare
               1:42, # Closed HH
               0:49} # Crash
    def main(self):
        while 1:
            if self.dataReady("inbox"):
                note, velocity = self.recv("inbox")[1]
                self.send((0x90 + self.channel, self.mapping[note],
                           int(velocity*127)), "outbox")
            if self.dataReady("control"):
                msg = self.recv("control")
                if (isinstance(msg, producerFinished) or
                   isinstance(msg, shutdownMicroprocess)):
                    self.send(msg, "signal")
                    break
            if not self.anyReady():
                self.pause()
            yield 1


if __name__ == "__main__":
    StepSequencer().run()

    #from Kamaelia.Chassis.Graphline import Graphline
    #Graphline(ss1 = StepSequencer(), ss2 = StepSequencer(position=(600, 0)),
    #         linkages={("ss1","localChanges"):("ss2", "remoteChanges")}).run()

    #from Kamaelia.Chassis.Pipeline import Pipeline
    #from Kamaelia.Apps.Jam.Protocol.Midi import Midi
    #Pipeline(StepSequencer(), StepSequencerMidiConverter(), Midi(0)).run()
