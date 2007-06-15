#!/usr/bin/env  python
#simple scrolling textbox using Pygame

import pygame
import time
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished

class TextDisplayer(component):
    #inboxes: inbox, control
    #outboxes: outbox, signal
    def __init__(self, screen_width=300, screen_height=200, text_height=14,
                 background_color = (255,255,255), text_color=(0,0,0)):
        super(TextDisplayer, self).__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.text_height = text_height
        self.background_color = background_color
        self.text_color = text_color
        
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.screen.fill(background_color)
        pygame.display.update()
        
        self.scratch = self.screen.copy()
        self.font = pygame.font.Font(None, 14)
        self.linelen = self.screen_width/self.font.size('a')[0]
        self.keepRect = pygame.Rect((0, text_height), (screen_width, screen_width-text_height))
        self.scrollingRect = pygame.Rect((0, 0), (screen_width, screen_height - text_height))
        self.writeRect = pygame.Rect((0, screen_height-text_height), (screen_width, text_height))
        self.done = False
    
    def main(self):
        while not self.shutdown():
            yield 1
            if self.dataReady('inbox'):
                line = self.recv('inbox')
                self.update(line)
            pygame.display.update() #constantly refresh screen 

    def update(self, text):
        while len(text) > self.linelen:
            cutoff = text.rfind(' ', 0, self.linelen)
            self.updateLine(text[0:cutoff])
            text = text[cutoff + 1:]
        self.updateLine(text)
            
    def updateLine(self, line):            
        lineSurf = self.font.render(line, True, self.text_color)    
        self.screen.fill(self.background_color)
        self.screen.blit(self.scratch, self.scrollingRect, self.keepRect)
        self.screen.blit(lineSurf, self.writeRect)
        self.scratch.fill(self.background_color)
        self.scratch.blit(self.screen, self.screen.get_rect())
        pygame.display.update()

    def shutdown(self):
        while self.dataReady("control"):
           msg = self.recv("control")
           if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
               self.send(msg, "signal")
               return True
        if self.done or pygame.event.get(pygame.QUIT):
            self.send(producerFinished(), "signal")
            return True


if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import Pipeline
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
                yield 1
##            self.send(shutdownMicroprocess(), 'signal')

    Pipeline(Chargen(), textScroller()).run()
