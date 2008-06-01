#!/usr/bin/python

import time
from background import background
from Kamaelia.UI.Pygame.Text import Textbox
from ThreadWrap import ThreadWrap
background().start()

TB = ThreadWrap(
        Textbox(position=(20, 340),
                text_height=36,
                screen_width=900,
                screen_height=400,
                background_color=(130,0,70),
                text_color=(255,255,255)
               )
     ).activate()

while 1:
    time.sleep(1)
