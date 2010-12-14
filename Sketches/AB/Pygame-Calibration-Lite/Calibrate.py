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

import pygame
import cjson
from time import time

from Axon.Component import component
from Axon.Ipc import WaitComplete, producerFinished, shutdownMicroprocess
from Kamaelia.UI.PygameDisplay import PygameDisplay
from Kamaelia.File.WholeFileWriter import WholeFileWriter
from Kamaelia.Chassis.Graphline import Graphline

class Calibrate(component):
    '''
    A basic Pygame display calibrator intended primarily for use of the Kamaelia Whiteboard on touch screen displays.
    Ensures mouse clicks align properly with the display using captured co-ordinates
    NB: Only currently set up for 1024x768 displays - using this on larger displays will result in extrapolation of results and hence possible alignment errors
    '''

    Inboxes = {"inbox":"Receives data back from the file writer",
               "control":"",
               "fromDisplay":"Receives messages from the Pygame display",
               "eventsIn":"Receives mouse events from the Pygame display"}
    Outboxes = {"outbox":"For sending data to the file writer",
                "signal":"",
                "toDisplay":"Sends surface messages to the Pygame display"}

    def shutdown(self):
       """Return 0 if a shutdown message is received, else return 1."""
       if self.dataReady("control"):
           msg=self.recv("control")
           if isinstance(msg,producerFinished) or isinstance(msg,shutdownMicroprocess):
               self.send(producerFinished(self),"signal")
               return 0
       return 1

    def requestDisplay(self, **argd):
        # Create a Pygame display surface linked to local mailboxes
        displayservice = PygameDisplay.getDisplayService()
        self.link((self,"toDisplay"), displayservice)
        self.send(argd, "toDisplay")
        for _ in self.waitBox("fromDisplay"):
            yield 1
        self.surface = self.recv("fromDisplay")

    def waitBox(self,boxname):
        waiting = True
        while waiting:
            if self.dataReady(boxname):
                return
            else:
                yield 1

    def write(self, args):
        # Write data to the Pygame display
        x,y,size,r,g,b = [int(a) for a in args[0:6]]
        text = args[6]
        font = pygame.font.Font(None,size)
        textimg = font.render(text, True, (r,g,b))
        self.surface.blit(textimg, (x,y))

    def clear(self):
        # Clear the Pygame display
        self.surface.fill((255,255,255))

    def redraw(self):
        # Issue a redraw request to the display
        self.send({"REDRAW":True, "surface":self.surface}, "toDisplay")

    def main(self):
        # Set up the display
        yield WaitComplete(
              self.requestDisplay( DISPLAYREQUEST=True,
                                   callback = (self,"fromDisplay"),
                                   events = (self, "eventsIn"),
                                   size = (1024,768),
                                   position = (0,0),
                                 )
              )
        
        self.clear()
        self.redraw()

        # Add callbacks for mouse events
        self.send( {"ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN, "surface" : self.surface},
                   "toDisplay" )
        self.send( {"ADDLISTENEVENT" : pygame.MOUSEBUTTONUP, "surface" : self.surface},
                   "toDisplay" )

        # Write initial instructions to the display
        self.write(['150','300','30','255','0','0',"Please click each + for > 1 second as they appear to calibrate the display"])
        self.write(['300','350','30','255','0','0',"To begin, press anywhere on the display"])
        self.redraw()

        stage = 0
        eventtodo = False
        mousepress = time()
        calibdata = dict()
        while self.shutdown():
            # Watch for mouse events
            while not self.dataReady("eventsIn"):
                self.pause()
                yield 1
            events = self.recv("eventsIn")
            for data in events:
                if data.type == pygame.MOUSEBUTTONDOWN:
                    if data.button==1:
                        clickpos = data.pos
                        mousepress = time()
                elif data.type == pygame.MOUSEBUTTONUP:
                    if data.button==1:
                        # Ensure that mouse presses last at least one second if setting a calibration point
                        if time() - mousepress > 1 or stage == 0 or stage == 5:
                            stage += 1
                            eventtodo = True
            if eventtodo:
                if stage == 1:
                    # Click has been made to start the process - show first +
                    self.clear()
                    self.write(['10','10','50','255','0','0',"+"])
                    self.redraw()
                elif stage == 2:
                    # Click has been made on first +, store and show the next one
                    calibdata['topleftx'],calibdata['toplefty'] = clickpos
                    self.clear()
                    self.write(['994','10','50','255','0','0',"+"])
                    self.redraw()
                elif stage == 3:
                    # Click has been made on second...
                    calibdata['toprightx'],calibdata['toprighty'] = clickpos
                    self.clear()
                    self.write(['10','698','50','255','0','0',"+"])
                    self.redraw()
                elif stage == 4:
                    # Click has been made on third...
                    calibdata['bottomleftx'],calibdata['bottomlefty'] = clickpos
                    self.clear()
                    self.write(['994','698','50','255','0','0',"+"])
                    self.redraw()
                elif stage == 5:
                    # Click has been made on fourth, store and show exit message
                    calibdata['bottomrightx'],calibdata['bottomrighty'] = clickpos
                    # Write the stored data to a file
                    calibdata = ["pygame-calibration.conf",cjson.encode(calibdata)]
                    self.send(calibdata,"outbox")
                    # No error handling here - assuming it worked
                    while not self.dataReady("inbox"):
                        self.pause()
                        yield 1
                    self.clear()
                    self.write(['210','300','30','255','0','0',"Calibration complete - data saved to pygame-calibration.conf"])
                    self.write(['250','350','30','255','0','0',"Please copy this file to one of the following locations:"])
                    self.write(['400','390','20','255','0','0',"~/.kamaelia/Kamaelia.UI.Pygame"])
                    self.write(['380','420','20','255','0','0',"/usr/local/etc/kamaelia/Kamaelia.UI.Pygame"])
                    self.write(['400','450','20','255','0','0',"/etc/kamaelia/Kamaelia.UI.Pygame"])
                    self.write(['450','500','30','255','0','0',"Click to exit"])
                    self.redraw()
                elif stage == 6:
                    # Run exit here
                    self.scheduler.stop()
                eventtodo = False

            self.pause()
            yield 1

if __name__=="__main__":
    Graphline(CALIB=Calibrate(),WRITER=WholeFileWriter(),
                linkages={("CALIB","outbox"):("WRITER","inbox"),("WRITER","outbox"):("CALIB","inbox")},
              ).run()