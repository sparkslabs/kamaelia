#!/usr/bin/python
#
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
#
# a first hash attempt at some components to incorporate Tkinter into Kamaelia

import Tkinter
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess


class TkWindow(component):
    """Tk window component. Subclass and override methods to customise

       The first one of these instantiated (in the order of execution of your app) will be
       the 'root'

       Do not replace the bound handler for the 'Destroy' event, instead override self.destroyHandler()
    """
    
    tkroot = None # class variable containing the tk 'root'

    
    def __init__(self):
        super(TkWindow, self).__init__()

        # create root/toplevel window
        if not TkWindow.tkroot:
            TkWindow.tkroot = Tkinter.Tk()
            self.window = TkWindow.tkroot
        else:
            self.window = Tkinter.Toplevel()

        self._destroyed = False
        self.window.bind("<Destroy>", self.__destroyHandler)
        self.setupWindow()

    def setupWindow(self):
        """Stub method, override with your own.
           Populate the window with widgets, set its title, set up any event bindings you need etc."""
        self.frame = Tkinter.Frame(self.window)

        self.window.title("TkWindow "+str(self.id))
        
        self.frame.grid(row=0, column=0, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        
    def isDestroyed(self):
        """Returns true if this window has been destroyed"""
        return self._destroyed

    
    def main(self):
        """Stub method, override with your own.

           main kamaelia loop, must regularly call self.tkupdate() to ensure tk event processing happens.

           default implementation terminates when the window is destroyed, and destroys the window in
           response to producerFinished or shutdownMicroprocess messages on the contorl inbox
        """

        while not self.isDestroyed():
            yield 1
            if self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                    self.send(msg, "signal")
                    self.window.destroy()
            self.tkupdate()

    def tkupdate(self):
        """Calls tk's event processing loop (if this is the root window).
           ONLY CALL FROM WITHIN main()
        """
        if TkWindow.tkroot == self.window:
            if not self.isDestroyed():
                self.window.update()


    def __destroyHandler(self, event):
        """Do not override. Handler for destroy event"""
        if str(event.widget) == str(self.window): # comparing widget path names, not sufficient to just compare widgets for some reason
            self._destroyed = True
        self.destroyHandler(event)
        
        
    def destroyHandler(self,event):
        """Stub method. Override"""
        pass
    


class tkInvisibleWindow(TkWindow):
    def setupWindow(self):
        super(tkInvisibleWindow,self).setupWindow()
        self.window.withdraw()


if __name__ == "__main__":
    from Axon.Scheduler import scheduler

    class MyWindow(TkWindow):
        def __init__(self, title, text):
            self.title = title
            self.text  = text
            super(MyWindow,self).__init__()

        def setupWindow(self):
            self.label = Tkinter.Label(self.window, text=self.text)
    
            self.window.title(self.title)
            
            self.label.grid(row=0, column=0, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)
            self.window.rowconfigure(0, weight=1)
            self.window.columnconfigure(0, weight=1)

    root = TkWindow().activate()
    win = TkWindow().activate()
    my = MyWindow("MyWindow","Hello world!").activate()
    
    scheduler.run.runThreads(slowmo=0)
    