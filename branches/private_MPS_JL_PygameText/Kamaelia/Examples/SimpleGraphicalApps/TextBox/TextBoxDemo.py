#!/usr/bin/python


from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.UI.Pygame.Text import Textbox, TextDisplayer

Pipeline(Textbox(screen_width = 800,
                 screen_height = 300,
                 position = (0,0)),
         TextDisplayer(screen_width = 800,
                       screen_height = 300,
                       position = (0,340))
         ).run()
