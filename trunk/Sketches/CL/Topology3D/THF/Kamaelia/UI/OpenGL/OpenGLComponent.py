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
========================
General OpenGL component
========================

This components implements the interaction with the OpenGLDisplay
service that is needed to setup, draw and move an object using OpenGL.

It is recommended to use it as base class for new 3D components. It
provides methods to be overridden for adding functionality.

Example Usage
-------------
One of the simplest possible reasonable component would like something
like this::

    class Point(OpenGLComponent):
        def draw(self):
            glBegin(GL_POINTS)
            glColor(1,0,0)
            glVertex(0,0,0)
            glEnd()

A more complex component that changes colour in response to messages
sent to its "colour" inbox and reacts to mouse clicks by rotationg
slightly::

    class ChangingColourQuad(OpenGLComponent):
        def setup(self):
            self.colour = (0.5,1.0,0.5)
            self.addInbox("colour")
            self.addListenEvents([pygame.MOUSEBUTTONDOWN])
        
        def draw(self):
            glBegin(GL_QUADS)
            glColor(*self.colour)
            glVertex(-1, 1, 0)
            glVertex(1, 1, 0)
            glVertex(1, -1, 0)
            glVertex(-1, -1, 0)
            glEnd()
            
        def handleEvents(self):
            while self.dataReady("events"):
                event = self.recv("events")
                if event.type == pygame.MOUSEBUTTONDOWN and self.identifier in event.hitobjects:
                    self.rotation += Vector(0,0,10)
                    self.rotation %= 360
        
        def frame(self):
            while self.dataReady("colour"):
                self.colour = self.recv("colour")
                self.redraw()
      

How does it work?
-----------------

OpenGLComponent provides functionality to display and move objects in
OpenGL as well as to process events. The component registers at the
OpenGL display service, draws its contens to a displaylist and applies
its transformations to a Transform object. The display list id and the
Transform objects are continuosly transfered to the display service when
updated.

For movement several inboxes are provided. The messages sent to these
boxes are collected and applied automatically. The inboxes and expected
messages are:

- position      -- position triples (x,y,z)
- rotation      -- rotation triples (x,y,z)
- scaling       -- scaling triples (x,y,z)
- rel_position  -- relative position triples (x,y,z)
- rel_rotation  -- relative rotation triples (x,y,z)
- rel_scaling   -- relative scaling triples (x,y,z)

When an OpenGLComponent gets moved, it also provides feedback about its
movement. This feedback is sent to the following outboxes:

- position  -- position triples (x,y,z)
- rotation  -- rotation triples (x,y,z)
- scaling   -- scaling triples (x,y,z)

OpenGLComponent is designed to get subclassed by opengl components.
Using it as base class has the advantage not having to worry about
interaction with the OpenGl display service. To add functionality, the
following methods are provided to be overridden:

- setup()           -- set up the component
- draw()            -- draw content using OpenGL
- handleEvents()    -- handle input events ("events" inbox)
- frame()           -- called every frame, to add additional functionality

Stubs method are provided, so missing these out does not result in
broken code. The methods get called from the main method, the following
code shows in which order::

    def main(self):
        # create and send display request
        ...
        # setup function from derived objects
        self.setup()        
        ...
        # inital apply trasformations
        self.applyTransforms() # generates and sends a Transform object
        # initial draw to display list
        self.redraw() # calls draw and saves it to a displaylist

        ...
        while 1:
            yield 1
            self.applyTransforms()
            self.handleMovement()
            # handle events function from derived objects
            self.handleEvents()
            # frame function from derived objects
            self.frame()

As can be seen here, there is no invocation of draw in the main loop. It
is only called once to generate a displaylist which then gets send to
the display service. This is the normal situation with static 3D
objects. If you want to create a dynamic object, e.g. which changes e.g.
its geometry or colour (see second example above), you need to call the
redraw() method whenever changes happen.

If you need to override the __init__() method, e.g. to get
initialisation parameters, make sure to pass on all keyword arguments to
__init__(...) of the superclass, e.g.::

    def __init__(self, **argd):
        super(ClassName, self).__init__(**argd)
        # get an initialisation parameter
        myparam = argd.get("myparam", defaultvalue)


The following methods are provided to be used by inherited objects:

