#! /usr/bin/env python
#terminates! Upon an ESC or clicking on the X!
#doesn't play with PygameDisplay :(

from TextDisplayer import *
from pygame.locals import *

class Textbox(TextDisplayer):
    "Reads keyboard input and updates it on the screen. Upon seeing \
    a newline sends the input to it's 'outbox'"
    Inboxes = {"inbox" : "for incoming lines of text",
               "_surface" : "for PygameDisplay to send surfaces to",
               "_quitevents" : "user-generated quit events",
               "_events" : "key events",
               "control" : "shutdown handling"}
    
    Outboxes = {"outbox" : "not used",
                "_pygame" : "for sending requests to PygameDisplay",
                "signal" : "propagates out shutdown signals"}

    string_buffer = ""
    def setText(self, text):
        self.screen.fill(self.background_color)
        self.scratch.fill(self.background_color)
        self.update(text)

    def main(self):
        for _ in self.initPygame(DISPLAYREQUEST = True,
                                 size = (self.screen_width, self.screen_height),
                                 callback = (self, '_surface'),
                                 position = self.position,
                                 events = (self, "_events")):
            yield 1

        self.send({'ADDLISTENEVENT' : True,
                   'surface' : self.screen
                   }
                  , '_pygame')
        while not self.shutdown():
            yield 1
            string_buffer = self.string_buffer
            for event in pygame.event.get():
                if (event.type == KEYDOWN):
                    char = event.unicode
                    if char == '\n' or char == '\r':
                        self.send(string_buffer)
                        string_buffer = ''
                    elif event.key == K_BACKSPACE:
                        string_buffer = string_buffer[:len(string_buffer)-1]
                    elif event.key == K_ESCAPE:
                        self.done = True
                    else:
                        string_buffer += char
                    self.setText(string_buffer + '|')
                    self.string_buffer = string_buffer

if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Chassis.Graphline import Graphline
    
    Pipeline(Textbox(screen_width = 800, screen_height = 300, position = (0,0)),
             TextDisplayer(screen_width = 800, screen_height = 300, position = (0,340))).run()
