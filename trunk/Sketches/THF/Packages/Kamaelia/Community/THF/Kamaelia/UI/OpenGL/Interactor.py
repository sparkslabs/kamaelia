#!/usr/bin/env python
#
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
"""\
=====================
General Interactor
=====================

This component implements the basic functionality of an Interactor. An
Interactor listens to events of another component and tranlates them
into movement which is applied to the victim component. It provides
methods to be overridden for adding functionality.

Example Usage
-------------

A very simple Interactor could look like this:

class VerySimpleInteractor(Interactor):
    def makeInteractorLinkages(self):
        self.link( (self,"outbox"), (self.victim, "rel_rotation") )
    
    def setup(self):
        self.addListenEvents([pygame.MOUSEBUTTONDOWN])
    
    def handleEvents(self):
        while self.dataReady("events"):
            event = self.recv("events")
            if self.identifier in event.hitobjects:
                self.send((0,90,0))
            

For examples of how to create Interactors have a look at the files
*Interactor.py.

A MatchedInteractor and a RotationInteractor each interacting with a
SimpleCube:

    CUBE1 = SimpleCube(size=(1,1,1), position=(1,0,0)).activate()
    CUBE2 = SimpleCube(size=(1,1,1), position=(-1,0,0)).activate()
    INTERACTOR1 = MatchedTranslationInteractor(victim=CUBE1).activate()
    INTERACTOR2 = SimpleRotationInteractor(victim=CUBE2).activate()
    
    Axon.Scheduler.scheduler.run.runThreads()  

How does it work?
-----------------

The following methods are provided to be overridden:
- makeInteractorLinkages() -- make linkages to and from victims needed
- setup()			       -- set up the component
- handleEvents()	       -- handle input events ("events" inbox)
- frame()			       -- called every frame, to add additional functionality

Stubs method are provided, so missing these out does not result in
broken code. The methods get called from the main method, the following
code shows in which order:

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
initialisation parameters, make sure to call the __init__() method of
the parent class in the following way:

    def __init__(self, **argd):
        super(ClassName, self).__init__(**argd)
        # get an initialisation parameter
        myparam = argd.get("myparam", defaultvalue)
        
The following methods are provided to be used by inherited objects:

- addListenEvents()
- removeListenEvents()        

The are inteded to simplify component handling. For their functionality
see their description.

The event identifier of the victim component gets saved in
self.identifier. Use this variable in event handling to determine if the
victim component has been hit.

"""


import pygame
from pygame.locals import *
from OpenGLDisplay import *

import Axon

class Interactor(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    """\
    Interactor specific constructor keyword arguments:
    - victim    -- OpenGL component to interact with
    - nolink    -- if True, no linkages are made (default=False)
    """
    
    Inboxes = {
        "inbox"      : "not used",
        "control"    : "ignored",
        "events"     : "Input events",
        "callback"   : "for the response after a displayrequest",
    }
    
    Outboxes = {
        "outbox"        : "used for sending relative tranlational movement",
        "display_signal": "Outbox used for communicating to the display surface",
    }
    
    def __init__(self, **argd):
        super(Interactor, self).__init__()

        # get display service
        displayservice = OpenGLDisplay.getDisplayService()
        # link display_signal to displayservice
        self.link((self,"display_signal"), displayservice)
       
        self.victim = argd.get("victim")
        
        self.nolink = argd.get("nolink", False)
                    
            
    def main(self):
        # create eventspy request
        self.eventspyrequest = { "EVENTSPYREQUEST" : True,
                                                   "objectid" : id(self),
                                                   "victim": id(self.victim),
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
        Should look like this:
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

