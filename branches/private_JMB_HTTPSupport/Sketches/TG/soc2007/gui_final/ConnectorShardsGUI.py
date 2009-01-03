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
from ConnectorShardPanel import ConnectorShardPanel

import Tkinter

from ShardGen import shardGen

class ConnectorShardsGUI(TkWindow):
    """
    Dialogue box that displays the list of classes it is given in a drop down
    menu. Information each class are shown when selected, see
    ConnectorShardPanel for details. Used by the ShardComposeGUI to
    display and configure the shard connector classes available.
    Sending a ['SELECT', 'NODE', <shardGen object>] message to its inbox
    will cause that object's details to be displayed.
    
    TODO: update menu button field on SELECT
    """

    def __init__(self, classes):
        self.selectedComponent = None
        self.uid = 1
        self.classes = classes
        super(ConnectorShardsGUI, self).__init__()

    def setupWindow(self):
        self.window.title("Connector Shards")

        self.addframe = Tkinter.Frame(self.window, borderwidth=2, relief=Tkinter.GROOVE)
        self.addframe.grid(row=0, column=0, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S, padx=4, pady=4)
        
        def menuCallback(index, text):
            self.click_menuChoice(shardGen(lookup[text]))
        
        lookup = {}
        for theclass in self.classes:
            lookup[theclass.__name__] = theclass
        
        items = list(lookup.keys())
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
        
        self.click_menuChoice(shardGen(lookup[items[0]]))

        self.addbutton = Tkinter.Button(self.addframe, text="ADD Shard", command=self.click_addComponent )
        self.addbutton.grid(row=2, column=0, columnspan=2, sticky=Tkinter.S)
        self.addframe.rowconfigure(1, weight=1)
        self.addframe.columnconfigure(0, weight=1)
        
        self.updatebutton = Tkinter.Button(self.addframe, text="Update Shard", command=self.click_update)
        self.updatebutton.grid(row=3, column=0, columnspan=2, sticky=Tkinter.S)

        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        self.window.protocol("WM_DELETE_WINDOW", self.handleCloseWindowRequest )


    def main(self):
        while not self.isDestroyed():
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                if data[0].upper() == "SELECT":
                    if data[1].upper() == "NODE":
                        self.componentSelected(data[2])
                                        
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
        
    def componentSelected(self, component):
        self.selectedComponent = component
        self.click_menuChoice(component)
    
    def click_update(self):
        self.argPanel.update()
    
    def click_addComponent(self):
        node, name = self.argPanel.getDef()
        self.send(("ADD", node, name),"outbox")

    def click_menuChoice(self, shgen):
        if self.argPanel != None:
            self.argPanel.destroy()
        
        self.argPanel = ConnectorShardPanel(self.argCanvas, shgen)
        self.argPanel.update_idletasks()
        self.argCanvas.itemconfigure(self.argCanvasWID, window=self.argPanel)
        self.argCanvas['scrollregion'] = self.argCanvas.bbox("all")
        self.argPanel.focus_force() #doesn't work :(


if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline

    import Shard
    import LoopShard
    import ComponentShard
    
    # subset for testing
    items = [Shard.shard, Shard.docShard, LoopShard.forShard,
                  LoopShard.whileShard, ComponentShard.componentShard]
    Pipeline(
       ConnectorShardsGUI(items),
    ).run()

