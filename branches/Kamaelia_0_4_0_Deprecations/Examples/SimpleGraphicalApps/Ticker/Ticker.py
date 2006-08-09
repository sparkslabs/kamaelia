#!/usr/bin/python

from Kamaelia.UI.Pygame.Ticker import Ticker
from Kamaelia.Chassis.Pipeline import pipeline
from Kamaelia.ReadFileAdaptor import ReadFileAdaptor

pipeline( ReadFileAdaptor("Ulysses",readmode="line",steptime=0.5),
          Ticker(background_colour=(128,48,128),
                 render_left = 1,
                 render_top = 1,
                 render_right = 600,
                 render_bottom = 200,
                 position = (100, 300),
          )
).run()
