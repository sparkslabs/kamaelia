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

import Tkinter

class TextOutputGUI(TkWindow):
    """
    Simple text display box. Used by the ShardCompose GUI for displaying
    generated code and the file to which it was written
    """

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
                    if data[0] == 'text':
                        if data[1] == None:
                            self.allreceived = True
                        else:
                            self.textbox.insert(Tkinter.END, data[1])
                
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


if __name__ == '__main__':
    TextOutputGUI('title').run()