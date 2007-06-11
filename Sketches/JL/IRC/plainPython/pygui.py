#simple scrolling textbox using Pygame

import pygame
import sys
import threading

class textbox(object):
    def __init__(self, screen_width=300, screen_height=200, text_height=14,
                 background_color = (255,255,255), text_color=(0,0,0)):
        super(textbox, self).__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.text_height = text_height
        self.background_color = background_color
        self.text_color = text_color
        self.linelen = 70
        
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.screen.fill(background_color)
        self.scratch = self.screen.copy()
        self.font = pygame.font.Font(None, 14)
        
        self.keepRect = pygame.Rect((0, text_height), (screen_width, screen_width-text_height))
        self.scrollingRect = pygame.Rect((0, 0), (screen_width, screen_height - text_height))
        self.writeRect = pygame.Rect((0, screen_height-text_height), (screen_width, text_height))

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

class inputThread(threading.Thread):
    def __init__(self, gui):
        super(inputThread, self).__init__()
        self.gui = gui
        self.done = False
        
    def run(self):
        while not self.done:
            msg = raw_input('You say: ')
            self.gui.update(msg)
            if msg == 'exit':
                pygame.event.post(pygame.event.Event(pygame.QUIT))

class UtilThread(threading.Thread):
    def __init__(self, threads):
        super(UtilThread, self).__init__()
        self.threads = threads
        
    def checkForShutdown(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False
                
    def run(self):
        while True:
            if self.checkForShutdown():
                for one_thread in self.threads:
                    one_thread.done = True
                    print 'Press any key to exit.'
                break
            else:
                pygame.display.update()

class ui(object):
    def __init__(self):
        super(ui, self).__init__()
        gui = textbox()
        input1 = inputThread(gui)
        util = UtilThread([input1])
        input1.start()
        util.start()

done = False
if __name__ == '__main__':
    UI = ui()
    
