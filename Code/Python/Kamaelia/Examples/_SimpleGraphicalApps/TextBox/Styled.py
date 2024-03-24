#!/usr/bin/python

from Kamaelia.UI.Pygame.Display import PygameDisplay
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.UI.Pygame.Text import Textbox, TextDisplayer

X = PygameDisplay(background_colour=(224,224,255),width=1000,height=400).activate()
PygameDisplay.setDisplayService(X)

Pipeline(
         Textbox(size = (800, 150), position = (100,230),      font_file="/home/michaels/.fonts/MichaelHW.ttf",padding=20, border_size=10, border_colour=(128,0,0)),
         TextDisplayer(size = (800, 150), position = (100,40), font_file="/home/michaels/.fonts/GillSans.ttf", padding=20, border_size=10, border_colour=(0,0,128))
).run()
                 
                  
