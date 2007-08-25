#!/usr/bin/env python

# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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