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

from Axon.Component import component
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
    sendNoteNumber = False

    def __init__(self, **argd):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """

        super(PianoRoll, self).__init__(**argd)

        # Dict relating a uuid to all of the information in a note
        self.notes = {}
        # 2D list relating a note numbers to the ids of notes with that number
        self.notesByNumber = []
        for i in range(len(noteList)):
            self.notesByNumber.append([])

        # Start at C5
        self.minVisibleNote = 60
        self.maxVisibleNote = self.minVisibleNote + self.notesVisible - 1

        totalBeats = self.loopBars * self.beatsPerBar
        # Make size fit to an exact number of beats and notes
        # Add 1 for the border
        self.size = (self.size[0] - (self.size[0] % totalBeats) + 1,
                     self.size[1] - (self.size[1] % self.notesVisible) + 1)

        # The length in beats to use when a new note is added
        self.noteLength = 1

        self.barWidth = self.size[0] / self.loopBars
        self.beatWidth = self.barWidth / self.beatsPerBar

        self.noteSize = [self.beatWidth, self.size[1]/self.notesVisible]

        # The width in px of the resize tab
        self.tabWidth = 5

        self.resizing = False
        self.moving = False
        self.scrolling = 0
        self.scrollEvent = None

        self.resizeCount = 0
    
        pygame.font.init()
        self.font = pygame.font.Font(None, 14)

    def addNote(self, beat, length, noteNumber, velocity, noteId=None,
                send=False):
        """
        Add a note with a position, note number and velocity to the scheduler.
        If the send argument is true then also send a message indicating the
        note has been added to the "localChanges" outbox
        """
        note = {"beat": beat, "length" : length, "noteNumber" : noteNumber,
                "velocity" : velocity, "surface" : None, "playing" : False}
        # Making a UUID may be overkill, but better safe than sorry
        if not noteId:
            noteId = str(uuid.uuid4())
        #print "Adding note - id =", noteId
        self.notes[noteId] = note
        self.notesByNumber[noteNumber].append(noteId)
        self.scheduleNoteOn(noteId)
        self.scheduleNoteOff(noteId)
        if send:
            self.send((self.messagePrefix + "Add", (noteId, beat, length,
                                                    noteNumber, velocity)),
                      "localChanges")
        return noteId

    def removeNote(self, noteId, send=False):
        """
        Remove a note with a known id from the scheduler.  If the send argument
        is true then also send a message indicating the note has been removed
        to the "localChanges" outbox
        """
        #print "Removing note - id =", noteId
        # Turn the note off if it's playing
        if self.notes[noteId]["playing"] == True:
            self.sendNoteOff(noteId)
        # Remove it from the scheduler
        self.cancelNote(noteId)
        # Remove it from the notes dict and list
        noteNumber = self.notes[noteId]["noteNumber"]
        del self.notes[noteId]
        self.notesByNumber[noteNumber].remove(noteId)
        if send:
            self.send((self.messagePrefix + "Remove", noteId),
                      "localChanges")

    def setVelocity(self, noteId, velocity, send=False):
        """
        Change the velocity of a note.   If the send argument is true then also
        send a message indicating the velocity has changed to the
        "localChanges" outbox
        """
        self.notes[noteId]["velocity"] = velocity
        if send:
            # TODO: Make me send sensible stuff
            self.send((self.messagePrefix + "Velocity",
                       (noteId, velocity)), "localChanges")

    def moveNote(self, noteId, send=False):
        """
        Change the start time of a note in the scheduler.  This is done by
        simply rescheduling the note on and off events.  If the send argument
        is true then also send a message indicating the note has been moved to
        the "localChanges" outbox
        """
        self.scheduleNoteOn(noteId)
        self.scheduleNoteOff(noteId)
        if send:
            beat = self.notes[noteId]["beat"]
            noteNumber = self.notes[noteId]["noteNumber"]
            self.send((self.messagePrefix + "Move",
                       (noteId, beat, noteNumber)), "localChanges")

    def resizeNote(self, noteId, send=False):
        """
        Change the length of a note in the scheduler.  This is done by
        simply rescheduling the note on and off events.  If the send argument
        is true then also send a message indicating the note has been resized
        to the "localChanges" outbox
        """
        self.scheduleNoteOn(noteId)
        self.scheduleNoteOff(noteId)
        if send:
            length = self.notes[noteId]["length"]
            self.send((self.messagePrefix + "Resize",
                       (noteId, length)), "localChanges")

    def setNoteNumber(self, noteId, noteNumber):
        """
        Change the note number of a note, and keep the references to it
        consistent in the notesByNumber list
        """
        oldNoteNumber = self.notes[noteId]["noteNumber"]
        self.notesByNumber[oldNoteNumber].remove(noteId)
        self.notesByNumber[noteNumber].append(noteId)
        self.notes[noteId]["noteNumber"] = noteNumber

    def sendNoteOn(self, noteId):
        """
        Send a message indication that a note needs to be played to the
        "outbox" outbox
        """
        self.notes[noteId]["playing"] = True
        noteNumber = self.notes[noteId]["noteNumber"]
        velocity = self.notes[noteId]["velocity"]
        if not self.sendNoteNumber:
            freq = noteList[noteNumber]["freq"]
            #print "Note On", freq, velocity
            self.send((self.messagePrefix + "On", (freq, velocity)),
                      "outbox")
        else:
            #print "Note On", noteNumber+1, velocity
            # Use noteNumber + 1 because we are using a zero-index, where
            # MIDI is 1-indexed
            self.send((self.messagePrefix + "On", (noteNumber + 1, velocity)),
                      "outbox")

    def sendNoteOff(self, noteId):
        """
        Send a message indicating that a note needs to stop playing to the
        "outbox" outbox
        """
        self.notes[noteId]["playing"] = False
        noteNumber = self.notes[noteId]["noteNumber"]
        freq = noteList[noteNumber]["freq"]
        #print "Note Off", freq
        self.send((self.messagePrefix + "Off", freq),
                  "outbox")

    ###
    # Timing Functions
    ###
    def scheduleNoteOn(self, noteId):
        """
        Schedule a step which has been just been activated
        """
        note = self.notes[noteId]
        # Easier if we define some stuff here
        currentBeat = self.beat + (self.loopBar * self.beatsPerBar)
        loopStart = self.lastBeatTime - (currentBeat * self.beatLength)
        loopLength = self.loopBars * self.beatsPerBar * self.beatLength

        noteOnTime = loopStart + (note["beat"] * self.beatLength)
        # Fraction through the current beat
        beatFraction = (time.time() - self.lastBeatTime)/self.beatLength
        # If we are scheduling a note behind the current playback position then
        # make sure it's scheduled for the next loop round
        if note["beat"] <= currentBeat + beatFraction:
            noteOnTime += loopLength
        #print "Scheduling note for", noteOnTime - time.time()
        event = self.scheduleAbs(("NoteOn", noteId), noteOnTime, 3)
        note["onEvent"] = event

    def scheduleNoteOff(self, noteId):
        # SMELL: Duplication of scheduleNoteOn is pretty ugly
        note = self.notes[noteId]
        # Easier if we define some stuff here
        currentBeat = self.beat + (self.loopBar * self.beatsPerBar)
        loopStart = self.lastBeatTime - (currentBeat * self.beatLength)
        loopLength = self.loopBars * self.beatsPerBar * self.beatLength

        noteOnTime = loopStart + (note["beat"] * self.beatLength)
        # Fraction through the current beat
        beatFraction = (time.time() - self.lastBeatTime)/self.beatLength
        # If we are scheduling a note behind the current playback position then
        # make sure it's scheduled for the next loop round
        if note["beat"] <= currentBeat + beatFraction:
            noteOnTime += loopLength
        noteOffTime = noteOnTime + note["length"] * self.beatLength

        event = self.scheduleAbs(("NoteOff", noteId), noteOffTime, 3)
        note["offEvent"] = event


    def cancelNote(self, noteId):
        """
        Delete a note's events from the scheduler
        """
        note = self.notes[noteId]
        self.cancelEvent(note["onEvent"])
        self.cancelEvent(note["offEvent"])

    ###
    # UI Functions
    ###

    def createSurface(self, displayRequest):
        """
        Request a new pygame surface, and wait for it to arrive
        """
        self.send(displayRequest, "display_signal")
        while not self.dataReady("callback"):
            self.pause()
        display = self.recv("callback")
        return display

    def addListenEvent(self, eventType):
        """
        Start listening to a certain type of event from the pygame display
        """
        self.send({"ADDLISTENEVENT" : eventType,
                   "surface" : self.display},
                  "display_signal")
       
    def removeListenEvent(self, eventType):
        """
        Stop listening to a certain type of event from the pygame display
        """
        self.send({"REMOVELISTENEVENT" : eventType,
                   "surface" : self.display},
                  "display_signal")

    def requestRedraw(self):
        """
        Request a complete redraw of the pygame display
        """
        self.send({"REDRAW":True, "surface":self.display}, "display_signal")

    def drawMarkings(self):
        """
        Draw the background beat markings and sharp/flat shading
        """
        self.background.fill((255, 255, 255))
        for i in range(self.notesVisible):
            noteName = noteList[self.maxVisibleNote - i]["name"]
            octave = noteList[self.maxVisibleNote - i]["octave"]
            # Draw shaded rects for the note backgrounds
            if noteName[-1] == "#":
                # Sharp note, so shade it darker
                colour = (224, 224, 224)
            else:
                colour = (255, 255, 255)
            pygame.draw.rect(self.background, colour,
                             pygame.Rect((0, i * self.noteSize[1]),
                                         (self.size[0], self.noteSize[1])))
            # Draw lines to make the note boundaries clearer
            pygame.draw.line(self.background, (127, 127, 127),
                             (0, i * self.noteSize[1]),
                             (self.size[0], i * self.noteSize[1]))
            # Write note name to the left of the note
            surface = self.font.render(noteName + str(octave), True, (0, 0, 0))
            self.background.blit(surface, (5, i * self.noteSize[1]))
        
        for i in range(self.loopBars + 1):
            xPos = i * self.barWidth
            for i in range(self.beatsPerBar):
                # Draw light lines for beat boundaries
                pygame.draw.line(self.background, (127, 127, 127),
                                 (xPos + i * self.beatWidth, 0),
                                 (xPos + i * self.beatWidth, self.size[1]))
            # Draw dark lines for bar boundaries
            pygame.draw.line(self.background, (0, 0, 0), (xPos, 0),
                             (xPos, self.size[1]))
                

    def drawNoteRect(self, noteId):
        """
        Render a note onto a new surface with transparency corresponding to
        its velocity
        """
        # The number of notes from this note to the bottom
        notesUp = self.notes[noteId]["noteNumber"] - self.minVisibleNote
        position = (self.notes[noteId]["beat"] * self.beatWidth,
                    self.size[1] - (notesUp + 1) * self.noteSize[1])
        # Adjust surface position for the position of the Piano Roll
        if self.position:
            position = (position[0] + self.position[0],
                        position[1] + self.position[1])
        size = (self.notes[noteId]["length"] * self.beatWidth,
                self.noteSize[1])

        displayRequest = {"DISPLAYREQUEST" : True,
                          "size" : size,
                          "position" : position,
                          "callback" : (self, "callback")}
        surface = self.createSurface(displayRequest)
        
        # Fill the whole rect black
        surface.fill((0, 0, 0))
        # Adjust the size to for a border
        size = (size[0] - (2 + self.tabWidth), size[1] - 2)
        # Fill the inner rect red
        surface.fill((255, 0, 0), pygame.Rect((1, 1), size))
        # Make the surface transparent depending on its velocity
        velocity = self.notes[noteId]["velocity"]
        surface.set_alpha(255 * velocity)
        self.notes[noteId]["surface"] = surface

    def deleteNoteRect(self, noteId):
        """
        Remove a note surface from the display
        """
        surface = self.notes[noteId]["surface"]
        self.send(producerFinished(message=surface),
                  "display_signal")
        self.notes[noteId]["surface"] = None

    def redrawNoteRect(self, noteId):
        """
        Delete and subsequently redraw a note surface.  Note that for just
        moving a note this is slower than using the moveNoteRect method, and
        should only be used when the surface needs to be resized.
        """
        self.deleteNoteRect(noteId)
        self.drawNoteRect(noteId)

    def moveNoteRect(self, noteId):
        """ Move a note surface to a different position """
        # The number of notes from this note to the bottom
        notesUp = self.notes[noteId]["noteNumber"] - self.minVisibleNote
        position = (self.notes[noteId]["beat"] * self.beatWidth,
                    self.size[1] - (notesUp + 1) * self.noteSize[1])
        # Adjust surface position for the position of the Piano Roll
        if self.position:
            position = (position[0] + self.position[0],
                        position[1] + self.position[1])
        self.send({"CHANGEDISPLAYGEO" : True,
                   "surface" : self.notes[noteId]["surface"],
                   "position" : position},
                  "display_signal")

    def scrollUp(self):
        """
        Scroll the piano roll up by one note
        """
        self.minVisibleNote += 1
        self.maxVisibleNote += 1
        self.drawMarkings()
        # Delete any note rects which will be off screen
        for noteId in self.notesByNumber[self.minVisibleNote - 1]:
            self.deleteNoteRect(noteId)
        # Move any note rects which will still be on screen
        notes = self.notesByNumber[self.minVisibleNote:self.maxVisibleNote - 1]
        for noteId in sum(notes, []):
            self.moveNoteRect(noteId)
        # Add any note rects which have come on screen
        for noteId in self.notesByNumber[self.maxVisibleNote]: 
            self.drawNoteRect(noteId)

    def scrollDown(self):
        """
        Scroll the piano roll down by one note
        """
        self.minVisibleNote -= 1
        self.maxVisibleNote -= 1
        self.drawMarkings()
        # Delete any note rects which will be off screen
        for noteId in self.notesByNumber[self.maxVisibleNote + 1]:
            self.deleteNoteRect(noteId)
        # Move any note rects which will still be on screen
        notes = self.notesByNumber[self.minVisibleNote + 1:self.maxVisibleNote]
        for noteId in sum(notes, []):
            self.moveNoteRect(noteId)
        # Add any note rects which have come on screen
        for noteId in self.notesByNumber[self.minVisibleNote]:
            self.drawNoteRect(noteId)

    def noteIsVisible(self, noteId):
        """
        Returns whether the note is within the range of visible notes
        """
        noteNumber = self.notes[noteId]["noteNumber"]
        return (noteNumber <= self.maxVisibleNote and
                noteNumber >= self.minVisibleNote)

    def positionToNote(self, position):
        """
        Convert an (x, y) tuple from the mouse position to a (beat, noteNumber)
        tuple
        """
        # Number of notes from the top of the piano roll
        notesDown = int(self.notesVisible * float(position[1]) / self.size[1])
        noteNumber = self.minVisibleNote + self.notesVisible - notesDown - 1
        beat = float(position[0]) / self.beatWidth
        return (beat, noteNumber)

    def noteToPosition(self, noteId):
        """
        Convert a (beat, noteNumber) tuple into an (x, y) tuple
        """
        note = self.notes[noteId]
        xPos = note["beat"] * self.beatWidth
        yPos = (self.maxVisibleNote - note["noteNumber"]) * self.noteSize[1]
        return (xPos, yPos)

    def getNoteIds(self, beat, noteNumber):
        """
        Return a list of notes with a certain note number which contain the
        beat position provided
        """
        ids = []
        for noteId in self.notesByNumber[noteNumber]:
            note = self.notes[noteId]
            if beat >= note["beat"] and beat <= note["beat"] + note["length"]:
                ids.append(noteId)
        return ids

    def handleMouseDown(self, event):
        """
        Handle mouse down events from the pygame display
        """
        beat, noteNumber = self.positionToNote(event.pos)
        ids = self.getNoteIds(beat, noteNumber)
        if ids:
            # We have clicked on one or more notes
            notes = [self.notes[noteId] for noteId in ids]
            # Use the earliest note
            # FIXME: A little ugly maybe?  Short though...
            note = min(notes, key=operator.itemgetter("beat"))
            noteId = ids[notes.index(note)]
            surface = self.notes[noteId]["surface"]
            velocity = self.notes[noteId]["velocity"]

            if event.button == 1:
                # Left click - Move or resize
                # Stop the note playing before moving or resizing, so we
                # don't leave notes hanging
                if self.notes[noteId]["playing"]:
                    self.sendNoteOff(noteId)
                self.cancelNote(noteId)

                # Number of beats between the click position and the end of
                # the note
                toEnd = note["beat"] + note["length"] - beat
                notePos = self.noteToPosition(noteId)
                deltaPos = []
                for i in xrange(2):
                    deltaPos.append(event.pos[i] - notePos[i])

                if toEnd < float(self.tabWidth) / self.beatWidth:
                    # We have clicked in the tab
                    # Resize
                    # SMELL: Should really be boolean
                    self.resizing = (noteId, deltaPos)
                    self.resizeCount = 0
                else:
                    # We have clicked in the main bit
                    # Move
                    # SMELL: Should really be boolean
                    self.moving = (noteId, deltaPos)
                ### FIXME: BUG: These cause a race hazard where if the listen
                ### event isn't registered before we do a mouse up it crashes
                ### when we try to drop the note.  Not cool.
                self.addListenEvent(pygame.MOUSEBUTTONUP)
                self.addListenEvent(pygame.MOUSEMOTION)

            if event.button == 3:
                # Right click - Note off
                self.send(producerFinished(message=surface),
                          "display_signal")
                self.removeNote(noteId, True)

            if event.button == 4:
                # Scroll up - Velocity up
                # Floating point strangeness - use 0.951 rather than 0.95
                if velocity > 0 and velocity <= 0.951:
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
            # We haven't clicked on an existing note
            if event.button == 1:
                # Left click - Note on
                # Make sure it fits by adjusting the note length if we need to
                if beat + self.noteLength > self.loopBars * self.beatsPerBar:
                    self.noteLength = self.loopBars * self.beatsPerBar - beat
                noteId = self.addNote(beat, self.noteLength,
                                      noteNumber, 0.7, send=True)
                self.drawNoteRect(noteId)
        self.requestRedraw()

    def handleMouseUp(self, event):
        """
        Handle mouse up events from the pygame display
        """
        if event.button == 1:
            if self.moving:
                noteId, deltaPos = self.moving
                self.moving = False
                self.moveNote(noteId, True)

            if self.resizing:
                noteId, deltaPos = self.resizing
                self.resizeNote(noteId, True)
                self.redrawNoteRect(noteId)
                # Change the note length so the next note we create is the same
                # length
                # FIXME: This should probably happen when we move a note too
                self.noteLength = self.notes[noteId]["length"]
                self.resizing = False
            self.requestRedraw()
            self.removeListenEvent(pygame.MOUSEBUTTONUP)
            self.removeListenEvent(pygame.MOUSEMOTION)
            self.scrolling = 0

    def handleMouseMotion(self, event):
        """
        Handle mouse motion events from the pygame display
        """
        if self.moving:
            noteId, deltaPos = self.moving
            # Get the real start position, taking into account where we clicked
            # on the note
            position = []
            for i in xrange(2):
                position.append(event.pos[i] - deltaPos[i])
            beat, noteNumber = self.positionToNote(position)

            totalBeats = self.loopBars * self.beatsPerBar
            length = self.notes[noteId]["length"]

            # Don't move the note outside of the visible region vertically
            if noteNumber > self.maxVisibleNote:
                noteNumber = self.maxVisibleNote
            if noteNumber < self.minVisibleNote:
                noteNumber = self.minVisibleNote

            # Don't move the note outside of the visible region horizontally
            if beat < 0:
                beat = 0
            if beat + length > totalBeats:
                beat = totalBeats - length
            
            self.setNoteNumber(noteId, noteNumber)
            self.notes[noteId]["beat"] = beat 
            self.moveNoteRect(noteId)

            if event.pos[1] >= self.size[1]:
                # Scroll down
                if noteNumber > 0:
                    self.scrolling = -1
            elif event.pos[1] <= 0:
                # Scroll up
                if noteNumber < len(noteList) - 1:
                    self.scrolling = 1
            else:
                self.scrolling = 0

            if ((self.scrolling == 1 or self.scrolling == -1) and
                not self.scrollEvent):
                # We need to scroll and aren't already, so set the ball rolling
                self.scrollEvent = self.scheduleRel("Scroll", 0.2, 4)

        if self.resizing:
            # We ignore deltaPos for resizing 'cause the tab size is pretty
            # small anyway so it's probably not worth it
            noteId, deltaPos = self.resizing

            endBeat, noteNumber = self.positionToNote(event.pos)
            beat = self.notes[noteId]["beat"]

            length = endBeat - beat
            if length < 0:
                # Minimum of an eighth note
                # TODO : Check is this is too big
                length = 1.0/8
            if endBeat > self.loopBars * self.beatsPerBar:
                length = self.loopBars * self.beatsPerBar - beat

            # SMELL: Slow down the refresh rate by only drawing every few 
            # resizes.  This makes resizing much more responsive, but smellier
            self.notes[noteId]["length"] = length
            if self.resizeCount % 3 == 0:
                self.redrawNoteRect(noteId)
            self.resizeCount += 1
            
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

        self.addListenEvent(pygame.MOUSEBUTTONDOWN)

        # Background surface - this is what we draw the background markings onto
        displayRequest = {"DISPLAYREQUEST" : True,
                          "callback" : (self,"callback"),
                          "size": self.size,
                          "position" : (0, 0)
                         }
        if self.position:
            displayRequest["position"] = self.position
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

        while 1:
            if self.dataReady("inbox"):
                for event in self.recv("inbox"):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        bounds = self.display.get_rect()
                        if bounds.collidepoint(*event.pos):
                            self.handleMouseDown(event)

                    if event.type == pygame.MOUSEBUTTONUP:
                        self.handleMouseUp(event)

                    if event.type == pygame.MOUSEMOTION:
                        self.handleMouseMotion(event)

            if self.dataReady("remoteChanges"):
                data = self.recv("remoteChanges")
                # Only the last part of an OSC address
                address = data[0].split("/")[-1]
                if address == "Add":
                    noteId = data[1][0]
                    # Add the note to the scheduler
                    self.addNote(noteId=noteId, *data[1][1:])
                    # Draw it if we need to see it
                    if self.noteIsVisible(noteId):
                        self.drawNoteRect(noteId)
                if address == "Remove":
                    noteId = data[1][0]
                    if self.notes.has_key(noteId):
                        # We know about the note
                        # Delete the rect first so we still know the note info
                        if self.noteIsVisible(noteId):
                            self.deleteNoteRect(noteId)
                        # Remove the note fully
                        self.removeNote(noteId)
                if address == "Velocity":
                    noteId = data[1][0]
                    if self.notes.has_key(noteId):
                        # We know about the note
                        velocity = data[1][1]
                        surface = self.notes[noteId]["surface"]
                        self.setVelocity(noteId, velocity)
                        # Set the opacity if the note is on screen
                        if self.noteIsVisible(noteId):
                            surface = self.notes[noteId]["surface"]
                            surface.set_alpha(255 * velocity)
                if address == "Move":
                    noteId = data[1][0]
                    if self.notes.has_key(noteId):
                        # We know about the note
                        oldNoteNumber = self.notes[noteId]["noteNumber"]
                        beat = data[1][1]
                        noteNumber = data[1][2]
                        # Stop the note if it is playing
                        if self.notes[noteId]["playing"]:
                            self.sendNoteOff(noteId)
                        # Whether the note is visible
                        isVisible = self.noteIsVisible(noteId)
                        # Set the new beat and note number
                        self.notes[noteId]["beat"] = beat
                        self.setNoteNumber(noteId, noteNumber)
                        # Reschedule the note for the new time
                        self.cancelNote(noteId)
                        self.moveNote(noteId)
                        # Whether the note should be visible
                        needVisible = self.noteIsVisible(noteId)
                        # Either draw, move or delete the note rect, depending
                        # on whether it was and should be visible
                        if isVisible:
                            if needVisible:
                                self.moveNoteRect(noteId)
                            else:
                                self.deleteNoteRect(noteId)
                        elif needVisible:
                            self.drawNoteRect(noteId)
                if address == "Resize":
                    noteId = data[1][0]
                    if self.notes.has_key(noteId):
                        # We know about the note
                        length = data[1][1]
                        # Stop the note if it's playing 
                        if self.notes[noteId]["playing"]:
                            self.sendNoteOff(noteId)
                        self.notes[noteId]["length"] = length
                        # Cancel and reschedule the note
                        self.cancelNote(noteId)
                        self.resizeNote(noteId)
                        # Draw it if we need to
                        if self.noteIsVisible(noteId):
                            self.redrawNoteRect(noteId)
                self.requestRedraw()

            if self.dataReady("event"):
                data = self.recv("event")
                if data == "Beat":
                    self.updateBeat()

                elif data == "Scroll":
                    if self.scrolling == 1:
                        if self.maxVisibleNote < len(noteList):
                            self.scrollUp()
                            # Make sure the note we are dragging stays at the
                            # top of the piano roll
                            noteId = self.moving[0]
                            self.setNoteNumber(noteId, self.maxVisibleNote)
                            self.moveNoteRect(noteId)

                    if self.scrolling == -1:
                        if self.minVisibleNote > 0:
                            self.scrollDown()
                            noteId = self.moving[0]
                            self.setNoteNumber(noteId, self.minVisibleNote)
                            self.moveNoteRect(noteId)

                    if self.scrolling != 0:
                        self.scrollEvent = self.scheduleRel("Scroll", 0.2, 4)
                    else:
                        self.scrollEvent = None

                elif data[0] == "NoteOn":
                    noteId = data[1]
                    self.sendNoteOn(noteId)
                    self.scheduleNoteOn(noteId)
                elif data[0] == "NoteOff":
                    noteId = data[1]
                    self.sendNoteOff(noteId)
                    self.scheduleNoteOff(noteId)

            if self.dataReady("sync"):
                # Ignore any sync messages once as we have already synced by
                # now
                self.recv("sync")

            if not self.anyReady():
                self.pause()

class PianoRollMidiConverter(component):
    channel = 0
    def main(self):
        while 1:
            if self.dataReady("inbox"):
                message = self.recv("inbox")
                address = message[0].split("/")[-1]
                if address == "On":
                    noteNumber, velocity = message[1]
                    self.send((0x90 + self.channel, noteNumber,
                               int(velocity*127)), "outbox")
                elif address == "Off":
                    noteNumber = message[1]
                    self.send((0x80 + self.channel, noteNumber, 0), "outbox")
                    
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
    #PianoRoll().run()

    #from Kamaelia.Chassis.Graphline import Graphline
    #Graphline(pr1 = PianoRoll(), pr2 = PianoRoll(position=(600, 0)),
    #          linkages={("pr1","localChanges"):("pr2", "remoteChanges")}).run()

    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Apps.Jam.Protocol.Midi import Midi
    Pipeline(PianoRoll(), PianoRollMidiConverter(), Midi()).run()
