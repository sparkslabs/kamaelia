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
from ImportShardPanel import ImportShardPanel
import Tkinter
import pprint
from glom import glomfrompath

class ImportShardsGUI(TkWindow):

    def __init__(self, path):
        self.selectedComponent = None
        self.uid = 1
        self.functions = glomfrompath(path)
        super(ImportShardsGUI, self).__init__()

    def setupWindow(self):
        items = []
        lookup = {} # This is a bit of a nasty hack really ... :-)
                    # Why is this a hack ?
                    # Oh it's viewed here as a hack because it's a closure
        self.window.title("Shard Builder")

        self.addframe = Tkinter.Frame(self.window, borderwidth=2, relief=Tkinter.GROOVE)
        self.addframe.grid(row=0, column=0, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S, padx=4, pady=4)
        
        # called when item selected from function list
        def menuCallback(index, text):
            self.click_menuChoice(self.getname(text), self.functions[text])
        
        items = list(self.functions.keys())
        
        self.choosebutton = ScrollingMenu(self.addframe, items,
                                          command = menuCallback)
        self.choosebutton.grid(row=0, column=0, columnspan=2, sticky=Tkinter.N)

        self.argPanel = None
        self.argCanvas = Tkinter.Canvas(self.addframe, relief=Tkinter.SUNKEN, borderwidth=2)
        self.argCanvas.grid(row=1, column=0, sticky=Tkinter.N+Tkinter.S+Tkinter.E+Tkinter.W)
        self.argCanvasWID = self.argCanvas.create_window(0,0, anchor=Tkinter.NW)
        self.argCanvasScroll = Tkinter.Scrollbar(self.addframe, orient=Tkinter.VERTICAL)
        self.argCanvasScroll.grid(row=1, column=1, sticky=Tkinter.N+Tkinter.S+Tkinter.E)
        self.argCanvasScroll['command'] = self.argCanvas.yview
        self.argCanvas['yscrollcommand'] = self.argCanvasScroll.set
        
        self.click_menuChoice(self.getname(items[0]), self.functions[items[0]])

        self.addbutton = Tkinter.Button(self.addframe, text="ADD Shard", command=self.click_addComponent)
        self.addbutton.grid(row=2, column=0, columnspan=2, sticky=Tkinter.S)
        self.addframe.rowconfigure(1, weight=1)
        self.addframe.columnconfigure(0, weight=1)
        
        # just adds component same atm.
        self.inlinebutton = Tkinter.Button(self.addframe, text="ADD Inline Shard", command=self.click_addInline)
        self.inlinebutton.grid(row=3, column=0, columnspan=2, sticky=Tkinter.S)

        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        self.window.protocol("WM_DELETE_WINDOW", self.handleCloseWindowRequest )


    def main(self):
        while not self.isDestroyed():
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                    self.send(msg, "signal")
                    self.window.destroy()
                    
            self.tkupdate()
            yield 1

    def handleCloseWindowRequest(self):
        self.send( shutdownMicroprocess(self), "signal")
        self.window.destroy()
    
    def getname(self, fname):
        return fname.split(':')[1].lstrip()

    def click_addComponent(self):
        node, name = self.argPanel.getDef()
        self.send(("ADD", node, name),"outbox")
    
    def click_addInline(self):
        node, name = self.argPanel.getInlineDef()
        self.send(("ADD", node, name),"outbox")
    
    def click_menuChoice(self, fname, fcode):
        if self.argPanel != None:
            self.argPanel.destroy()
        
        self.argPanel = ImportShardPanel(self.argCanvas, fname, fcode)
        self.argPanel.update_idletasks()
        self.argCanvas.itemconfigure(self.argCanvasWID, window=self.argPanel)
        self.argCanvas['scrollregion'] = self.argCanvas.bbox("all")


if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    
    Pipeline(
       ImportShardsGUI('/usr/lib/python2.5/site-packages/Kamaelia/Util'),
    ).run()

