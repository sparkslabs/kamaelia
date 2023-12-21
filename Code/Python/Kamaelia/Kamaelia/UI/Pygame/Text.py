#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------
#

"""
============================================
Pygame components for text input and display
============================================

TextDisplayer displays any data it receives on a Pygame surface. Every new piece
of data is displayed on its own line, and lines wrap automatically.

Textbox displays user input while the user types, and sends its string buffer
to its 'outbox' when it receives a '\n'.



Example Usage
-------------

To take user input in Textbox and display it in TextDisplayer::

    Pipeline(Textbox(size = (800, 300),
                     position = (0,0)),
             TextDisplayer(size = (800, 300),
                           position = (0,340))
             ).run()



How does it work? 
-----------------
TextDisplayer requests a display from the Pygame Display service and requests
that Pygame Display send all keypresses to it. Every time TextDisplayer receives
a keypress, it updates its string buffer and the display. 

If it receives a newline, or if text must wrap, it moves the existing text
upwards and blits the new line onto the bottom. 



Known issues
------------
The line wrapping length is specified by the width of the display divided by the
width of the letter 'a' in the displayed font, so lines may wrap too far off the
edge of the screen if the user types very narrow text (i.e. just spaces with no
other charachters), or too far inside the edge of the screen (usually).
"""

import pygame
import time
import Axon
from Kamaelia.UI.Pygame.Display import PygameDisplay
from Kamaelia.UI.Pygame.KeyEvent import KeyEvent
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished, WaitComplete

class TextDisplayer(component): # FIXME - can this be used to replace Ticker ?
    """\
    TextDisplayer(...) -> new TextDisplayer Pygame component.

    Keyword arguments:

    - size             -- (w, h) size of the TextDisplayer surface, in pixels.
                          Default (500, 300).
    - text_height      -- font size. Default 18.
    - bgcolour         -- tuple containing RGB values for the background color.
                          Default is a pale yellow.
    - fgcolour         -- tuple containing RGB values for the text color.
                          Default is black.
    - position         -- tuple containing x,y coordinates of the surface's
                          upper left corner in relation to the Pygame
                          window. Default (0,0)
    """
    Inboxes = {"inbox" : "for incoming lines of text",
               "_surface" : "for PygameDisplay to send surfaces to",
               "_quitevents" : "user-generated quit events",
               "control" : "shutdown handling"}
    
    Outboxes = {"outbox" : "not used",
                "_pygame" : "for sending requests to PygameDisplay",
                "signal" : "propagates out shutdown signals"}
    
    size = (500, 300)
    text_height=18
    bgcolour=(255,255,200)
    fgcolour=(0,0,0)
    position=(0,0)
    transparent = False
    font_file = None
    padding = 0
    border_size = 0
    border_colour = (128,128,128)

    def __init__(self, **argd):
        """Initialises"""
        # FIXME: Change this to use the same names in self as in the args (note is for thoughout the file)
        # FIXME: Change this to use **argd rather than positional params
        super(TextDisplayer, self).__init__(**argd)
        self.screen_width = self.size[0]
        self.screen_height = self.size[1]
        self.background_color = self.bgcolour
        self.text_color = self.fgcolour
        self.done = False
        self.padding = self.padding + self.border_size

        pygame.font.init()

    def clear(self):
        pygame.draw.rect(self.screen, self.border_colour, (0,0,self.screen_width,self.screen_height))
        bs = self.border_size
        pygame.draw.rect(self.screen, self.background_color, (bs,bs,self.screen_width-bs-bs,self.screen_height-bs-bs))

    def initPygame(self, **argd):
        """requests a display surface from the PygameDisplay service, fills
        the color in, and copies it"""
        displayservice = PygameDisplay.getDisplayService()
        self.link((self, "_pygame"), displayservice)
        if self.transparent:
            argd["transparency"] = self.bgcolour
        self.send(argd, "_pygame")
        while not self.dataReady("_surface"):
            yield 1
        self.screen = self.recv("_surface")
        self.clear()

        self.scratch = self.screen.copy()
        self.send({"REDRAW" : True,
                   "surface" : self.screen}, "_pygame")
        yield 1

        h = self.screen_height
        w = self.screen_width
        th = self.text_height                                     # Text height

        self.font = pygame.font.Font(self.font_file, th)
        th = self.text_height = self.font.get_linesize() # Adjust the rendering of text inside, such that it renders nicer

        self.linelen = w/self.font.size('a')[0]

        # First pass approach at adding basic padding into the model
        pad = self.padding

        padtop = self.padding
        padbottom = self.padding
        padleft = self.padding
        padright = self.padding
        
        self.keepRect      = pygame.Rect((0+padleft, th+padtop),(w - padleft - padright, h - th - padtop - padbottom))
        self.scrollingRect = pygame.Rect((0+padleft, 0+padtop), (w - padleft - padright, h - th - padtop - padbottom))
        self.writeRect     = pygame.Rect((0+padleft, h - th - padbottom), (w - pad - pad, th))

