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
General OpenGL component
=====================

This components implements the interaction with the OpenGLDisplay
service that is needed to setup, draw and move OpenGL components. It is
recommended to use it as base class for new 3D components. It provides
methods to be overridden for adding functionality.

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

The only thing it does is to draw a point in its origin. But despite its
simplicity it can be translated, rotated and scaled using its provided
inboxes. Using Interactors (see Interactor.py) it can for example even
be controlled by mouse events.

A more complex component could look like this::

    def ChangingColourQuad(OpenGLComponent):
        def setup(self):
            self.colour = (0,0,0)
            self.addInbox("colour")
        
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
                    self.rotation += Vector(0,0,1)
                    self.rotation %= 360
        
        def frame(self):
            while self.dataReady("colour"):
                self.colour = self.recv("colour")
                self.redraw()

It represents a coloured quad which can change its colour when a
corresponing message is sent to its "colour" inbox. When this happens it
gets redrawn. Additionally it reacts to mouseclicks by rotation the quad
by one degree around the z axis.
        

How does it work?
-----------------

The following methods are provided to be overridden:
- setup()           -- set up the component
- draw()            -- draw content using OpenGL
- handleEvents()    -- handle input events ("events" inbox)
- frame()           -- called every frame, to add additional functionality

Stubs method are provided, so missing these out does not result in
broken code. The methods get called from the main method, the following
code shows in which order:

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
initialisation parameters, make sure to call the __init__() method of
the parent class in the following way:

    def __init__(self, **argd):
        super(ClassName, self).__init__(**argd)
        # get an initialisation parameter
        myparam = argd.get("myparam", defaultvalue)

The following methods are provided to be used by inherited objects:

- redraw()
- addListenEvents()
- removeListenEvents()        

The are inteded to simplify component handling. For their functionality
see their description.

Every OpenGLComponent has its own pygame Clock object. It is used to measure the time between frames. The value gets stored in self.frametime in seconds and can be used by derived components to make movement time-based rather than frame-based. For example to rotate 3 degrees per second you would do something like:

    self.rotation.y += 3.0*self.frametime
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

    Keyword arguments:
    - size      -- three dimensional size of component (default=(0,0,0))
    - rotation  -- rotation of component around (x,y,z) axis (defaul=(0,0,0))
    - scaling   -- scaling along the (x,y,z) axis (default=(1,1,1))
    - position  -- three dimensional position (default=(0,0,0))
    - name      -- name of component (mostly for debugging, default="nameless")
    """
    
    Inboxes = {
        "inbox": "not used",
        "control": "ignored",
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
        "signal": "not used",
        "display_signal" : "Outbox used for communicating to the display surface",
        "position" : "send position status when updated",
        "rotation": "send rotation status when updated",
        "scaling": "send scaling status when updated",
    }
    
    def __init__(self, **argd):
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
        Should look like this:
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



if __name__=='__main__':
    o1 = OpenGLComponent(pos=Vector(2, 0,-12), name="center").activate()
    o2 = OpenGLComponent(pos=Vector(3, 1,-12), name="right").activate()
    o3 = OpenGLComponent(pos=Vector(-4, 0,-12), name="left").activate()
    Axon.Scheduler.scheduler.run.runThreads()  
