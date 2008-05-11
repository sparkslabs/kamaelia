#!/usr/bin/env python

# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
from Axon.Ipc import producerFinished, shutdownMicroprocess

import Tkinter
import re

class ComponentEditor(TkWindow):
    """\
    This component provides a tk textbox for describing how to instantiate a component.
    
    it can be updated with details from elsewhere by sending it an:
        ("UPDATE_NAME", "NODE", id, "import:class(arguments)")
    
    if it sees a ("SELECT","NODE", id) message, this component will send its own ("GET_NAME",...)
    message out of the "topocontrol" outbox
    
    sending a ("GET_NAME", "NODE", id) message will cause to emit an UPDATE_NAME message
    for the specified id, using the details as entered by the user
    """
    
    Inboxes = { "inbox" : "receives updates, instructions to emit",
                "control" : "",
              }
    Outboxes =  { "outbox" : 'emits ("UPDATE_NAME", id, "NODE", "newname") messages',
                  "topocontrol" : 'for querying a topology viewer',
                  "signal" : "",
                }
    
    def __init__(self, classes):
        self.classes = classes
        super(ComponentEditor, self).__init__()
        
    def setupWindow(self):
        self.window.title("Component Editor")

        self.choosebutton = Tkinter.Button(self.window, text="<<no component>>", command=self.click_chooseComponent )
        self.choosebutton.grid(row=0, column=0, sticky=Tkinter.W+Tkinter.E)
        
        self.label1 = Tkinter.Label(self.window, text=" ( ")
        self.label1.grid(row=0, column=1, sticky=Tkinter.W+Tkinter.E)
        
        self.argsvar = Tkinter.StringVar()
        self.args = Tkinter.Entry(self.window, bg="white", textvariable=self.argsvar, takefocus=1)
        self.argsvar.set("")
        self.args.grid(row=0,column=2, sticky=Tkinter.W+Tkinter.E)

        self.label2 = Tkinter.Label(self.window, text=" ) ")
        self.label2.grid(row=0, column=3, sticky=Tkinter.W+Tkinter.E)

#        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(2, weight=2)
        self.window.grid()

        self.window.protocol("WM_DELETE_WINDOW", self.handleCloseWindowRequest )
        
        
        
    def main(self):
        self.nodeEditable=False
        self.click_menuChoice(self.classes[0])
        selectedId = None

        while not self.isDestroyed():

            if self.dataReady("inbox"):
                data = self.recv("inbox")
                
                if (data[0], data[1]) == ("SELECT", "NODE"):
                    if data[2] != None:
                        self.send( ("GET_NAME", "NODE", data[2]), "topocontrol")      # find out about the selected node
                        
                if (data[0], data[1]) == ("UPDATE_NAME", "NODE"):
                    if self.componentSelected(data[3]):   # (ignore the ID)
                        selectedId = data[2]
                    else:
                        selectedId = None
                    
                if (data[0], data[1]) == ("GET_NAME", "NODE"):
                    if selectedId == data[2]:
                        self.send( ("UPDATE_NAME", "NODE", data[2], self.getInstantiation()), "outbox")
                                        
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

        
    def componentSelected(self, spec):
        match = re.match(r"^([*+]?)([^:]*)\:([^(]+)\((.*)\)$", spec)
        if match:
            (_, modulename, classname, arguments) = match.groups()
            for theclass in self.classes:
                if theclass['module'] == modulename and theclass['class'] == classname:
                    self.click_menuChoice(theclass, arguments=arguments)
                    return True   # node was successfully parsed, so is editable
        return False
        

    def click_chooseComponent(self):
        self.menu = Tkinter.Menu(self.window, tearoff=0)
        for theclass in self.classes:
            self.menu.add_command( label=theclass['module']+"."+theclass['class'],
                                   command=lambda it=theclass: self.click_menuChoice(it)
                                 )
        self.menu.post(self.choosebutton.winfo_rootx(),
                       self.choosebutton.winfo_rooty() + self.choosebutton.winfo_height())

    def click_menuChoice(self, theclass, arguments=None):
        self.choosebutton['text'] = theclass['module']+"."+theclass['class']
        if not arguments:
            arguments = theclass['defaults']
        self.argsvar.set(arguments)
        self.currentclass = theclass

    def getInstantiation(self):
        return self.currentclass['module'] + ":" + self.currentclass['class'] + "(" + self.argsvar.get() + ")"
            
