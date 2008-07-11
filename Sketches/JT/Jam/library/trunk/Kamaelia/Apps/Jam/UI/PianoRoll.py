#!/usr/bin/env python
"""
==============
Piano Roll
==============
"""

import time
import pygame
import operator
import uuid

from Axon.SchedulingComponent import SchedulingComponent
from Axon.Ipc import producerFinished
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

        self.notes = {}
        self.notesByNumber = []
        for i in range(len(noteList)):
            self.notesByNumber.append([])

        # Start at C5
        self.minVisibleNote = 0
        self.maxVisibleNote = self.minVisibleNote + self.notesVisible

        totalBeats = self.loopBars * self.beatsPerBar
        # Make size fit to an exact number of beats and notes
        # Add 1 for the border
        self.size = (self.size[0] - (self.size[0] % totalBeats) + 1,
                     self.size[1] - (self.size[1] % self.notesVisible) + 1)

        self.noteLength = 1

        self.barWidth = self.size[0] / self.loopBars
        self.beatWidth = self.barWidth / self.beatsPerBar

        self.noteSize = [self.beatWidth, self.size[1]/self.notesVisible]

        self.tabWidth = 5

        self.resizing = False
        self.moving = False

    def addNote(self, beat, length, noteNumber, velocity, send=False):
        """
        Turn a step on with a given velocity and add it to the scheduler.  If
        the send argument is true then also send a message indicating the step
        has been activated to the "localChanges" outbox
        """
        note = {"beat": beat, "length" : length, "noteNumber" : noteNumber,
                "velocity" : velocity, "surface" : None}
        # Making a UUID may be overkill, but better safe than sorry
        noteId = uuid.uuid4()
        #print "Adding note - id =", noteId
        self.notes[noteId] = note
        self.notesByNumber[noteNumber].append(noteId)
        self.scheduleNote(noteId)
        if send:
            self.send((self.messagePrefix + "Add", (beat, length,
                                                    noteNumber, velocity)
                      ), "localChanges")
        return noteId

    def removeNote(self, noteId, send=False):
        """
        Turn a step off and remove it from the scheduler.  If the send argument
        is true then also send a message indicating the step has been removed
        to the "localChanges" outbox
        """
        #print "Removing note - id =", noteId
        self.cancelNote(noteId)
        noteNumber = self.notes[noteId]["noteNumber"]
        del self.notes[noteId]
        self.notesByNumber[noteNumber].remove(noteId)
        if send:
            # TODO: Make me send sensible stuff
            self.send((self.messagePrefix + "Remove", 1),
                      "localChanges")

    def setVelocity(self, noteId, velocity, send=False):
        """
        Change the velocity of a step.   If the send argument is true then also
        send a message indicating the velocity has changed to the
        "localChanges" outbox
        """
        self.notes[noteId]["velocity"] = velocity
        if send:
            # TODO: Make me send sensible stuff
            self.send((self.messagePrefix + "Velocity",
                       velocity), "localChanges")

    def moveNote(self, noteId, beat, send=False):
        self.notes[noteId]["beat"] = beat
        if send:
            self.send((self.messagePrefix + "Move",
                       length), "localChanges")

    def resizeNote(self, noteId, length, send=False):
        self.notes[noteId]["length"] = length
        if send:
            self.send((self.messagePrefix + "Resize",
                       length), "localChanges")

    ###
    # Timing Functions
    ###
    def scheduleNote(self, noteId):
        """
        Schedule a step which has been just been activated
        """
        note = self.notes[noteId]
        # Easier if we define some stuff here
        currentBeat = self.beat + (self.loopBar * self.beatsPerBar)
        loopStart = self.lastBeatTime - (currentBeat * self.beatLength)
        loopLength = self.loopBars * self.beatsPerBar * self.beatLength

        noteTime = loopStart + (note["beat"] * self.beatLength)
        # Fraction
        beatFraction = (time.time() - self.lastBeatTime)/self.beatLength
        if note["beat"] <= currentBeat + beatFraction:
            noteTime += loopLength
        #print "Scheduling note for", noteTime - time.time()
        event = self.scheduleAbs(("NoteActive", noteId), noteTime, 3)
        note["event"] = event

    def cancelNote(self, noteId):
        """
        Delete a step event from the scheduler
        """
        note = self.notes[noteId]
        self.cancelEvent(note["event"])

    ###
    # UI Functions
    ###

    def createSurface(self, displayRequest):
        self.send(displayRequest, "display_signal")
        while not self.dataReady("callback"):
            self.pause()
        display = self.recv("callback")
        return display

    def requestRedraw(self):
        self.send({"REDRAW":True, "surface":self.display}, "display_signal")

    def drawMarkings(self):
        """
        Initial render of all of the blank steps
        """
        self.background.fill((255, 255, 255))
        for i in range(self.notesVisible + 1):
            pygame.draw.line(self.background, (127, 127, 127),
                             (0, i * self.noteSize[1]),
                             (self.size[0], i * self.noteSize[1]))
        for i in range(self.loopBars + 1):
            xPos = i * self.barWidth
            for i in range(self.beatsPerBar):
                pygame.draw.line(self.background, (127, 127, 127),
                                 (xPos + i * self.beatWidth, 0),
                                 (xPos + i * self.beatWidth, self.size[1]))
            pygame.draw.line(self.background, (0, 0, 0), (xPos, 0),
                             (xPos, self.size[1]))
                

    def drawNoteRect(self, noteId):
        """
        Render a single step with a colour corresponding to its velocity
        """
        if not self.notes[noteId]["surface"]:
            # We don't have a surface for the note yet, so make a new one                
            # The number of notes from this note to the bottom
            notesUp = self.notes[noteId]["noteNumber"] - self.minVisibleNote
            position = (self.notes[noteId]["beat"] * self.beatWidth,
                        self.size[1] - notesUp * self.noteSize[1])
            size = (self.notes[noteId]["length"] * self.beatWidth,
                    self.noteSize[1])

            displayRequest = {"DISPLAYREQUEST" : True,
                              "size" : size,
                              "position" : position,
                              "callback" : (self, "callback")}

            surface = self.createSurface(displayRequest)
        else:
            surface = self.notes[noteId]["surface"]

        surface.fill((0, 0, 0))
        
        # Adjust for a border
        size = (size[0] - (2 + self.tabWidth), size[1] - 2)

        surface.fill((255, 0, 0), pygame.Rect((1, 1), size))
        velocity = self.notes[noteId]["velocity"]
        surface.set_alpha(255 * velocity)
        self.notes[noteId]["surface"] = surface

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
        for noteId in self.notesByNumber[noteNumber]:
            note = self.notes[noteId]
            # TODO: Clean me up - this is pretty *ewww*.  Maybe should be a 
            #       seperate function?
            if beat >= note["beat"] and beat <= note["beat"] + note["length"]:
                ids.append(noteId)
        return ids

    def main(self):
        """Main loop."""
        displayService = PygameDisplay.getDisplayService()
        self.link((self,"display_signal"), displayService)

        # Display surface - this is what we call to redraw
        displayRequest = {"DISPLAYREQUEST" : True,
                          "callback" : (self,"callback"),
                          "events" : (self, "inbox"),
                          "size" : self.size,
                          "position" : (0, 0)
                         }
        if self.position:
            displayRequest["position"] = self.position
        self.display = self.createSurface(displayRequest)

        self.send({"ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN,
                   "surface" : self.display},
                  "display_signal")

        self.send({"ADDLISTENEVENT" : pygame.MOUSEBUTTONUP,
                   "surface" : self.display},
                  "display_signal")
        
        # Background surface - this is what we draw the background markings onto
        displayRequest = {"DISPLAYREQUEST" : True,
                          "callback" : (self,"callback"),
                          "size": self.size,
                          "position" : (0, 0)
                         }
        self.background = self.createSurface(displayRequest)

        # Initial render
        self.drawMarkings()
        self.requestRedraw()

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
                            if ids:
                                # We have clicked on one or more notes
                                notes = [self.notes[noteId] for noteId in ids]
                                # Use the earliest note
                                # FIXME: A little ugly maybe?  Short though...
                                note = min(notes,
                                           key=operator.itemgetter("beat"))
                                noteId = ids[notes.index(note)]
                                surface = self.notes[noteId]["surface"]
                                velocity = self.notes[noteId]["velocity"]
                                if event.button == 1:
                                    # Left click - Move or resize
                                    # Number of beats between the click and the
                                    # start and end of the note
                                    toEnd = note["beat"] + note["length"] - beat
                                    if toEnd < float(self.tabWidth) / self.beatWidth:
                                        # Resize
                                        self.resizing = (noteId, event.pos[0])
                                    else:
                                        # Move
                                        self.moving = (noteId, event.pos[0])

                                if event.button == 3:
                                    # Right click - Note off
                                    self.send(producerFinished(message=surface),
                                              "display_signal")
                                    self.removeNote(noteId)

                                if event.button == 4:
                                    # Scroll up - Velocity up
                                    if velocity > 0 and velocity <= 0.95:
                                        velocity += 0.05
                                        self.setVelocity(noteId, velocity,
                                                         True)
                                        surface.set_alpha(255 * velocity)

                                if event.button == 5:
                                    # Scroll down - Velocity down
                                    if velocity > 0.05:
                                        velocity -= 0.05
                                        self.setVelocity(noteId, velocity,
                                                         True)
                                        surface.set_alpha(255 * velocity)
                            else:
                                if event.button == 1:
                                    # Left click - Note on
                                    noteId = self.addNote(beat, self.noteLength,
                                                          noteNumber, 0.7, True)
                                    self.drawNoteRect(noteId)
                            self.requestRedraw()

                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            if self.moving:
                                noteId, startPos = self.moving

                                beat = self.notes[noteId]["beat"]
                                length = self.notes[noteId]["length"]
                                numBeats = self.beatsPerBar * self.loopBars

                                deltaPos = float(event.pos[0] - startPos)
                                deltaPos /= self.beatWidth

                                beat += deltaPos

                                if beat + length > numBeats:
                                    beat = numBeats - length
                                if beat < 0:
                                    beat = 0
                                self.moveNote(noteId, beat)
                                # Delete the note rect and recreate it
                                surface = self.notes[noteId]["surface"]
                                self.send(producerFinished(message=surface),
                                          "display_signal")
                                self.notes[noteId]["surface"] = None
                                self.drawNoteRect(noteId)
                                self.moving = False

                            if self.resizing:
                                noteId, startPos = self.resizing

                                beat = self.notes[noteId]["beat"]
                                length = self.notes[noteId]["length"]
                                numBeats = self.beatsPerBar * self.loopBars

                                deltaLength = float(event.pos[0] - startPos)
                                deltaLength /= self.beatWidth

                                length += deltaLength

                                if beat + length > numBeats:
                                    length = numBeats - beat
                                self.resizeNote(noteId, length)
                                # Delete the note rect and recreate it
                                surface = self.notes[noteId]["surface"]
                                self.send(producerFinished(message=surface),
                                          "display_signal")
                                self.notes[noteId]["surface"] = None
                                self.drawNoteRect(noteId)
                                self.resizing = False
                            self.requestRedraw()

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
                elif data[0] == "NoteActive":
                    noteId = data[1]
                    note = self.notes[noteId]
                    freq = noteList[note["noteNumber"]]["freq"]
                    velocity = note["velocity"]
                    self.send((self.messagePrefix + "On", (freq, velocity)),
                              "outbox")
                    self.scheduleNote(noteId)

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
