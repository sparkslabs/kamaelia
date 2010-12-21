#!/usr/bin/env python
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
==================
General Interactor
==================

This component implements the basic functionality of an Interactor. An
Interactor listens to events of another component and tranlates them
into movement which is applied to the target component. It provides
methods to be overridden for adding functionality.

Example Usage
-------------
A very simple Interactor could look like this::

    class VerySimpleInteractor(Interactor):
        def makeInteractorLinkages(self):
            self.link( (self,"outbox"), (self.target, "rel_rotation") )
        
        def setup(self):
            self.addListenEvents([pygame.MOUSEBUTTONDOWN])
        
        def handleEvents(self):
            while self.dataReady("events"):
                event = self.recv("events")
                if self.identifier in event.hitobjects:
                    self.send((0,90,0))
            

For examples of how to create Interactors have a look at the files
XXXInteractor.py.

A MatchedInteractor and a RotationInteractor each interacting with a
SimpleCube::

    CUBE1 = SimpleCube(size=(1,1,1), position=(1,0,0)).activate()
    CUBE2 = SimpleCube(size=(1,1,1), position=(-1,0,0)).activate()
    INTERACTOR1 = MatchedTranslationInteractor(target=CUBE1).activate()
    INTERACTOR2 = SimpleRotationInteractor(target=CUBE2).activate()
    
    Axon.Scheduler.scheduler.run.runThreads()  

How does it work?
-----------------
Interactor provides functionality for interaction with the OpenGL
display service and OpenGL components. It is designed to be subclassed.
The following methods are provided to be overridden:

- makeInteractorLinkages() -- make linkages to and from targets needed
- setup()                  -- set up the component
- handleEvents()           -- handle input events ("events" inbox)
- frame()                  -- called every frame, to add additional functionality

Stubs method are provided, so missing these out does not result in
broken code. The methods get called from the main method, the following
code shows in which order::

    def main(self):
        # create and send eventspy request
        ...
        # setup function from derived objects
        self.setup()        
        ...
        while 1:
            yield 1
            # handle events function from derived objects
            self.handleEvents()
            # frame function from derived objects
            self.frame()

If you need to override the __init__() method, e.g. to get
initialisation parameters, make sure to pass on all keyword arguments to
__init__(...) of the superclass, e.g.::

    def __init__(self, **argd):
        super(ClassName, self).__init__(**argd)
        # get an initialisation parameter
        myparam = argd.get("myparam", defaultvalue)
        
The following methods are provided to be used by inherited objects:

- addListenEvents(list of events) -- Request reception of a list of events
- removeListenEvents(list of events) -- Stop reveiving events

The are inteded to simplify component handling. For their functionality
see their description.

The event identifier of the target component gets saved in
self.identifier. Use this variable in event handling to determine if the
target component has been hit.

Interactor components terminate if a producerFinished or
shutdownMicroprocess message is received on their "control" inbox. The
received message is also forwarded to the "signal" outbox. Upon
termination, this component does *not* unbind itself from the
OpenGLDisplay service and does not free any requested resources.

"""


import pygame
from pygame.locals import *
from OpenGLDisplay import *

import Axon

class Interactor(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    """\
    Interactor(...) -> A new Interactor object (not very useful, designed to be subclassed)
    
    This component implements the basic functionality of an Interactor. An
    Interactor listens to events of another component and tranlates them
    into movement which is applied to the target component. It provides
    methods to be overridden for adding functionality.
    
    Keyword arguments:
    
    - target    -- OpenGL component to interact with
    - nolink    -- if True, no linkages are made (default=False)
    """
    
    Inboxes = {
        "inbox"      : "not used",
        "control"    : "For shutdown messages",
        "events"     : "Input events",
        "callback"   : "for the response after a displayrequest",
    }
    
    Outboxes = {
        "outbox"        : "used for sending relative tranlational movement",
        "signal"        : "For shutdown messages",
        "display_signal": "Outbox used for communicating to the display surface",
    }
    
    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Interactor, self).__init__()

        # get display service
        displayservice = OpenGLDisplay.getDisplayService()
        # link display_signal to displayservice
        self.link((self,"display_signal"), displayservice)
       
        self.target = argd.get("target")
        
        self.nolink = argd.get("nolink", False)
                    
            
    def main(self):
        # create eventspy request
        self.eventspyrequest = { "EVENTSPYREQUEST" : True,
                                                   "objectid" : id(self),
                                                   "target": id(self.target),
                                                   "callback" : (self,"callback"),
                                                   "events" : (self, "events")  }
    
        # send display request
        self.send(self.eventspyrequest, "display_signal")

        # setup function from derived objects
        self.setup()        

        # wait for response on displayrequest
        while not self.dataReady("callback"): yield 1
        self.identifier = self.recv("callback")

        while 1:
            yield 1

            while self.dataReady("control"):
                cmsg = self.recv("control")
                if isinstance(cmsg, producerFinished) or isinstance(cmsg, shutdownMicroprocess):
                    self.send(cmsg, "signal")
                    return

            # handle events function from derived objects
            self.handleEvents()
            # frame function from derived objects
            self.frame()

    ##
    # Methods to be used by derived objects
    ##

    def addListenEvents(self, events):
        """\
        Sends listening request for pygame events to the display service.
        The events parameter is expected to be a list of pygame event constants.
        """
        for event in events:
            self.send({"ADDLISTENEVENT":event, "objectid":id(self)}, "display_signal")

    
    def removeListenEvents(self, events):
        """\
        Sends stop listening request for pygame events to the display service.
        The events parameter is expected to be a list of pygame event constants.
        """
        for event in events:
            self.send({"REMOVELISTENEVENT":event, "objectid":id(self)}, "display_signal")


    ##
    # Method stubs to be overridden by derived objects
    ##
    def makeInteractorLinkages(self):
        """ Method stub """
        pass


    def handleEvents(self):
        """
        Method stub
        
        Override this method to do event handling inside.
        Should look like this::

            while self.dataReady("events"):
                event = self.recv("events")
                # handle event ...
        
        """
        pass        
    
    def setup(self):
        """
        Method stub
        
        Override this method for component setup.
        It will be called on the first scheduling of the component.
        """
        pass

    def frame(self):
        """
        Method stub
        
        Override this method for operations you want to do every frame.
        It will be called every time the component is scheduled. Do not
        include infinite loops, the method has to return every time it
        gets called.
        """
        pass

__kamaelia_components__ = ( Interactor, )


# Licensed to the BBC under a Contributor Agreement: THF
