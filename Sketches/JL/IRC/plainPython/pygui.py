#simple scrolling textbox using Pygame

import pygame
import sys
import threading
import time
from Axon.Component import component

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
For who would bear the whips and scorns of time,
The oppressor's wrong, the proud man's contumely,
The pangs of despised love, the law's delay,
The insolence of office and the spurns
That patient merit of the unworthy takes,
When he himself might his quietus make With a bare bodkin? who would fardels bear,
To grunt and sweat under a weary life,
But that the dread of something after death,
The undiscover'd country from whose bourn
No traveller returns, puzzles the will
And makes us rather bear those ills we have
Than fly to others that we know not of?
Thus conscience does make cowards of us all;
And thus the native hue of resolution
Is sicklied o'er with the pale cast of thought,
And enterprises of great pith and moment
With this regard their currents turn awry,
And lose the name of action. - Soft you now!
The fair Ophelia! Nymph, in thy orisons
Be all my sins remember'd.
"""

def datasource():
    lines = text.split('\n')
    for one_line in lines:
        yield one_line

class writer(component):
    def __init__(self, source, screen_width=300, screen_height=200, text_height=14,
                 background_color = (255,255,255), text_color=(0,0,0)):
        super(writer, self).__init__()
        self.source = source
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
    
    def main(self):
        while True:
            try:
                time.sleep(0.5)
                line = self.source.next()
                print line
                self.update(line)
                yield 1
            except StopIteration:
                break

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

def tests():
    source = datasource()
    writer(source).run()

if __name__ == '__main__':
    tests()
