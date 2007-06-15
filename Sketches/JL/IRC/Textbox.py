#! /usr/bin/env python
#terminates! Upon an ESC or clicking on the X!
#doesn't play with PygameDisplay :(

from TextDisplayer import *
from pygame.locals import *

class Textbox(TextDisplayer):
    "Reads keyboard input and updates it on the screen. Upon seeing \
    a newline sends the input to it's 'outbox'"
    string_buffer = ''

    def setText(self, text):
        self.screen.fill(self.background_color)
        self.scratch.fill(self.background_color)
        self.update(text)

    def main(self):
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
    Pipeline(Textbox(), ConsoleEchoer()).run()