- redraw() -- Call draw() and save its actions to a displaylist. 
  Send it as update request to the display service.
  *Don't call this method from within draw()!*
- addListenEvents(list of events) -- Request reception of a list of events
- removeListenEvents(list of events) -- Stop reveiving events

The are inteded to simplify component handling. For detailed description
see their documentation.

Every OpenGLComponent has its own pygame Clock object. It is used to
measure the time between frames. The value gets stored in self.frametime
in seconds and can be used by derived components to make movement time-
based rather than frame-based. For example to rotate 3 degrees per
second you would do something like::

    self.rotation.y += 3.0*self.frametime

OpenGLComponent components terminate if a producerFinished or
shutdownMicroprocess message is received on their "control" inbox. The
received message is also forwarded to the "signal" outbox. Upon
termination, this component does *not* unbind itself from the
OpenGLDisplay service and does not free any requested resources.

"""


import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import Axon
from OpenGLDisplay import OpenGLDisplay
from Vector import Vector
from Transform import Transform


class OpenGLComponent(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    """\
    OpenGLComponent(...) -> create a new OpenGL component (not very useful though; it is rather designed to inherit from).

    This components implements the interaction with the OpenGLDisplay
    service that is needed to setup, draw and move an object using OpenGL.

    Keyword arguments:
    
    - size      -- three dimensional size of component (default=(0,0,0))
    - rotation  -- rotation of component around (x,y,z) axis (defaul=(0,0,0))
    - scaling   -- scaling along the (x,y,z) axis (default=(1,1,1))
    - position  -- three dimensional position (default=(0,0,0))
    - name      -- name of component (mostly for debugging, default="nameless")
    """
    
    Inboxes = {
        "inbox": "not used",
        "control": "For shutdown messages",
        "callback": "for the response after a displayrequest",
        "events": "Input events",
        "position" : "receive position triple (x,y,z)",
        "rotation": "receive rotation triple (x,y,z)",
        "scaling": "receive scaling triple (x,y,z)",
        "rel_position" : "receive position triple (x,y,z)",
        "rel_rotation": "receive rotation triple (x,y,z)",
        "rel_scaling": "receive scaling triple (x,y,z)",
    }
    
    Outboxes = {
        "outbox": "not used",
        "signal": "For shutdown messages",
        "display_signal" : "Outbox used for communicating to the display surface",
        "position" : "send position status when updated",
        "rotation": "send rotation status when updated",
        "scaling": "send scaling status when updated",
    }
    
    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(OpenGLComponent, self).__init__()

        # get transformation data and convert to vectors
        self.size = Vector( *argd.get("size", (0,0,0)) )
        self.position = Vector( *argd.get("position", (0,0,0)) )
        self.rotation = Vector( *argd.get("rotation", (0.0,0.0,0.0)) )
        self.scaling = Vector( *argd.get("scaling", (1,1,1) ) )
        
        # for detection of changes
        self.oldrot = Vector()
        self.oldpos = Vector()
        self.oldscaling = Vector()

        self.transform = Transform()

        # name (mostly for debugging)
        self.name = argd.get("name", "nameless")

        # create clock
        self.clock = pygame.time.Clock()
        self.frametime = 0.0

        # get display service
        displayservice = OpenGLDisplay.getDisplayService()
        # link display_signal to displayservice
        self.link((self,"display_signal"), displayservice)
        
            
            
    def main(self):
        # create display request
        self.disprequest = { "OGL_DISPLAYREQUEST" : True,
                             "objectid" : id(self),
                             "callback" : (self,"callback"),
                             "events" : (self, "events"),
                             "size": self.size
                           }
        # send display request
        self.send(self.disprequest, "display_signal")
        # inital apply trasformations
        self.applyTransforms()
        # setup function from derived objects
        self.setup()        
        # initial draw to display list
        self.redraw()

        # wait for response on displayrequest
        while not self.dataReady("callback"):  yield 1
        self.identifier = self.recv("callback")
        
        while 1:
            yield 1
            
            while self.dataReady("control"):
                cmsg = self.recv("control")
#                if isinstance(cmsg, producerFinished) or isinstance(cmsg, shutdownMicroprocess):
#                    self.send(cmsg, "signal")
#                    return
                   
            self.frametime = float(self.clock.tick())/1000.0
            self.handleMovement()
            self.handleEvents()
            self.applyTransforms()
            # frame function from derived objects
            self.frame()

                                          
    def applyTransforms(self):
        """ Use the objects translation/rotation/scaling values to generate a new transformation Matrix if changes have happened. """
        # generate new transformation matrix if needed
        if self.oldscaling != self.scaling or self.oldrot != self.rotation or self.oldpos != self.position:
            self.transform = Transform()
            self.transform.applyScaling(self.scaling)
            self.transform.applyRotation(self.rotation)
            self.transform.applyTranslation(self.position)

            if self.oldscaling != self.scaling:
                self.send(self.scaling.toTuple(), "scaling")
                self.oldscaling = self.scaling.copy()

            if self.oldrot != self.rotation:
                self.send(self.rotation.toTuple(), "rotation")
                self.oldrot = self.rotation.copy()

            if self.oldpos != self.position:
                self.send(self.position.toTuple(), "position")
                self.oldpos = self.position.copy()
                
            # send new transform to display service
            transform_update = { "TRANSFORM_UPDATE": True,
                                 "objectid": id(self),
                                 "transform": self.transform
                               }
            self.send(transform_update, "display_signal")


    def handleMovement(self):
        """ Handle movement commands received by corresponding inboxes. """
        while self.dataReady("position"):
            pos = self.recv("position")
            self.position = Vector(*pos)
        
        while self.dataReady("rotation"):
            rot = self.recv("rotation")
            self.rotation = Vector(*rot)
            
        while self.dataReady("scaling"):
            scaling = self.recv("scaling")
            self.scaling = Vector(*scaling)
            
        while self.dataReady("rel_position"):
            self.position += Vector(*self.recv("rel_position"))
            
        while self.dataReady("rel_rotation"):
            self.rotation += Vector(*self.recv("rel_rotation"))
            
        while self.dataReady("rel_scaling"):
            self.scaling = Vector(*self.recv("rel_scaling"))

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


    def redraw(self):
        """\
        Invoke draw() and save its commands to a newly generated displaylist.
        
        The displaylist name is then sent to the display service via a
        "DISPLAYLIST_UPDATE" request.
        """
        # display list id
        displaylist = glGenLists(1);
        # draw object to its displaylist
        glNewList(displaylist, GL_COMPILE)
        self.draw()
        glEndList()

        
        dl_update = { "DISPLAYLIST_UPDATE": True,
                      "objectid": id(self),
                      "displaylist": displaylist
                    }
        self.send(dl_update, "display_signal")
        


    ##
    # Method stubs to be overridden by derived objects
    ##

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


    def draw(self):
        """
        Method stub
        
        Override this method for drawing. Only use commands which are
        needed for drawing. Will not draw directly but be saved to a
        displaylist. Therefore, make sure not to use any commands which
        cannot be stored in displaylists (unlikely anyway).
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

