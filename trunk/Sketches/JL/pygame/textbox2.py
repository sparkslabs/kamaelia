import pygame
from Kamaelia.UI.Pygame.Display import PygameDisplay
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.UI.Pygame.KeyEvent import KeyEvent
from pygame.locals import *
import Axon


class dummy(Axon.Component.component):
    def __init__(self):
        super(dummy, self).__init__()
        width = 400
        height = 200
        displayservice = PygameDisplay.getDisplayService()
        disprequest = {"DISPLAYREQUEST" : True,
                       "size" : (width,height),               # pixels size for the new surface
                       "callback" : (self, "inbox"),  # to send the new surface object to
                       "events" : (self, "events")
        }
        self.link((self, 'outbox'), displayservice)
        self.send(disprequest, 'outbox')

    def main(self):
        while True:
            yield 1
            
        
