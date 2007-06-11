#pygame GUI

import pygame
import sys
import threading

WHITE = (255, 255, 255)
BLACK = (0,0,0)

class gui(threading.Thread):
    def __init__(self, screen_width=300, screen_height=200, text_height=14):
        super(gui, self).__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.text_height = text_height
        self.linelen = 70
        
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.screen.fill(WHITE)
        self.scratch = pygame.Surface((screen_width, screen_height))
        self.scratch.fill(WHITE)
        self.font = pygame.font.Font(None, 14)
        self.keepRect = pygame.Rect((0, text_height), (screen_width, screen_width-text_height))
        self.scrollingRect = pygame.Rect((0, 0), (screen_width, screen_height - text_height))
        self.writeRect = pygame.Rect((0, screen_height-text_height), (screen_width, text_height))
        pygame.display.update()

    def update(self, line):            
        lineSurf = self.font.render(line, True, BLACK)    
        self.screen.fill(WHITE)
        self.screen.blit(self.scratch, self.scrollingRect, self.keepRect)
        self.screen.blit(lineSurf, self.writeRect)
        self.scratch.fill(WHITE)
        self.scratch.blit(self.screen, self.screen.get_rect())
        pygame.display.update()

    def run(self):
        while not done:
            msg = raw_input('> ')
            while len(msg) > self.linelen:
                cutoff = msg.rfind(' ', 0, self.linelen)
                self.update(msg[0:cutoff])
                msg = msg[cutoff + 1:]
            self.update(msg)

class shutdownThread(threading.Thread):
    def checkForShutdown(self):
        global done
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print 'Press any key to shut down...'
                done = True

    def run(self):
        while not done:
            self.checkForShutdown()

class refreshThread(threading.Thread):
    def run(self):
        while not done:
            pygame.display.update()

done = False
gui().start()
shutdownThread().start()
