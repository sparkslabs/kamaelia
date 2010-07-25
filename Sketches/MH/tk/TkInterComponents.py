#!/usr/bin/python
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
    