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
import zlib
from Axon.Ipc import WaitComplete, producerFinished, shutdownMicroprocess
from Kamaelia.UI.PygameDisplay import PygameDisplay
import pygame
from datetime import datetime
from zipfile import ZipFile
import os

#from FileDialog import *
from Tkinter import *
from tkFileDialog import askopenfilename
from tkSimpleDialog import askstring



try:
    import Image
except ImportError:
    print "WARNING: Python Imaging Library Not available, defaulting to bmp only mode"

class Canvas(Axon.Component.component):
    """\
    Canvas component - pygame surface that accepts drawing instructions
    """

    Inboxes =  { "inbox"   : "Receives drawing instructions",
                 "control" : "",
                 "fromDisplay"  : "For receiving replies from PygameDisplay service",
                 "eventsIn" : "For receiving PygameDisplay events",
               }
    Outboxes = { "outbox" : "Issues drawing instructions",
                 "signal" : "",
                 "toDisplay" : "For sending requests to PygameDisplay service",
                 "toApp" : "Send requests to app - for calibration", # MODIFICATION
                 "eventsOut" : "Events forwarded out of here",
                 "surfacechanged" : "If the surface gets changed from last load/save a 'dirty' message is emitted here",
                 "toTicker" : "Send data to text ticker",
                 "toFirstSlide" : "Move to first slide",
               }

    def __init__(self, position=(0,0), width=1024, height=768, bgcolour=(255,255,255), notepad="Scribbles"):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Canvas,self).__init__()
        self.position = position
        self.width = width
        self.height = height
        self.size = (width, height)
        self.antialias = False
        self.bgcolour = bgcolour
        self.notepad = notepad

        if self.antialias == True:
            self.pygame_draw_line = pygame.draw.aaline
        else:
            self.pygame_draw_line = pygame.draw.line
        self.dirty_sent = False

    def waitBox(self,boxname):
        waiting = True
        while waiting:
            if self.dataReady(boxname):
                return
            else:
                yield 1

    def requestDisplay(self, **argd):
        displayservice = PygameDisplay.getDisplayService()
        self.link((self,"toDisplay"), displayservice)
        argd["transparency"] = self.bgcolour
        self.send(argd, "toDisplay")
        self.send(argd, "toApp") # MODIFICATION
        for _ in self.waitBox("fromDisplay"):
            yield 1
        self.surface = self.recv("fromDisplay")

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False


    def main(self):
        """Main loop"""
        yield 1
        yield 1
        yield 1
        yield 1
        yield WaitComplete(
              self.requestDisplay( DISPLAYREQUEST=True,
                                   callback = (self,"fromDisplay"),
                                   events = (self, "eventsIn"),
                                   width = self.width,
                                   height = self.height,
                                   size = self.size,
                                   position = self.position,
                                 )
              )

        self.surface.fill( (self.bgcolour) )
        self.send({"REDRAW":True, "surface":self.surface}, "toDisplay")
        self.send({"REDRAW":True, "surface":self.surface}, "toApp") # MODIFICATION


        self.send( {"ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN, "surface" : self.surface},
                   "toDisplay" )
        self.send( {"ADDLISTENEVENT" : pygame.MOUSEMOTION, "surface" : self.surface},
                   "toDisplay" )
        self.send( {"ADDLISTENEVENT" : pygame.MOUSEBUTTONUP, "surface" : self.surface},
                   "toDisplay" )

        while not self.finished():
            
            self.redrawNeeded = False
            while self.dataReady("inbox"):
                msgs = self.recv("inbox")
#                \
#                print repr(msgs)
                for msg in msgs:
                    cmd = msg[0]
                    args = msg[1:]
                    # parse commands here
                    self.handleCommand(cmd, *args)
                yield 1
            
            if self.redrawNeeded:
                self.send({"REDRAW":True, "surface":self.surface}, "toDisplay")
                self.send({"REDRAW":True, "surface":self.surface}, "toApp") #MODIFICATION
                if not self.clean:
                    if not self.dirty_sent:
                        self.send("dirty", "surfacechanged")
                        self.dirty_sent = True

            # pass on events received from pygame display
            while self.dataReady("eventsIn"):
                self.send( self.recv("eventsIn"), "eventsOut" )

            self.pause()
            yield 1

    def handleCommand(self, cmd, *args):
        #
        # Could really take a dispatch pattern
        # Would then be pluggable.
        #
        cmd = cmd.upper()
        if   cmd=="CLEAR":
            self.clear(args)
            self.clean = True
            self.dirty_sent = False
        elif cmd=="LINE":
             self.line(args)
        elif cmd=="CIRCLE":
            self.circle(args)
            self.clean = False
        elif cmd=="LOAD":
            self.load(args)
            self.clean = True
            self.dirty_sent = False
        elif cmd=="SAVE":
            self.save(args)
            self.clean = True
            self.dirty_sent = False
        elif cmd=="LOADDECK":
            self.loaddeck(args)
            self.clean = True
            self.dirty_sent = False
        elif cmd=="SAVEDECK":
            self.savedeck(args)
            self.clean = True
            self.dirty_sent = False
        elif cmd=="CLEARSCRIBBLES":
            self.clearscribbles(args)
            self.clean = True
            self.dirty_sent = False
        elif cmd=="GETIMG":
            self.getimg(args)
            self.clean = False
        elif cmd=="SETIMG":
            self.setimg(args)
            self.clean = False
        elif cmd=="WRITE":
            self.write(args)
            self.clean = False
        elif cmd=="CAM":
            self.webcam(args)
            self.clean = True
            self.dirty_sent = True

    def line(self, args):
        (r,g,b,sx,sy,ex,ey) = [int(v) for v in args[0:7]]
        self.pygame_draw_line(self.surface, (r,g,b), (sx,sy), (ex,ey))
#        pygame.draw.aaline(self.surface, (r,g,b), (sx,sy), (ex,ey))
        self.redrawNeeded = True
        if not((sy <0) or (ey <0)):
            self.clean = False

    def clear(self, args):
        if len(args) == 3:
            self.surface.fill( [int(a) for a in args[0:3]] )
        else:
            self.surface.fill( (self.bgcolour) )
        self.redrawNeeded = True
        self.send("dirty", "surfacechanged")
        self.dirty_sent = True
        self.clean = True

    def circle(self, args):
        (r,g,b,x,y,radius) = [int(v) for v in args[0:6]]
        pygame.draw.circle(self.surface, (r,g,b), (x,y), radius, 0)
        self.redrawNeeded = True

    def load(self, args):
            filename = args[0]
#            print "ARGS", args
            try:
                loadedimage = pygame.image.load(filename)
            except:
                pass
            else:
                self.surface.blit(loadedimage, (0,0))
            self.redrawNeeded = True
            if not ( (len(args) >1) and args[1] == "nopropogate" ):
                self.getimg(())
            self.clean = True

    def save(self, args):
        filename = args[0]
        try:
            imagestring = pygame.image.tostring(self.surface,"RGB")
            pilImage = Image.fromstring("RGB", self.surface.get_size(), imagestring)
            pilImage.save(filename)
        except NameError:
            pygame.image.save(self.surface, filename)
        self.clean = True
        
    def loaddeck(self, args):
        root = Tk()
        root.withdraw()
        filename = askopenfilename(filetypes=[("Zip Archives",".zip")],initialdir="Decks",title="Load Slide Deck",parent=root)
        root.destroy()
        root = Tk()
        root.withdraw()
        password = askstring("Deck Password","Please enter the password for this zip file, or leave blank if there is no password:", parent=root)
        root.destroy()
        if (filename):
            try:
                unzipped = ZipFile(filename)
                self.clearscribbles("")
                unzipped.extractall(path=self.notepad,pwd=password)
                files = os.listdir(self.notepad)
                files.sort()
                loadstring = self.notepad + "/" + files[0]
                self.send("first", "toFirstSlide")
                self.send("CLRTKR", "toTicker")
                self.send("Deck loaded successfully","toTicker")
            except Exception, e:
                self.send("CLRTKR", "toTicker")
                self.send("Failed to open the deck specified. You may have entered the password incorrectly","toTicker")
        self.clean = True

    def savedeck(self, args):
        dt = datetime.now()
        filename = dt.strftime("%Y%m%d-%H%M%S")
        filename = filename + ".zip"
        num_pages = len(os.listdir(self.notepad))
        root = Tk()
        root.withdraw()
        password = askstring("Deck Password","Please enter a password for the zip file, or leave blank for no password:", parent=root)
        root.destroy()
        try:
            if (password != ""):
                #os.system("zip", "-j", "-q", "-P " + password, "Decks/" + filename, self.notepad + "/*.png")
                os.system("zip -j -q -P " + password + " Decks/" + filename + " " + self.notepad + "/*.png")
                self.send("CLRTKR", "toTicker")
                self.send("Zip file 'Decks/" + filename + "' created successfully with password","toTicker")
            else:
                os.system("zip -j -q Decks/" + filename + " " + self.notepad + "/*.png")
                """zipped = ZipFile('Decks/' + filename,'w') # This seems to have broken
                for x in range(num_pages + 1):
                    if (x > 0):
                        zipped.write(self.notepad + "/" +  "slide." + str(x) + ".png", "slide." + str(x) + ".png")
                zipped.close()"""
                self.send("CLRTKR", "toTicker")
                self.send("Zip file 'Decks/" + filename + "' created successfully without password","toTicker")
        except Exception, e:
            self.send("CLRTKR", "toTicker")
            self.send("Failed to write to zip file 'Decks/" + filename + "'","toTicker")
        self.clean = True
        
    def clearscribbles(self, args):
        try:
            #for x in os.listdir(self.notepad):
            for x in os.listdir(self.notepad):
                if (os.path.splitext(x)[1] == ".png"):
                    os.remove(self.notepad + "/" + x)
            self.clear("")
            self.send("first", "toFirstSlide")
        except Exception, e:
            pass
        self.clean = True

    def getimg(self, args):
            imagestring = pygame.image.tostring(self.surface,"RGB")
            imagestring = zlib.compress(imagestring)
            w,h = self.surface.get_size()
            self.send( [["SETIMG",imagestring,str(w),str(h),"RGB"]], "outbox" )
#            print "GETIMG"

    def setimg(self, args):
            w,h = int(args[1]), int(args[2])
            imagestring = zlib.decompress(args[0])
            recvsurface = pygame.image.frombuffer(imagestring, (w,h), args[3])
            self.surface.blit(recvsurface, (0,0))
            self.redrawNeeded = True

    def write(self, args):
            x,y,size,r,g,b = [int(a) for a in args[0:6]]
            text = args[6]
            font = pygame.font.Font(None,size)
            textimg = font.render(text, self.antialias, (r,g,b))
            self.surface.blit(textimg, (x,y))
            self.redrawNeeded = True

    def webcam(self, args):
        snapshot = args[0]
        imageorigin = args[1]
        location = args[2]
        self.surface.blit(snapshot, imageorigin) # temp
        if (location == "local"):
            imageorigin = (imageorigin[0], imageorigin[1] + 141)
        self.surface.blit(snapshot, imageorigin)
        self.redrawNeeded = True
        self.send({"REDRAW":True, "surface":self.surface}, "toDisplay")
        #self.send("dirty", "surfacechanged")