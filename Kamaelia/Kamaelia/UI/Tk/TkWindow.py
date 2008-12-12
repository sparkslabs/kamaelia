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
"""\
===========================
Simple Tk Window base class
===========================

A simple component providing a framework for having a Tk window as a component.

TkInvisibleWindow is a simple implementation of an invisible (hidden) Tk window,
useful if you want none of the visible windows to be the Tk root window.



Example Usage
-------------

Three Tk windows, one with "Hello world" written in it::
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

    root = TkWindow().activate()          # first window created is the root
    win2 = MyWindow("MyWindow","Hello world!").activate()
    
    scheduler.run.runThreads(slowmo=0)



How does it work?
-----------------

This component provides basic integration for Tk. It creates and sets up a Tk
window widget, and then provides a kamaelia main loop that ensures Tk's own
event processing loop is regularly called.

self.window contains the Tk window widget.

To set up your own widgets and event handling bindings for the window,
reimplement the setupWindow() method.

NOTE: Do not bind the "<Destroy>" event as this is already handled. Instead,
reimplement the destroyHandler() method. This is guaranteed to only be called if
the destroy event is for this specific window.

The first window instantiated is the Tk "root" window. Note that closing this
window will result in Tk trying to close down. To avoid this style of behaviour,
create a TkInvisibleWindow as the root.

The existing main() method ensures Tk's event processing loop is regularly
called.

You can reimplement main(). However, you must ensure you include the existing
functionality:
- regularly calling tkupdate() to ensure Tk gets to process its own events
- calls self.window.destroy() method to destroy the window upon shutdown.
- finishes if self.isDestroyed() returns True

The existing main() method will cause the component to terminate if a
producerFinished or shutdownMicroprocess message is received on the "control"
inbox. It sends the message on out of the "signal" outbox and calls
self.window.destroy() to ensure the window is destroyed.

NOTE: main() must not ask to be paused as it calls the Tk event loop. If the
Tk event loop is not called, then a Tk app will freeze and be unable to respond
to events.

NOTE: Event bindings are called from within Tk event handling. If, for example,
there are two (or more) TkWindow instances, then a given event handler could be
called whilst the thread of execution is actually within the other TkWindow
component's main() method. This is a bit messy. It will not cause problems in
a single threaded system, but may be an issue once Axon/Kamaelia is able to
distribute across multiple processors.



Development History
-------------------
Started as a first hash attempt at some components to incorporate Tkinter into
Kamaelia in cvs:/Sketches/tk/tkInterComponents.py

Turned out to be remarkably resilient so far, so migrated into the main codebase.
"""

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#
# XXX TODO - various improvements (Michael Sparks)
#
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

import Tkinter
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class TkWindow(component):
    """\
    TkWindow() -> new TkWindow component

    A component providing a Tk window. The first TkWindow created will be the
    "root" window.

    Subclass to implement your own widgets and functionality on the window.
    """
    
    tkroot = None # class variable containing the tk 'root'

    
    def __init__(self):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
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
        """\
        Populate the window with widgets, set its title, set up event bindings etc...

        Do not bind the "<Destroy>" event, as this is already handled.
        
        Stub method. Reimplement with your own functionality.
        """
        self.frame = Tkinter.Frame(self.window)

        self.window.title("TkWindow "+str(self.id))
        
        self.frame.grid(row=0, column=0, sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S)
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        
    def isDestroyed(self):
        """Returns true if this window has been destroyed"""
        return self._destroyed

    
    def main(self):
        """
        Main loop. Stub method, reimplement with your own functionality.

        Must regularly call self.tkupdate() to ensure tk event processing happens.
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
        """\
        Calls tk's event processing loop (if this is the root window).

        To be called from within self.main().
        """
        if TkWindow.tkroot == self.window:
            if not self.isDestroyed():
                self.window.update()


    def __destroyHandler(self, event):
        """Handler for destroy event. Do not override."""
        if str(event.widget) == str(self.window): # comparing widget path names, not sufficient to just compare widgets for some reason
            self._destroyed = True
        self.destroyHandler(event)
        
        
    def destroyHandler(self,event):
        """Stub method. Reimplement with your own functionality to respond to a tk window destroy event."""
        pass
    


class tkInvisibleWindow(TkWindow):
    """\
    tkInvisibleWindow() -> new tkInvisibleWindow component.

    An invisible, empty tk window. Can use as a 'root' window, thereby ensuring
    closing any (visible) window doesn't terminate Tk (closing the root does).
    """
    def setupWindow(self):
        """Sets up and hides the window."""
        super(tkInvisibleWindow,self).setupWindow()
        self.window.withdraw()

__kamaelia_components__  = ( TkWindow, tkInvisibleWindow, )

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
    