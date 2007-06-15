#!/usr/bin/env  python
#simple scrolling textbox using Pygame

import pygame
import time
from Kamaelia.UI.Pygame.Display import PygameDisplay
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished

class TextDisplayer(component):
    Inboxes = {"inbox" : "for incoming lines of text",
               "_surface" : "for PygameDisplay to send surfaces to",
               "_quitevents" : "for PygameDisplay to send quit events to",
               "control" : "shutdown handling"}
    Outboxes = {"outbox" : "not used",
                "_pygame" : "for sending requests to PygameDisplay",
                "signal" : "propagates out shutdown signals"}
    
    def __init__(self, screen_width=300, screen_height=200, text_height=18,
                 background_color = (255,255,255), text_color=(0,0,0)):
        super(TextDisplayer, self).__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.text_height = text_height
        self.background_color = background_color
        self.text_color = text_color
        self.done = False
        
        displayservice = PygameDisplay.getDisplayService()
        self.link((self, "_pygame"), displayservice)
        
    def initPygame(self):
        self.send({"DISPLAYREQUEST" : True,
                   "size" : (self.screen_width, self.screen_height),
                   "callback" : (self, "_surface")}, "_pygame")
        while not self.dataReady("_surface"):
            yield 1
        self.screen = self.recv("_surface")
        self.screen.fill(self.background_color)
        self.scratch = self.screen.copy()
        self.send({"REDRAW" : True,
                   "surface" : self.screen}, "_pygame")

        h = self.screen_height
        w = self.screen_width
        th = self.text_height
        self.font = pygame.font.Font(None, th)
        self.linelen = w/self.font.size('a')[0]
        self.keepRect = pygame.Rect((0, th),(w, h - th))
        self.scrollingRect = pygame.Rect((0, 0), (w, h - th))
        self.writeRect = pygame.Rect((0, h - th), (w, th))

        self.send({"ADDLISTENEVENT" : pygame.QUIT,
                   "surface" : self.screen})
    
    def main(self):
        for _ in self.initPygame():
            yield 1
    
        while not self.shutdown():
            yield 1
            if self.dataReady('inbox'):
                line = self.recv('inbox')
                self.update(line)

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
        self.send({"REDRAW" : True,
                   "surface" : self.screen}, "_pygame")

    def shutdown(self):
        while self.dataReady("control"):
           msg = self.recv("control")
           if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
               self.send(msg, "signal")
               return True
        while self.dataReady("_quitevents"):
            msg = self.recv("_quitevents")
            if msg.type == pygame.QUIT:
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

    Pipeline(Chargen(), TextDisplayer()).run()
