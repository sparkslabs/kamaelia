import pygame
from Kamaelia.UI.Pygame.Display import PygameDisplay
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.UI.Pygame.KeyEvent import KeyEvent
from pygame.locals import *

width = 400
height = 200

displayservice = PygameDisplay.getDisplayService()
g = Graphline(displayservice = displayservice,
              linkages = {("self", "outbox") : displayservice,
                          }
              )

disprequest = {"DISPLAYREQUEST" : True,
               "size" : (width,height),               # pixels size for the new surface
               "callback" : (g, "inbox"),  # to send the new surface object to
               "events" : (g, "events")
}

