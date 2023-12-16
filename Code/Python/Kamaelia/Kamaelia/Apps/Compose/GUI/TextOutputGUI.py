#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from Kamaelia.UI.Tk.TkWindow import TkWindow
from Kamaelia.Support.Tk.Scrolling import ScrollingMenu
from Axon.Ipc import producerFinished, shutdownMicroprocess

import tkinter as Tkinter

class TextOutputGUI(TkWindow):

    def __init__(self, title):
        self.title = title
        self.allreceived = True
        super(TextOutputGUI, self).__init__()

    def setupWindow(self):
        self.textbox = Tkinter.Text(self.window, cnf={"state":Tkinter.DISABLED} )

        self.window.title(self.title)
        
        self.textbox.grid(row=0, column=0, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        self.window.protocol("WM_DELETE_WINDOW", self.handleCloseWindowRequest )

    def main(self):

        while not self.isDestroyed():

            if self.dataReady("inbox"):
                self.textbox.config(state=Tkinter.NORMAL)        # enable editing
                
                if self.allreceived:
                    self.allreceived = False
                    self.textbox.delete(1.0, Tkinter.END)
                while self.dataReady("inbox"):
                    data = self.recv("inbox")
                    if data == None:
                        self.allreceived = True
                    else:
                        self.textbox.insert(Tkinter.END, data)
                
                self.textbox.config(state=Tkinter.DISABLED)     # disable editing
                        
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                    self.send(msg, "signal")
                    self.window.destroy()

            self.tkupdate()
            yield 1

    def handleCloseWindowRequest(self):
        self.send( shutdownMicroprocess(self), "signal")
        self.window.destroy()

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    import Axon
    import time
    class Source(Axon.Component.component):
        "A simple data source"
        def __init__(self, data=None):
            super(Source, self).__init__()
            if data == None: data = []
            self.data = data

        def main(self):
            for item in iter(self.data):
                self.send(item, "outbox")
                yield 1

    class TimedPassthrough(Axon.ThreadedComponent.threadedcomponent):
        def __init__(self, delay=1):
            super(TimedPassthrough, self).__init__()
            self.delay = delay
        def main(self):
            while 1:
                 time.sleep(self.delay)
                 if self.dataReady("inbox"):
                     data = self.recv("inbox")
                     self.send(data, "outbox")

    Pipeline(
        Source(["H\n", None, # None says "We're done. Anything you recieve after this replaces this text"
                "Hel\n", None,
                "Hello \n", None,
                "Hello Wo\n", None,
                "Hello World\n",
        ]),
        TimedPassthrough(0.1),
        TextOutputGUI("Basic Display"),
    ).run()





