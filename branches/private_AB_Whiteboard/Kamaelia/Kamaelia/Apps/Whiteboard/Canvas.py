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
import os
import pygame

from datetime import datetime
from zipfile import ZipFile

from Tkinter import Tk
from tkFileDialog import askopenfilename
from tkSimpleDialog import askstring
from tkMessageBox import askyesno

from Axon.Ipc import WaitComplete, producerFinished, shutdownMicroprocess
from Kamaelia.UI.PygameDisplay import PygameDisplay




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
                 "fromEmail" : "Accepts status messages back from the e-mail component - TEMPORARY",
               }
    Outboxes = { "outbox" : "Issues drawing instructions",
                 "signal" : "",
                 "toDisplay" : "For sending requests to PygameDisplay service",
                 "eventsOut" : "Events forwarded out of here",
                 "surfacechanged" : "If the surface gets changed from last load/save a 'dirty' message is emitted here",
                 "toTicker" : "Send data to text ticker",
                 "toHistory" : "Move to first slide",
                 "toEmail" : "For sending out e-mails in list format - TEMPORARY",
               }

    def __init__(self, position=(0,0), size=(1024,768), bgcolour=(255,255,255), notepad="Scribbles", email=False):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Canvas,self).__init__()
        self.position = position
        self.size = size
        self.antialias = False
        self.bgcolour = bgcolour
        self.notepad = notepad
        
        # This will be moved out of here before branch completion
        self.email = email

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
        #argd["transparency"] = self.bgcolour # This causes problems when using OpenGL.
	#Modified to something that works with most apps - not sure why it does
	argd["transparency"] = (255,255,180)
        self.send(argd, "toDisplay")
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
        #yield 1 #FIXME
        #yield 1 #FIXME
        #yield 1 #FIXME
        #yield 1 #FIXME
        yield WaitComplete(
              self.requestDisplay( DISPLAYREQUEST=True,
                                   callback = (self,"fromDisplay"),
                                   events = (self, "eventsIn"),
                                   size = self.size,
                                   position = self.position,
                                 )
              )

        self.surface.fill( (self.bgcolour) )
        self.send({"REDRAW":True, "surface":self.surface}, "toDisplay")


        self.send( {"ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN, "surface" : self.surface},
                   "toDisplay" )
        self.send( {"ADDLISTENEVENT" : pygame.MOUSEMOTION, "surface" : self.surface},
                   "toDisplay" )
        self.send( {"ADDLISTENEVENT" : pygame.MOUSEBUTTONUP, "surface" : self.surface},
                   "toDisplay" )

        while not self.finished():
            
            #TEMPORARY - to be moved to another component
            while self.dataReady("fromEmail"):
                status = self.recv("fromEmail")
                if status == "sent":
                    self.send(". Deck e-mailed successfully","toTicker")
                else:
                    self.send(". Error sending deck by e-mail: " + status,"toTicker")

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
        elif cmd=="DELETESLIDE":
            self.deleteslide(args)
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
        elif cmd== "QUIT":
            self.quit(args)

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
        if filename != "":
            root = Tk()
            root.withdraw()
            password = askstring("Deck Password","Please enter the password for this zip file, or press cancel if you believe there isn't one:", parent=root)
            root.destroy()
            if filename:
                try:
                    unzipped = ZipFile(filename)
                    self.clearscribbles("")
                    if password != None:
                        unzipped.extractall(path=self.notepad,pwd=password)
                    else:
                        unzipped.extractall(path=self.notepad,pwd="")
                    files = os.listdir(self.notepad)
                    files.sort()
                    self.send("first", "toHistory")
                    self.send(chr(0) + "CLRTKR", "toTicker")
                    self.send("Deck loaded successfully","toTicker")
                except Exception, e:
                    self.send(chr(0) + "CLRTKR", "toTicker")
                    self.send("Failed to open the deck specified. You may have entered the password incorrectly","toTicker")
        self.clean = True

    def savedeck(self, args):
        num_pages = 0
        for x in os.listdir(self.notepad):
            if (os.path.splitext(x)[1] == ".png"):
                num_pages += 1
        if num_pages > 0:
            dt = datetime.now()
            filename = dt.strftime("%Y%m%d-%H%M%S")
            filename = filename + ".zip"
            root = Tk()
            root.withdraw()
            success = False
            if askyesno("Deck Password","Would you like this deck to be password protected?",parent=root):
                root.destroy()
                root = Tk()
                root.withdraw()
                password = ""
                while password == "":
                    password = askstring("Deck Password","Please enter a password for the zip file:", parent=root)

                if password != None:
                    # Ensure the user hasn't pressed Cancel - if not, proceed, otherwise don't save
                    try:
                        os.system("zip -j -q -P " + password + " Decks/" + filename + " " + self.notepad + "/*.png")
                        self.send(chr(0) + "CLRTKR", "toTicker")
                        self.send("Zip file 'Decks/" + filename + "' created successfully with password","toTicker")
                        success = True
                    except Exception, e:
                        self.send(chr(0) + "CLRTKR", "toTicker")
                        self.send("Failed to write to zip file 'Decks/" + filename + "'","toTicker")
            else:
                try:
                    os.system("zip -j -q Decks/" + filename + " " + self.notepad + "/*.png")
                    self.send(chr(0) + "CLRTKR", "toTicker")
                    self.send("Zip file 'Decks/" + filename + "' created successfully without password","toTicker")
                    success = True
                except Exception, e:
                    self.send(chr(0) + "CLRTKR", "toTicker")
                    self.send("Failed to write to zip file 'Decks/" + filename + "'","toTicker")

            root.destroy()

            if success == True and self.email == True:
                # Ask if the user wants to e-mail a copy to themselves
                root = Tk()
                root.withdraw()
                if askyesno("E-mail Deck","Would you like to send a copy of this deck by e-mail?",parent=root):
                    root.destroy()
                    root = Tk()
                    root.withdraw()
                    address = ""
                    while address == "":
                        address = askstring("E-mail Deck","Please enter an e-mail address. Multiple addresses can be entered if separated by semicolons:", parent=root)

                    if address != None:
                        # We have an address - no idea if it's valid or not, but this is where we'll send the message
                        body = "Your whiteboard deck has been attached\n\nSent via Whiteboard"
                        self.send([address,"Whiteboard Deck " + filename,body,["Decks/" + filename]], "toEmail")

                root.destroy()
        else:
            self.send(chr(0) + "CLRTKR", "toTicker")
            self.send("Save failed: No slides appear to exist","toTicker")
        self.clean = True
        
    def clearscribbles(self, args):
        try:
            for x in os.listdir(self.notepad):
                if os.path.splitext(x)[1] == ".png":
                    os.remove(self.notepad + "/" + x)
            self.clear("")
            self.send("first", "toHistory")
        except Exception, e:
            pass
        self.clean = True
        
    def deleteslide(self, args):
        self.clear("")
        self.send("delete", "toHistory")
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
        if location == "local":
            imageorigin = (imageorigin[0], imageorigin[1] + 141)
        self.surface.blit(snapshot, imageorigin)
        self.redrawNeeded = True
        self.send({"REDRAW":True, "surface":self.surface}, "toDisplay")
        
    def quit(self, args):
        root = Tk()
        root.withdraw()
        kill = False
        if askyesno("Confirm","Unsaved changes will be lost. Are you sure you want to quit?",parent=root):
            # perform quit
            kill = True
            #pygame.quit() # This isn't the right way to do it!
            # Also, saving won't work as the program exits before it's happened
        root.destroy()
        if kill:
            print("Exiting")
            self.scheduler.stop()
