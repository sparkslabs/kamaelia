#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
    