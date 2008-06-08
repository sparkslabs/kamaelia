#!/usr/bin/python


from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.UI.Pygame.Text import Textbox, TextDisplayer

Pipeline(Textbox(size = (800, 300),
                 position = (0,0)),
         TextDisplayer(size = (800, 300),
                       position = (0,340))
         ).run()
