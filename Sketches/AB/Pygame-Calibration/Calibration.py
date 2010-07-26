#!/usr/bin/env python
#
# Copyright (C) 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
#

import Axon
import pygame

from Axon.Component import component
from Axon.Ipc import WaitComplete, producerFinished, shutdownMicroprocess

from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Pipeline import Pipeline

from Kamaelia.Util.Backplane import Backplane, PublishTo, SubscribeTo
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.File.WholeFileWriter import WholeFileWriter

#
# The following application specific components will probably be rolled
# back into the repository.
#
from Kamaelia.Apps.Whiteboard.TagFiltering import TagAndFilterWrapper
from Kamaelia.Apps.Whiteboard.Canvas import Canvas
from Kamaelia.Apps.Whiteboard.Painter import Painter
from Kamaelia.Apps.Whiteboard.TwoWaySplitter import TwoWaySplitter
from Kamaelia.Apps.Whiteboard.UI import ClearPage


from Calibrate import Calibrate

     
def calibButton(left, top):    
    return Button(caption="Calibrate", size=(63,32), position=(left, top))
        

def makeBasicSketcher(left=0,top=0,width=1024,height=768):
    return Graphline( CANVAS  = Canvas( position=(left,top+32),size=(width,height-32) ),
                      PAINTER = Painter(),
                      #CLEAR = ClearPage(left,top),
                      CALIBRATE = Calibrate(),
                      TWOWAY = TwoWaySplitter(),
                      CALIBBUTTON = calibButton(left,top),
                      FILEWRITER = WholeFileWriter(),

                      DEBUG   = ConsoleEchoer(),

                      linkages = {
                          ("CANVAS", "eventsOut") : ("PAINTER", "inbox"),

                          #("PAINTER", "outbox")    : ("CANVAS", "inbox"),
                          ("PAINTER", "outbox")    : ("TWOWAY", "inbox"),
                          #("CLEAR", "outbox")       : ("CANVAS", "inbox"),
                          
                          ("CALIBRATE", "outbox") : ("CANVAS", "inbox"),
                          #("CANVAS", "toApp") : ("CALIBRATE", "coords"),
                          
                          ("TWOWAY", "outbox")    : ("CALIBRATE", "coords"),
                          ("TWOWAY", "outbox2")    : ("CANVAS", "inbox"),
                          
                          ("CALIBBUTTON", "outbox") : ("CALIBRATE", "inbox"),
                          
                          ("CALIBRATE", "finaldata") : ("FILEWRITER", "inbox"),
                          ("FILEWRITER", "outbox") : ("CALIBRATE", "inbox"),
                          },
                    )

if __name__=="__main__":
    mainsketcher = \
        Graphline( SKETCHER = makeBasicSketcher(width=1024,height=768),
                   linkages = { ('','inbox'):('SKETCHER','inbox'),
                                ('SKETCHER','outbox'):('','outbox'),
                              }
                     )
    # primary calibrator
    Pipeline( SubscribeTo("CALIBRATOR"),
              TagAndFilterWrapper(mainsketcher),
              PublishTo("CALIBRATOR")
            ).activate()

    print("Starting calibration...")
    Backplane("CALIBRATOR").run()
    