#        self.keepRect = pygame.Rect((0, th),(w, h - th))
#        self.scrollingRect = pygame.Rect((0, 0), (w, h - th))
#        self.writeRect = pygame.Rect((0, h - th), (w, th))

    def main(self):
        """Main loop"""
        yield 1
        yield 1
        yield 1
        yield WaitComplete(self.initPygame(DISPLAYREQUEST = True,
                                           size = (self.screen_width, self.screen_height),
                                           callback = (self, '_surface'),
                                           position = self.position))
        
        while not self.needShutdown():
            yield 1
            if self.dataReady('inbox'):
                line = str(self.recv('inbox'))
                self.update(line)
            while not self.anyReady():  # changed to while - can be woken by messages leaving as well as arriving
                self.pause()            # Looping here is safe, since we only update based on information on inboxes
                yield 1
#        print "DONE"
         # FIXME: Pygame display needs to be told that we have finished with the surface, so it can be removed, and deallocated.
        self.send(Axon.Ipc.producerFinished(message=self.screen), "_pygame")

    def update(self, text):
        """Updates text to the bottom of the screen while scrolling old text
        upwards. Delegates most of the work to updateLine"""
        while len(text) > self.linelen:
            cutoff = text.rfind(' ', 0, self.linelen)
            if cutoff == -1:
                cutoff = self.linelen
            self.updateLine(text[0:cutoff])
            text = text[cutoff + 1:]
        self.updateLine(text)
            
    def updateLine(self, line):
        """Updates one line of text to bottom of screen, scrolling old text upwards."""
        line = line.replace('\r', ' ')
        line = line.replace('\n', ' ')
        lineSurf = self.font.render(line, True, self.text_color, self.bgcolour)

        self.clear()
#        self.screen.fill(self.background_color)
        self.screen.blit(self.scratch, self.scrollingRect, self.keepRect)
        self.screen.blit(lineSurf, self.writeRect)
        self.scratch.fill(self.background_color)
        self.scratch.blit(self.screen, self.screen.get_rect())
        self.send({"REDRAW" : True,
                   "surface" : self.screen}, "_pygame")

    def needShutdown(self): # FIXME: Inconsistent with other components. Original comment for this claimed standard name was confusing. Is it?
        """Checks for control messages"""
        while self.dataReady("control"):
            msg = self.recv("control")
            if (isinstance(msg, producerFinished) or
                isinstance(msg, shutdownMicroprocess)):
                self.done = True
        if self.dataReady("_quitevents"):
            self.done = True
        if self.done:
            self.send(shutdownMicroprocess(), 'signal')
            return True
            

