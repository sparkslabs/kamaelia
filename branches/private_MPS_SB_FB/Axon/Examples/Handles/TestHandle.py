#!/usr/bin/python

import time
from Axon.background import background
from Kamaelia.UI.Pygame.Text import Textbox, TextDisplayer
from Axon.Handle import Handle
background().start()

try:
   import Queue
   queue = Queue # Python 3 compatibility change
except ImportError:
   # Python 3 compatibility change
   import queue
TD = Handle(
         TextDisplayer(position=(20, 90),
                       text_height=36,
                       screen_width=900,
                       screen_height=200,
                       background_color=(130,0,70),
                       text_color=(255,255,255)
                      )
     ).activate()

TB = Handle(
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
    try:
       data = TB.get("outbox")
       print (data)
       message = data
    except queue.Empty:
       pass
    TD.put(message, "inbox")