__kamaelia_components__ = (OpenGLComponent,)

if __name__=='__main__':
    class Point(OpenGLComponent):
        def draw(self):
            glBegin(GL_POINTS)
            glColor(1,0,0)
            glVertex(0,0,0)
            glEnd()

    class ChangingColourQuad(OpenGLComponent):
        def setup(self):
            self.colour = (0.5,1.0,0.5)
            self.addInbox("colour")
            self.addListenEvents([pygame.MOUSEBUTTONDOWN])
        
        def draw(self):
            glBegin(GL_QUADS)
            glColor(*self.colour)
            glVertex(-1, 1, 0)
            glVertex(1, 1, 0)
            glVertex(1, -1, 0)
            glVertex(-1, -1, 0)
            glEnd()
            
        def handleEvents(self):
            while self.dataReady("events"):
                event = self.recv("events")
                if event.type == pygame.MOUSEBUTTONDOWN and self.identifier in event.hitobjects:
                    self.rotation += Vector(0,0,10)
                    self.rotation %= 360
        
        def frame(self):
            while self.dataReady("colour"):
                self.colour = self.recv("colour")
                self.redraw()

    Point(position=(-1,0,-10)).activate()
    ChangingColourQuad(position=(1,0,-10)).activate()
    Axon.Scheduler.scheduler.run.runThreads()  
# Licensed to the BBC under a Contributor Agreement: THF