class Textbox(TextDisplayer):
    """\
    Textbox(...) -> New Pygame Textbox component

    Keyword Arguments:
    
    - Textbox inherits its keyword arguments from TextDisplayer. Please see
      TextDisplayer docs.

    Reads keyboard input and updates it on the screen. Flushes string buffer and
    sends it to outbox when a newline is encountered.
    """
    
    Inboxes = {"inbox" : "for incoming lines of text",
               "_surface" : "for PygameDisplay to send surfaces to",
               "_quitevents" : "user-generated quit events",
               "_events" : "key events",
               "control" : "shutdown handling"}
    
    Outboxes = {"outbox" : "not used",
                "_pygame" : "for sending requests to PygameDisplay",
                "signal" : "propagates out shutdown signals"}

    initial_string_buffer = ""

    def setText(self, text):
        """erases the screen and updates it with text"""
        self.screen.fill(self.background_color)
        self.scratch.fill(self.background_color)
        self.update(text)

    def main(self):
        """\
        Requests a surface from PygameDisplay and registers to listen for events
        Then enters the main loop, which checks for Pygame events and updates
        them to the screen.
        """
        yield 1
        yield 1
        yield 1
        yield WaitComplete(self.initPygame(DISPLAYREQUEST = True,
                                           size = (self.screen_width, self.screen_height),
                                           callback = (self, '_surface'),
                                           position = self.position,
                                           events = (self, "_events")))

        self.send({'ADDLISTENEVENT' : pygame.KEYDOWN,
                   'surface' : self.screen},
                  '_pygame')
        
        string_buffer = self.initial_string_buffer
        while not self.needShutdown(): # FIXME: Inconsistent - see method definition
            yield 1
            while self.dataReady('_events'):
                for event in self.recv('_events'):
                    char = event.unicode
                    if char == '\n' or char == '\r':
                        self.send(string_buffer)
                        string_buffer = ''
                    elif event.key == pygame.K_BACKSPACE:
                        string_buffer = string_buffer[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        self.done = True
                    else:
                        string_buffer += char
                    # Add a '|' character as a text cursor
                    self.setText(string_buffer + '|')
            while self.dataReady("inbox"):
                char = self.recv("inbox")
                if char == "\n" or char == "\r":
                    self.send(string_buffer)
                    string_buffer = ''
                elif char == "\x08":
                    string_buffer = string_buffer[:-1]
                else:
                    string_buffer += char
                self.setText(string_buffer + '|')
                    
            while not self.anyReady() and not self.needShutdown():  # changed to while - can be woken by messages leaving as well as arriving
                self.pause()            # Looping here is safe, since we only update based on information on inboxes
                yield 1

        self.send(Axon.Ipc.producerFinished(message=self.screen), "_pygame")


__kamaelia_components__ = (TextDisplayer, Textbox, )

if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer

    if 0:
        Pipeline(Textbox(size = (800, 300),
                         position = (0,0)),
                 TextDisplayer(size = (800, 300),
                               position = (0,340))
                 ).run()

    if 0: #old test just involving TextDisplayer
        from Kamaelia.Chassis.Pipeline import Pipeline
        from Kamaelia.Util.Console import ConsoleReader
        Pipeline(ConsoleReader(), TextDisplayer()).run()

    if 1: #old test just involving TextDisplayer
        import Axon
        import time
        from Kamaelia.Chassis.Pipeline import Pipeline

        #the long lines are there on purpose, to see if the component wraps text correctly.

        class TimedLineSender(Axon.ThreadedComponent.threadedcomponent):
            text =  """\
                    To be, or not to be: that is the question:
                    Whether 'tis nobler in the mind to suffer
                    The slings and arrows of outrageous fortune,
                    Or to take arms against a sea of troubles,
                    And by opposing end them? To die: to sleep;
                    No more; and by a sleep to say we end
                    The heart-ache and the thousand natural shocks That flesh is heir to, 'tis a consummation Devoutly to be wish'd. To die, to sleep;
                    To sleep: perchance to dream: ay, there's the rub;
                    For in that sleep of death what dreams may come
                    When we have shuffled off this mortal coil,
                    Must give us pause: there's the respect
                    That makes calamity of so long life;
                    """
            strip_leading = True
            debug = True
            delay = 0.5
            def main(self):
                lines = self.text.split('\n')
                for line in lines:
                    if self.strip_leading:
                        line = line.lstrip()
                    time.sleep(self.delay)
                    self.send(line) # remove preding spaces 
                self.send(producerFinished(), 'signal')

        Pipeline(TimedLineSender(),
                 TextDisplayer()).run()
