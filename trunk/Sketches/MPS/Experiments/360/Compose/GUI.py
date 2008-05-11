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
from Kamaelia.Support.Tk.Scrolling import ScrollingMenu
from Axon.Ipc import producerFinished, shutdownMicroprocess

import Tkinter


class ArgumentsPanel(Tkinter.Frame):
    def __init__(self, parent, theclass):
        Tkinter.Frame.__init__(self, parent)

        self.theclass = theclass

        # build widgets
        
        row=0
        if self.theclass['classdoc']:
            self.classdoclabel = Tkinter.Label(self, text = self.theclass['classdoc'], justify="left")
            self.classdoclabel['font'] = " ".join(self.classdoclabel['font'].split(" ")[0:2])
            self.classdoclabel.grid(row=row, column=0,columnspan=2,
                                    sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S, padx=4, pady=4)
            row+=1

        if self.theclass['initdoc']:
            self.initdoclabel = Tkinter.Label(self, text = self.theclass['initdoc'], justify="left")
            self.initdoclabel['font'] = " ".join(self.initdoclabel['font'].split(" ")[0:2])
            self.initdoclabel.grid(row=row, column=0, columnspan=2,
                                   sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S, padx=4, pady=4)
            row+=1

        self.label = Tkinter.Label(self, text="ARGUMENTS:")
        self.label.grid(row=row, column=0, columnspan=2,sticky=Tkinter.W+Tkinter.S, padx=4, pady=4)
        row+=1

        
        # enumerate std args
        self.args = []
        for arg in self.theclass['args']['std']:
            arglabel = Tkinter.Label(self, text=arg[0])
            arglabel.grid(row=row,column=0, sticky=Tkinter.E)

            svar = Tkinter.StringVar()
            argfield = Tkinter.Entry(self, bg="white", textvariable=svar, takefocus=1)
            default=""
            if len(arg)>=2:
                default = arg[1]
                svar.set(default)
            argfield.grid(row=row,column=1, sticky=Tkinter.W)
            
            self.args.append( (arg[0], svar, default) )
            row+=1


         # now do * and ** args
        for argname in ["*","**"]:
            if self.theclass['args'][argname]:
                arglabel = Tkinter.Label(self, text=argname)
                arglabel.grid(row=row,column=0, sticky=Tkinter.E)
                arglabel = None
                
                svar = Tkinter.StringVar()
                argfield = Tkinter.Entry(self, bg="white", textvariable=svar, takefocus=1)
                argfield.grid(row=row,column=1, sticky=Tkinter.W)
                
                self.args.append( (argname, svar, "") )
                row+=1
                
#        self.rowconfigure(row, weight=1)
#        self.grid()

        
    def getDef(self):
        return { "name"          : self.theclass['class'],
                 "module"        : self.theclass['module'],
                 "instantiation" : self.getInstantiation()
               }

                        
    def getInstantiation(self):
        """Return the instantiation string"""
        argstr = ""
        prefix = ""
        for (argname, svar, default) in self.args:
            text = svar.get().strip()
            default = default.strip()
            if argname != "*" and argname != "**":
                if default=="" or text != default:
                    if not text:
                        text = "<<unspecified>>"
                    argstr = argstr + prefix + argname + " = " + text
                    prefix=", "
            else:
                if text:
                    argstr = argstr + prefix + text
                    prefix=", "
        
        return argstr


            
class BuilderControlsGUI(TkWindow):

    def __init__(self, classes):
        self.selectedComponent = None
        self.uid = 1
        self.classes = classes
        super(BuilderControlsGUI, self).__init__()

    def setupWindow(self):
        items = []
        lookup = {} # This is a bit of a nasty hack really ... :-)
                    # Why is this a hack ?
        self.window.title("Pipeline Builder")

        self.addframe = Tkinter.Frame(self.window, borderwidth=2, relief=Tkinter.GROOVE)
        self.addframe.grid(row=0, column=0, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S, padx=4, pady=4)
        
        def menuCallback(index, text):
            self.click_menuChoice(lookup[text])

        print self.classes[0]
        for theclass in self.classes:
            lookup[ theclass['module']+"."+theclass['class'] ] = theclass
            items.append(theclass['module']+"."+theclass['class'])

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
        
        self.click_menuChoice(self.classes[1])

        self.addbutton = Tkinter.Button(self.addframe, text="ADD Component", command=self.click_addComponent )
        self.addbutton.grid(row=2, column=0, columnspan=2, sticky=Tkinter.S)
        self.addframe.rowconfigure(1, weight=1)
        self.addframe.columnconfigure(0, weight=1)
        
        self.remframe = Tkinter.Frame(self.window, borderwidth=2, relief=Tkinter.GROOVE)
        self.remframe.grid(row=1, column=0, columnspan=2, sticky=Tkinter.S+Tkinter.E+Tkinter.W, padx=4, pady=4)

        self.selectedlabel = Tkinter.Label(self.remframe, text="<no component selected>")
        self.selectedlabel.grid(row=0, column=0, sticky=Tkinter.S)
        
        self.delbutton = Tkinter.Button(self.remframe, text="REMOVE Component", command=self.click_removeComponent )
        self.delbutton.grid(row=1, column=0, sticky=Tkinter.S)
        self.delbutton.config(state=Tkinter.DISABLED)

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


    def makeUID(self):
        uid = self.uid
        self.uid += 1
        return uid
        
    def componentSelected(self, component):
        self.selectedComponent = component
        if component == None:
            self.delbutton.config(state=Tkinter.DISABLED)
            self.selectedlabel["text"] = "<no component selected>"
        else:
            self.delbutton.config(state=Tkinter.NORMAL)
            self.selectedlabel["text"] = repr(component[0])


    def click_addComponent(self):
        # add to the pipeline and wire it in
        
        c = self.argPanel.getDef()
        c["id"] = ( c['name'], repr(self.makeUID()) )
        msg = ("ADD", c['id'], c['name'], c, self.selectedComponent)
        self.send( msg, "outbox")
        

    def click_removeComponent(self):
        if self.selectedComponent:
            self.send( ("DEL", self.selectedComponent), "outbox")


    def click_chooseComponent(self):
        pass

    def click_menuChoice(self, theclass):
        if self.argPanel != None:
            self.argPanel.destroy()
        
        self.argPanel = ArgumentsPanel(self.argCanvas, theclass)
        self.argPanel.update_idletasks()
        self.argCanvas.itemconfigure(self.argCanvasWID, window=self.argPanel)
        self.argCanvas['scrollregion'] = self.argCanvas.bbox("all")


            
# -------------------------------------------------------------------

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


