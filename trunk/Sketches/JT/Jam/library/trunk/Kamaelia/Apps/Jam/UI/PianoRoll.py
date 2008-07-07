#!/usr/bin/env python
"""
==============
Piano Roll
==============
"""

import time
import pygame

from Axon.SchedulingComponent import SchedulingComponent
from Kamaelia.UI.GraphicDisplay import PygameDisplay

from Kamaelia.Apps.Jam.Util.MusicTiming import MusicTimingComponent
from Kamaelia.Apps.Jam.Support.Data.Notes import noteList

class PianoRoll(MusicTimingComponent):
    """
    PianoRoll([position, messagePrefix, size]) -> new PianoRoll component


    Keyword arguments (all optional):
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
    
    notesVisible = 12
    position=None
    messagePrefix=""
    size=(500, 200)

    def __init__(self, **argd):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """

        super(PianoRoll, self).__init__(**argd)

        self.notes = []
        for i in range(len(noteList)):
            self.notes.append({})

        self.idNoteNumberMap = {}

        # Start at C5
        self.minVisibleNote = 0
        self.maxVisibleNote = self.minVisibleNote + self.notesVisible

        totalBeats = self.loopBars * self.beatsPerBar
        self.size = (self.size[0] - self.size[0] % totalBeats,
                     self.size[1] - self.size[1] % self.notesVisible)

        self.noteLength = 1

        self.barWidth = self.size[0] / self.loopBars
        self.beatWidth = self.barWidth / self.beatsPerBar

        self.noteSize = [self.beatWidth, self.size[1]/self.notesVisible]

        self.dispRequest = {"DISPLAYREQUEST" : True,
                            "callback" : (self,"callback"),   
                            "events" : (self, "inbox"),
                            "size": self.size,
                           }

        if self.position:
            self.dispRequest["position"] = self.position

    def addNote(self, beat, length, noteNumber, velocity, send=False):
        """
        Turn a step on with a given velocity and add it to the scheduler.  If
        the send argument is true then also send a message indicating the step
        has been activated to the "localChanges" outbox
        """
        note = {"beat": beat, "length" : length, "noteNumber" : noteNumber,
                "velocity" : velocity}
        noteId = id(note)
        self.notes[noteNumber][noteId] = note
        self.idNoteNumberMap[noteId] = noteNumber
        self.scheduleNote(noteId)
        if send:
            self.send((self.messagePrefix + "Add", (beat, length,
                                                    noteNumber, velocity)
                      ), "localChanges")

    def removeNote(self, step, channel, send=False):
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

    def getNote(self, noteId):
        noteNumber = self.idNoteNumberMap[noteId]
        return self.notes[noteNumber][noteId]

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

    def moveNote(self):
        pass

    def resizeNote(self):
        pass

    ###
    # Timing Functions
    ###
