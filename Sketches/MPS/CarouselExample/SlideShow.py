#!/usr/bin/env python
##
## Copyright (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
##     All Rights Reserved.
##
from Kamaelia.Chassis.Carousel import Carousel
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Chooser import Chooser
from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.UI.Pygame.Text import TextDisplayer
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor

files = [ "1.txt", "2.txt", "3.txt", "4.txt" ]

def makeFileReader(filename):
    return ReadFileAdaptor(filename = filename )

Graphline(
    NEXT = Button(caption="Next", msg="NEXT", position=(72,8)),
    PREVIOUS = Button(caption="Previous", msg="PREV",position=(8,8)),
    CHOOSER = Chooser(items = files),
    READER = Carousel(componentFactory = makeFileReader),
    DISPLAY = TextDisplayer(position=(20, 90), screen_width=800, screen_height=600),
    linkages = {
        ("NEXT","outbox"):("CHOOSER","inbox"),
        ("PREVIOUS","outbox"):("CHOOSER","inbox"),
        ("CHOOSER","outbox"):("READER","next"),
        ("READER","outbox"):("DISPLAY","inbox"),
    }
).run()
