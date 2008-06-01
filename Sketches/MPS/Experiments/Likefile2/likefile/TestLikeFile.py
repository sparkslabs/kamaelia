#!/usr/bin/python

import time
from background import background
from Kamaelia.UI.Pygame.Text import Textbox, TextDisplayer
from LikeFile import LikeFile
background().start()

import Queue
TD = LikeFile(
         TextDisplayer(position=(20, 90),
                       text_height=36,
                       screen_width=900,
                       screen_height=200,
                       background_color=(130,0,70),
                       text_color=(255,255,255)
                      )
     ).activate()

TB = LikeFile(
        Textbox(position=(20, 340),
                text_height=36,
                screen_width=900,
                screen_height=400,
                background_color=(130,0,70),
                text_color=(255,255,255)
               )
     ).activate()

message = "hello\n"
while 1:
    time.sleep(1)
    print "."
    try:
       data,box = TB.get()
       print data, box
       message = data
    except Queue.Empty:
       pass
    TD.put(message, "inbox")
