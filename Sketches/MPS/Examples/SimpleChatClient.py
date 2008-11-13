#!/usr/bin/python

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.UI.Pygame.Text import Textbox, TextDisplayer
from Kamaelia.Internet.TCPClient import TCPClient

Pipeline(
         Textbox(size = (800, 300), position = (100,380)),
         TCPClient("127.0.0.1", 1501),
         TextDisplayer(size = (800, 300), position = (100,40))
).run()

