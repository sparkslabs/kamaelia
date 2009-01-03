#!/usr/bin/python

import time
from background import background
from Kamaelia.UI.Pygame.Text import Textbox
from LikeFile import LikeFile
background().start()

import Queue

TB = LikeFile(
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
    print "."
    try:
       print TB.get()
    except Queue.Empty:
       pass
