#simple scrolling textbox using Pygame

import pygame
import sys
import threading

WHITE = (255, 255, 255)
BLACK = (0,0,0)

class textbox(object):
    def __init__(self, screen_width=300, screen_height=200, text_height=14):
        super(textbox, self).__init__()
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

    def update(self, text):
        while len(text) > self.linelen:
            cutoff = text.rfind(' ', 0, self.linelen)
            self.updateLine(text[0:cutoff])
            text = text[cutoff + 1:]
        self.updateLine(text)
            
    def updateLine(self, line):            
        lineSurf = self.font.render(line, True, BLACK)    
        self.screen.fill(WHITE)
        self.screen.blit(self.scratch, self.scrollingRect, self.keepRect)
        self.screen.blit(lineSurf, self.writeRect)
        self.scratch.fill(WHITE)
        self.scratch.blit(self.screen, self.screen.get_rect())
        pygame.display.update()

class inputThread(threading.Thread):
    def __init__(self, gui):
        super(inputThread, self).__init__()
        self.gui = gui
        self.done = False
        
    def run(self):
        while not self.done:
            msg = raw_input('You say: ')
            self.gui.update(msg)

class shutdownThread(threading.Thread):
    def __init__(self, threads):
        super(shutdownThread, self).__init__()
        self.threads = threads
        self.done = False
        
    def checkForShutdown(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print 'Press any key to shut down...'
                for one_thread in self.threads:
                    one_thread.done = True
                self.done = True
                
    def run(self):
        while not self.done:
            self.checkForShutdown()

class refreshThread(threading.Thread):
    done = False
    def run(self):
        while not self.done:
            pygame.display.update()

class ui(object):
    def __init__(self):
        super(ui, self).__init__()
        gui = textbox()
        input1 = inputThread(gui)
        refresh = refreshThread()
        shutdown = shutdownThread([input1, refresh])
        input1.start()
        refresh.start()
        shutdown.start()

done = False
if __name__ == '__main__':
    UI = ui()
    
