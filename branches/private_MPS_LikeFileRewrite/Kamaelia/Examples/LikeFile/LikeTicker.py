#!/usr/bin/python

import Axon
from Axon.background import background
from Axon.LikeFile import LikeFile
from Kamaelia.UI.Pygame.Ticker import Ticker
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
import time

bg = background(slowmo=0.01).start()

ticker1 = LikeFile(Pipeline(
                            Ticker(background_colour=(128,48,128),
                                   render_left = 1,
                                   render_top = 1,
                                   render_right = 600,
                                   render_bottom = 200,
                                   position = (100, 250),
                            )
                   )
          ).activate()
ticker2 = LikeFile(Pipeline( 
                            Ticker(background_colour=(128,48,128),
                                render_left = 1,
                                render_top = 1,
                                render_right = 600,
                                render_bottom = 200,
                                position = (100, 0),
                            )
                   )
          ).activate()

ticker3 = LikeFile(Pipeline( 
                            Ticker(background_colour=(128,48,128),
                                render_left = 1,
                                render_top = 1,
                                render_right = 600,
                                render_bottom = 200,
                                position = (100, 500),
                            )
                   )
          ).activate()

for line in file("Ulysses", 'r+b'):
    line = line.rstrip() # kill the newlines - printing them in reverse order messes with the ticker.
    ticker1.put(line[::-1], "inbox")
    ticker2.put(line, "inbox")

time.sleep(5)

for line in file("Ulysses", 'r+b'):
    ticker3.put(line, "inbox")

time.sleep(10)

# we'll unceremoniously die now, since the ticker has no way to indicate when it's done drawing, or indeed to cleanly remove it from the pygame window. Sending
# a producerfinished would end it, but it'd remain in pygame.


