#!/usr/bin/env python
#
# (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
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
from Kamaelia.UI.Pygame.Display import PygameDisplay
from Kamaelia.UI.Pygame.KeyEvent import KeyEvent
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished, WaitComplete
from pygame.locals import *

    
class TextDisplayer(component):
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
    
    def __init__(self, size=(500, 300), text_height=18, bgcolour=(255,255,200),
                 fgcolour=(0,0,0), position=(0,0)):
        """Initialises"""
        super(TextDisplayer, self).__init__()
        self.screen_width = size[0]
        self.screen_height = size[1]
        self.text_height = text_height
        self.background_color = bgcolour
        self.text_color = fgcolour
        self.position = position
        self.done = False
        
    def initPygame(self, **argd):
        """requests a display surface from the PygameDisplay service, fills
        the color in, and copies it"""
        displayservice = PygameDisplay.getDisplayService()
        self.link((self, "_pygame"), displayservice)
        self.send(argd, "_pygame")
        while not self.dataReady("_surface"):
            yield 1
        self.screen = self.recv("_surface")
        self.screen.fill(self.background_color)
        self.scratch = self.screen.copy()
        self.send({"REDRAW" : True,
                   "surface" : self.screen}, "_pygame")
        yield 1

        h = self.screen_height
        w = self.screen_width
        th = self.text_height
        self.font = pygame.font.Font(None, th)
        self.linelen = w/self.font.size('a')[0]
        self.keepRect = pygame.Rect((0, th),(w, h - th))
        self.scrollingRect = pygame.Rect((0, 0), (w, h - th))
        self.writeRect = pygame.Rect((0, h - th), (w, th))

    def main(self):
        """Main loop"""
        yield WaitComplete(self.initPygame(DISPLAYREQUEST = True,
                                           size = (self.screen_width,
                                                   self.screen_height),
                                           callback = (self, '_surface'),
                                           position = self.position))
        
        while not self.needShutdown():
            yield 1
            if self.dataReady('inbox'):
                line = str(self.recv('inbox'))
                self.update(line)
            if not self.anyReady():
                self.pause()

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
        """Updates one line of text to bottom of screen, scrolling old text
           upwards."""
        line = line.replace('\r', ' ')
        line = line.replace('\n', ' ')
        lineSurf = self.font.render(line, True, self.text_color)    
        self.screen.fill(self.background_color)
        self.screen.blit(self.scratch, self.scrollingRect, self.keepRect)
        self.screen.blit(lineSurf, self.writeRect)
        self.scratch.fill(self.background_color)
        self.scratch.blit(self.screen, self.screen.get_rect())
        self.send({"REDRAW" : True,
                   "surface" : self.screen}, "_pygame")

    def needShutdown(self):
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

    def __init__(self, *args, **kwargs):
        super(Textbox, self).__init__(*args, **kwargs)
        self.string_buffer = ""

    def setText(self, text):
        """erases the screen and updates it with text"""
        self.screen.fill(self.background_color)
        self.scratch.fill(self.background_color)
        self.update(text)

    def main(self):
        """\
        Requests a surface from PygameDisplay and registers to listen for
        events.
        Then enters the main loop, which checks for Pygame events and updates
        them to the screen.
        """
        yield WaitComplete(self.initPygame(DISPLAYREQUEST = True,
                                           size = (self.screen_width,
                                                   self.screen_height),
                                           callback = (self, '_surface'),
                                           position = self.position,
                                           events = (self, "_events")))

        self.send({'ADDLISTENEVENT' : pygame.KEYDOWN,
                   'surface' : self.screen},
                  '_pygame')
        
        while not self.needShutdown():
            yield 1
            while self.dataReady('_events'):
                for event in self.recv('_events'):
                    char = event.unicode
                    if char == '\n' or char == '\r':
                        self.send(self.string_buffer)
                        self.string_buffer = ''
                    elif event.key == K_BACKSPACE:
                        self.string_buffer = self.string_buffer[:-1]
                    elif event.key == K_ESCAPE:
                        self.done = True
                    else:
                        self.string_buffer += char
                    # Add a '|' character as a text cursor
                    self.setText(self.string_buffer + '|')
            if not self.anyReady():
                self.pause()

__kamaelia_components__ = (TextDisplayer, Textbox, )

if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    
    Pipeline(Textbox(size = (800, 300),
                     position = (0,0)),
             TextDisplayer(size = (800, 300),
                           position = (0,340))
             ).run()

if 0: #old test just involving TextDisplayer
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleReader
    import time
    #the long lines are there on purpose, to see if the component wraps text correctly.
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

    class Chargen(component):
        def main(self):
            lines = text.split('\n')
            for one_line in lines:
                time.sleep(0.5)
                self.send(one_line)
                print one_line
                yield 1
##            self.send(producerFinished(), 'signal')

    Pipeline(ConsoleReader('>>>'), TextDisplayer()).run()
    