# Don't think we'll need an equivalent to this stuff
#    def startStep(self): # FIXME: Could maybe do with a better name?
#        """
#        For use after any clock synchronising.  Update the various timing
#        variables, and schedule an initial step update.
#        """
#        self.step = (self.loopBar * self.beatsPerBar + self.beat) * self.stepsPerBeat   
#        self.lastStepTime = self.lastBeatTime
#        self.stepLength = self.beatLength / self.stepsPerBeat
#        self.scheduleAbs("Step", self.lastStepTime + self.stepLength, 2)
# 
#
#    def updateStep(self):
#        """
#        Increment, and roll over if necessary, the step position counter, then
#        update the position display.
#        """
#        if self.step < self.numSteps - 1:
#            self.step += 1
#        else:
#            self.step = 0
#        self.lastStepTime += self.stepLength
#        if self.step == 0:
#            prevStep = self.numSteps - 1
#        else:
#            prevStep = self.step - 1
#        self.drawPositionRect(self.step, True)
#        self.drawPositionRect(prevStep, False)
#        self.scheduleAbs("Step", self.lastStepTime + self.stepLength, 2)

    def scheduleNote(self, noteId):
        """
        Schedule a step which has been just been activated
        """
        note = self.getNote(noteId)
        # Easier if we define some stuff here
        currentBeat = self.beat + (self.loopBar * self.beatsPerBar)
        loopStart = self.lastBeatTime - (currentBeat * self.beatLength)
        loopLength = self.loopBars * self.beatsPerBar * self.beatLength

        noteTime = loopStart + (note["beat"] * self.beatLength)
        if note["beat"] <= currentBeat:
            noteTime += loopLength
        event = self.scheduleAbs(("NoteActive", noteId), noteTime, 3)
        note["event"] = event

    def rescheduleNote(self, step, channel):
        """
        Reschedule a step to occur again in a loop's time
        """
        stepTime = self.lastStepTime + self.numSteps * self.stepLength
        event = self.scheduleAbs(("StepActive", step, channel), stepTime, 3)
        self.channels[channel][step][1] = event

    def cancelNote(self, step, channel):
        """
        Delete a step event from the scheduler
        """
        self.cancelEvent(self.channels[channel][step][1])
        self.channels[channel][step][1] = None

    ###
    # UI Functions
    ###

    def drawMarkings(self):
        """
        Initial render of all of the blank steps
        """
        self.display.fill((255, 255, 255))
        for i in range(self.notesVisible - 1):
            pygame.draw.line(self.display, (0, 0, 0),
                             (0, (i + 1) * self.noteSize[1]),
                             (self.size[0], (i + 1) * self.noteSize[1]))

    def drawNoteRect(self, noteId):
        """
        Render a single step with a colour corresponding to its velocity
        """
        note = self.getNote(noteId)
        yPos = self.size[1] - (note["noteNumber"] - self.minVisibleNote) * self.noteSize[1]
        position = (note["beat"] * self.beatWidth, yPos)
        size = (note["length"] * self.beatWidth, self.noteSize[1])
        pygame.draw.rect(self.display, (255, 255*(1-note["velocity"]),
                                        255*(1-note["velocity"])),
                         pygame.Rect(position, size))

    def render(self):
        self.drawMarkings()
        visibleNotes = self.notes[self.minVisibleNote:self.maxVisibleNote + 1]
        
        for noteId in sum([x.keys() for x in visibleNotes], []):
            self.drawNoteRect(noteId)
        self.send({"REDRAW":True, "surface":self.display}, "display_signal")

    def positionToNote(self, position):
        """
        Convert an (x, y) tuple from the mouse position to a (step, channel)
        tuple
        """
        noteNumber = self.notesVisible - int(self.notesVisible * float(position[1]) / self.size[1]) + self.minVisibleNote
        beat = float(position[0]) / self.beatWidth
        return (beat, noteNumber)

    def getNoteIds(self, beat, noteNumber):
        # TODO: Optimise me
        ids = []
        for noteId in self.notes[noteNumber]:
            note = self.notes[noteNumber][noteId]
            # TODO: Clean me up - this is pretty *ewww*.  Maybe should be a 
            #       seperate function?
            if beat >= note["beat"] and beat <= note["beat"] + note["length"]:
                ids.append(noteId)
        return ids

    def main(self):
        """Main loop."""
        displayService = PygameDisplay.getDisplayService()
        self.link((self,"display_signal"), displayService)

        self.send(self.dispRequest, "display_signal")

        # Wait until we get a display
        while not self.dataReady("callback"):
            self.pause()
        self.display = self.recv("callback")

        # Initial render
        self.render()

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
#        self.startStep()

        while 1:
            if self.dataReady("inbox"):
                for event in self.recv("inbox"):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        bounds = self.display.get_rect()
                        if bounds.collidepoint(*event.pos):
                            beat, noteNumber = self.positionToNote(event.pos)
                            ids = self.getNoteIds(beat, noteNumber)
                            if event.button == 1:
                                # Left click
                                if ids:
                                    pass
                                    # Note off
                                    # self.removeNote(id)
                                else:
                                    # Step on
                                    self.addNote(beat, self.noteLength,
                                                 noteNumber, 0.7, True)
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
                            self.render()

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
                    velocity = self.channels[channel][step]
                    self.send((self.messagePrefix + "On", (channel, velocity)),
                              "outbox")
                    self.rescheduleStep(step, channel)

            if self.dataReady("sync"):
                # Ignore any sync messages once as we have already synced by
                # now
                self.recv("sync")

            if not self.anyReady():
                self.pause()


if __name__ == "__main__":
    PianoRoll().run()
    #from Kamaelia.Chassis.Graphline import Graphline
    #Graphline(ss1 = StepSequencer(), ss2 = StepSequencer(position=(600, 0)),
    #         linkages={("ss1","localChanges"):("ss2", "remoteChanges")}).run()
