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

from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring
from tkinter.messagebox import askyesno

from zipfile import ZipFile
from datetime import datetime

import os
import shutil
import sys
import time

from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import WaitComplete, producerFinished, shutdownMicroprocess

class Decks(threadedcomponent):
    # Many of these inboxes and outboxes are temporary until the structure is finalised
    Inboxes = {
        "inbox" : "Button click events result in messages to this inbox",
        "fromEmail" : "Status messages from the e-mail component are received back here",
        "control" : "",
    }
    Outboxes = {
        "outbox" : "",
        "toTicker" : "Sends text messages out to the Ticker component for display to the user",
        "toCanvas" : "Sends drawing instructions out to the Canvas component",
        "toSequencer" : "Sends slide navigation messages out to the CheckpointSequencer component",
        "toEmail" : "Requests to send e-mails are sent through this outbox",
        "signal" : "",
    }
    
    def __init__(self, scribblesdir, deckdir, email):
        super(Decks, self).__init__()
        self.scribblesdir = scribblesdir
        self.deckdir = deckdir
        self.email = email
    
    def shutdown(self):
       """Return 0 if a shutdown message is received, else return 1."""
       if self.dataReady("control"):
           msg=self.recv("control")
           if isinstance(msg,producerFinished) or isinstance(msg,shutdownMicroprocess):
               self.send(producerFinished(self),"signal")
               return 0
       return 1

    def main(self):
        while self.shutdown():
            while self.dataReady("fromEmail"):
                status = self.recv("fromEmail")
                if status == "sent":
                    self.send(". Deck e-mailed successfully","toTicker")
                else:
                    self.send(". Error sending deck by e-mail: " + status,"toTicker")
            while self.dataReady("inbox"):
                cmd = self.recv("inbox")
                if isinstance(cmd,list):
                    if (cmd[0] == "delete"):
                        self.deleteslide(cmd[1])
                else:
                    self.handleCommand(cmd)
#                yield 1
#            self.pause()
#            yield 1
            time.sleep(0.1)
                
    def fixNumbering(self):
        exists = 1
        slides = os.listdir(self.scribblesdir)
        slides.sort()
        for x in slides:
            if x == "slide." + str(exists) + ".png":
                # This slide exists, skip to next one
                pass
            else:
                # This slide doesn't exist, find the next one up and copy it down
                try:
                    shutil.move(self.scribblesdir + "/" + x,self.scribblesdir + "/slide." + str(exists) + ".png")
                except Exception:
                    e = sys.exc_info()[1]
                    sys.stderr.write("Failed to renumber slides. There may be an error in the sequence")
                    sys.stderr.write(str(e))
            exists += 1
                
    def handleCommand(self, cmd):
        cmd = cmd.upper()
        if cmd=="LOADDECK":
            self.loaddeck()
        elif cmd=="SAVEDECK":
            self.savedeck()
        elif cmd=="CLEARSCRIBBLES":
            self.clearscribbles()
        elif cmd== "QUIT":
            self.quit()
    
    def loaddeck(self):
        root = Tk()
        root.withdraw()
        filename = askopenfilename(filetypes=[("Zip Archives",".zip")],initialdir=self.deckdir,title="Load Slide Deck",parent=root)
        root.destroy()
        if filename != "":
            root = Tk()
            root.withdraw()
            password = askstring("Deck Password","Please enter the password for this zip file, or press cancel if you believe there isn't one:", parent=root)
            root.destroy()
            if filename:
                try:
                    unzipped = ZipFile(filename)
                    self.clearscribbles()
                    if password != None:
                        unzipped.extractall(path=self.scribblesdir,pwd=password)
                    else:
                        unzipped.extractall(path=self.scribblesdir,pwd="")
                    num_pages = 0
                    for x in os.listdir(self.scribblesdir):
                        if (os.path.splitext(x)[1] == ".png"):
                            num_pages += 1
                    self.send(["first",num_pages], "toSequencer")
                    self.send(chr(0) + "CLRTKR", "toTicker")
                    self.send("Deck loaded successfully","toTicker")
                except Exception:
                    e = sys.exc_info()[1]
                    self.send(chr(0) + "CLRTKR", "toTicker")
                    self.send("Failed to open the deck specified. You may have entered the password incorrectly","toTicker")

    def savedeck(self):
        num_pages = 0
        for x in os.listdir(self.scribblesdir):
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
                        os.system("zip -j -q -P " + password + " " + self.deckdir + "/" + filename + " " + self.scribblesdir + "/*.png")
                        self.send(chr(0) + "CLRTKR", "toTicker")
                        self.send("Zip file '" + filename + "' created successfully with password","toTicker")
                        success = True
                    except Exception:
                        e = sys.exc_info()[1]
                        self.send(chr(0) + "CLRTKR", "toTicker")
                        self.send("Failed to write to zip file '" + filename + "'","toTicker")
            else:
                try:
                    os.system("zip -j -q " + self.deckdir + "/" + filename + " " + self.scribblesdir + "/*.png")
                    self.send(chr(0) + "CLRTKR", "toTicker")
                    self.send("Zip file '" + filename + "' created successfully without password","toTicker")
                    success = True
                except Exception:
                    e = sys.exc_info()[1]
                    self.send(chr(0) + "CLRTKR", "toTicker")
                    self.send("Failed to write to zip file '" + filename + "'","toTicker")

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
                        self.send([address,"Whiteboard Deck " + filename,body,[self.deckdir + "/" + filename]], "toEmail")

                root.destroy()
        else:
            self.send(chr(0) + "CLRTKR", "toTicker")
            self.send("Save failed: No slides appear to exist","toTicker")
        
    def clearscribbles(self):
        try:
            for x in os.listdir(self.scribblesdir):
                if os.path.splitext(x)[1] == ".png":
                    os.remove(self.scribblesdir + "/" + x)
            self.send([["clear"]], "toCanvas")
            self.send("reset", "toSequencer")
        except Exception:
            e = sys.exc_info()[1]
            sys.stderr.write("Failed to clear scribbles - couldn't remove " + str(self.scribblesdir + "/" + x))
        
    def deleteslide(self,current):
        try:
            os.remove(self.scribblesdir + "/slide." + str(current) + ".png")
        except Exception:
            e = sys.exc_info()[1]
            sys.stderr.write("Error deleting slide " + str(current))
        self.fixNumbering()
        self.send("loadsafe","toSequencer")
    
    def quit(self):
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
