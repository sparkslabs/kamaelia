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
from ArgumentsPanel import ArgumentsPanel
import Tkinter
import pprint

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
                    # Oh it's viewed here as a hack because it's a closure
        self.window.title("Pipeline Builder")

        self.addframe = Tkinter.Frame(self.window, borderwidth=2, relief=Tkinter.GROOVE)
        self.addframe.grid(row=0, column=0, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S, padx=4, pady=4)
        
        def menuCallback(index, text):
            self.click_menuChoice(lookup[text])

#        print self.classes[0]
        for theclass in self.classes:
#            print "THECLASS"
#            pprint.pprint(theclass)
#            print "SSALCEHT"
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
        
        self.delbutton = Tkinter.Button(self.remframe, text="REMOVE Component/Links", command=self.click_removeComponent )
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

"""
When the "ADD component" button is clicked, emit a message of the form:
   * ("ADD", c['id'], c['name'], c, self.selectedComponent)
   * Out the outbox

This declares a unique component id, with a unique name, along with a definition consisting
of:
def getDef(self):
        return { "name"          : self.theclass['class'],
                 "module"        : self.theclass['module'],
                 "instantiation" : self.getInstantiation()
               }

When the "remove component" button is clicked, emit
   *  a ("DEL", self.selectedComponent) message
   * out the outbox "outbox"

Specifically this says "delete the currently selected component"
"""

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    import Axon
    import pprint
     
    def getAllClasses( modules ):
        _modules = list(modules.keys())
        _modules.sort()
        for modname in _modules:
            try:
                for entry in getModuleConstructorArgs( modname, modules[modname] ):
                    yield entry
            except ImportError:
                print "WARNING: Import Error: ", modname
                continue
    
    def getModuleConstructorArgs( modulename, classnames):
        clist = []
    
        module = __import__(modulename, [], [], classnames)
        for classname in classnames:
            theclass = eval("module."+classname)
    
            entry = { "module"   : modulename,
                    "class"    : classname,
                    "classdoc" : theclass.__doc__,
                    "initdoc"  : theclass.__init__.__doc__,
                    "args"     : getConstructorArgs(theclass),
                    "theclass" : theclass,
                    }
    
            clist.append(entry)
    
        return clist
    
    def getConstructorArgs(component):
        initfunc = eval("component.__init__")
        try:
            (args, vargs, vargkw, defaults) = inspect.getargspec(initfunc)
        except TypeError, e:
            print "FAILURE", str(component), repr(component), component
            raise e
    
        arglist = [ [arg] for arg in args ]
        if defaults is not None:
            for i in range(0,len(defaults)):
                arglist[-1-i].append( repr(defaults[-1-i]) )
    
        del arglist[0]   # remove 'self'
        
        return {"std":arglist, "*":vargs, "**":vargkw}

    import inspect
    # subset for testing
    COMPONENTS = { 'Kamaelia.File.ReadFileAdaptor': ['ReadFileAdaptor'],
                   'Kamaelia.File.Reading': ['PromptedFileReader'],
                   'Kamaelia.Codec.Dirac': ['DiracDecoder', 'DiracEncoder'],
                   'Kamaelia.UI.Pygame.VideoOverlay': ['VideoOverlay'],
                   'Kamaelia.File.UnixProcess': ['UnixProcess'],
                   'Kamaelia.File.Writing': ['SimpleFileWriter']
                 }

    class PrettyPrinter(Axon.Component.component):
        def main(self):
            while 1:
                while self.dataReady("inbox"):
                    data = self.recv("inbox")
                    print "-------------------------------------------------------------------"
                    pprint.pprint(data)
                yield 1
    
    items = list(getAllClasses( COMPONENTS ))
    Pipeline(
       BuilderControlsGUI(items),
       PrettyPrinter()
    ).run()

