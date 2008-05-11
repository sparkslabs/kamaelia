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
======================
OpenGL Display Service
======================

This component provides an OpenGL window and manages input events,
positioning and drawing of other components. It handles both OpenGL and
Pygame components.

OpenGLDisplay is a service that registers with the Coordinating
Assistant Tracker (CAT).

Example Usage
-------------
If you want to change some of the default parameters, like the viewport,
you first have to create an OpenGLDisplay object and then register it.
The following would show a simple cube from a slightly changed viewer
position::

    display = OpenGLDisplay(viewerposition=(0,-10,0), lookat=(0,0,-15)).activate()
    OpenGLDisplay.setDisplayService(display)

    SimpleCube(position=(0,0,-15)).activate()

If you want to use pygame components, you have to override the
PygameDisplay service before creating any pygame components::

    display = OpenGLDisplay.getDisplayService()
    PygameDisplay.setDisplayService(display[0])

For examples of how components have to interfrere with OpenGLDisplay,
please have a look at OpenGLComponent.py and Interactor.py.

How does it work?
-----------------
OpenGLDisplay is a service. obtain it by calling the
OpenGLDisplay.getDisplayService(...) static method. Any existing instance
will be returned, otherwise a new one is automatically created.

Alternatively, if you wish to configure OpenGLDisplay with options other
than the defaults, create your own instance, then register it as a
service by calling the PygameDisplay.setDisplayService(...) static
method. NOTE that it is only advisable to do this at the top level of
your system, as other components may have already requested and created
a OpenGLDisplay component!

When using only OpenGL components and no special display settings have
to be made, you won't see OpenGLDisplay as it is registered
automatically when it is first requested (by invoking the
getDisplayService(...) static method).

You can also use an instance of OpenGLDisplay to override the
PygameDisplay service as it implements most of the functionality of
PygameDisplay. You will want to do this when you want to use Pygame
components along with OpenGL components.

pygame only supports one display window at a time, you must not make more than
one OpenGLDisplay component.

OpenGLDisplay listens for requests arriving at its "notify" inbox. A request can
currently be to:

- register an OpenGL component (OGL_DISPLAYREQUEST)
- register a pygame component (DISPLAYREQUEST)
- register a pygame wrapper  (WRAPPERREQUEST)
- register an eventspy (EVENTSPYREQUEST)
- listen or stop listening to events (ADDLISTENEVENT, REMOVELISTENEVENT)
- update the displaylist of an OpenGL component (UPDATE_DISPLAYLIST)
- update the transform of an OpenGL component (UPDATE_TRANSFORM)
- invoke a redraw of a pygame surface (REDRAW)

OpenGL components
^^^^^^^^^^^^^^^^^

OpenGL components get registered by an OGL_DISPLAYREQUEST. Such a
request is a dictionary with the following keys::

    {
        "OGL_DISPLAYREQUEST": True,     # OpenGL Display request
        "objectid" : id(object),            # id of requesting object (for identification)
        "callback" : (component,"inboxname"),   # to send the generated event id to
            
        "events" : (component, "inboxname"),    # to send event notification (optional)
        "size": (x,y,z),                # size of object (not yet used)
    }

When OpenGLDisplay received such a request it generates an identifier
and returns it to the box you specify by "callback". This identifier can
later be used to determine if a mouse event "hit" the object.

It is important to note that OpenGL don't draw and transform themselves
directly but only hand displaylists and Transform objects to the display
service. After an OpenGL component has been registered, it can send
displaylist- and transform-updates. These requests are dictionaries of
the following form::

    {
        "DISPLAYLIST_UPDATE": True, # update displaylist
        "objectid": id(object),     # id of requesting object
        "displaylist": displaylist  # new displaylist
    }

If an object is static, i.e. does not change its geometry, it only needs
to send this update one time. Dynamic objects can provide new
displaylists as often as they need to.::

    {
        "TRANSFORM_UPDATE": True,   # update transform
        "objectid": id(self),       # id of requesting object
        "transform": self.transform # new transform
    }

A transform update should be sent every time the object transform
changes, i.e. it is moved.

OpenGL components can also request listening to events. See "Listening
to events" below.

It is generally recommended to use the class OpenGLComponent as base
class for OpenGL components. It implements all the functionality
required to create, draw, move OpenGL components and to handle events
(see OpenGLComponent.py for the class and e.g. SimpleCube.py, Button.py
and other components for examples).

Pygame components
^^^^^^^^^^^^^^^^^

OpenGLDisplay is designed to be compatible with PygameDisplay. After
overriding the PygameDisplay service, pygame components can be created
as usual. See the documentation of PygameDisplay
(Kamaelia/UI/PygameDisplay.py) for how to do this.

NOTE: Overlays are not supported yet.

Pygame wrappers
^^^^^^^^^^^^^^^

It is possibly, by sending a WRAPPERREQUEST, to wrap an already
registered pygame component by a OpenGL component. The surface of the
pygame component is then excluded from normal drawing and this
responsibility is handed to the requesting component by giving it the
texture name corresponding to the surface. The event processing of mouse
events is then also relinked to be done by the wrapper.

The wrapper request is a dictionary with the following keys::

    {
        "WRAPPERREQUEST" : True,                    # wrap a pygame component
        "wrapcallback" : (object, "inboxname"),     # send response here
        "eventrequests" : (object, "inboxname"),    # to receive event requests by the wrapped component
        "wrap_objectid": id(wrapped_component)      # object id of the component to be wrapped
    }

When a WRAPPERREQUEST is received for a component which is not
registered yet, it is stored until the component to be wrapped gets
registered.

When a wrapper request was received, the OpenGL display service returns
a dictionary to the box specified by "wrapcallback" containing the
following keys::

    {
        "texname": texname,             # OpenGL texture name
        "texsize": (width, height),     # texture coordinate size
        "size": (width, height)         # size of pygame surface in pixels
    }

See PygameWrapperPlane.py for an example implementation of a wrapper.

Listening to events
^^^^^^^^^^^^^^^^^^^

Once your component has been registered, it can request to be notified
of specific pygame events. The same requests are used for Pygame and
OpenGL components, only the keys are slightly different.

To request to listen to a given event, send a dictionary to the "notify"
inbox, containing the following::

    {
        "ADDLISTENEVENT" : pygame_eventtype,    # example: pygame.KEYDOWN
        "surface" : your_surface,               # for pygame components
        "objectid" : id(object),                # for OpenGL components
    }

To unsubscribe from a given event, send a dictionary containing::

    {
        "REMOVELISTENEVENT" : pygame_eventtype,
        "surface" : your_surface,               # for pygame components
        "objectid" : id(object),                # for OpenGL components
    }
    
Events will be sent to the inbox specified in the "events" key of the
"DISPLAYREQUEST" or "OGL_DISPLAYREQUEST" message. They arrive as a list
of pygame event objects.

The events objects of type Bunch with the following variables:

- type      -- Pygame event type

 For events of type pygame.KEYDOWN, pygame.KEYUP:

- key       -- Pressed or released key

 For events of type pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP:

- pos       -- Mouse position
- button    -- Pressed or released mouse button number

 For events of type pygame.MOUSEMOTION:

- rel       -- Relative mouse motion.
- buttons   -- Buttons pressed while mousemotion

 For events of type pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION when sent to OpenGL components:

- viewerposition    -- Position of viewer
- dir               -- Direction vector of generated from mouse position
- hitobjects        -- List of hit objects
    
NOTE: If the event is MOUSEMOTION, MOUSEBUTTONUP or MOUSEBUTTONDOWN then
you will instead receive a replacement object, with the same attributes
as the pygame event. But for pygame components, the 'pos' attribute
adjusted so that (0,0) is the top left corner of *your* surface. For
OpenGL components the origin and direction of the intersection vector
determined using the mouse position and viewport will be added as well
as a list of identfiers of objects that has been hit.

If a component has requested reception of an event type, it gets every
event that happens of that type, regardless if it is of any concern to
the component. In the case of mouse events there is a list of hit
objects included which are determined by using OpenGL picking.

    
Eventspies
^^^^^^^^^^

Eventspies are components that basically listen to events for other
components. They are registered by sending an EVENSPYREQUEST::

    {
        "EVENTSPYREQUEST" : True,
        "objectid" : id(object),            # id of requesting object
        "target": id(target),               # id of object to be spied
        "callback" : (object,"inboxname"),  # for sending event identifier
        "events" : (object, "inboxname")    # for reception of events
    }

In return you get the identifier of the target component that can be
used to determine if the target component has been hit. An evenspy can
request reception of event types like usual (using ADDLISTENEVENT and
REMOVELISTENEVENT).  When events are spied this does not affect normal
event processing.

Shutdown
^^^^^^^^

Upon reception of a pygame.QUIT event, OpenGLDisplay sends an
Axon.Ipc.shutdownMicroprocess object out of its signal outbox. The
service itself does not terminate.

"""

import pygame
import Axon
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

from Kamaelia.UI.PygameDisplay import PygameDisplay

from Vector import Vector
from Transform import Transform

import time

_cat = Axon.CoordinatingAssistantTracker

class Bunch: pass

class OpenGLDisplay(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    """\
    OpenGLDisplay(...) -> new OpenGLDisplay component

    Use OpenGLDisplay.getDisplayService(...) in preference as it returns an
    existing instance, or automatically creates a new one.

    Or create your own and register it with setDisplayService(...)

    Keyword arguments (all optional):
    
    - title             -- caption of window (default=http://kamaelia.sourceforge.net)
    - width              -- pixels width (default=800)
    - height             -- pixels height (default=600)
    - background_colour  -- (r,g,b) background colour (default=(255,255,255))
    - fullscreen         -- set to True to start up fullscreen, not windowed   (default=False)
    - show_fps          -- show frames per second in window title (default=True)
    - limit_fps           -- maximum frame rate (default=60)
        Projection parameters
    - near              -- distance to near plane (default=1.0)
    - far               -- distance to far plane (default=100.0)
    - perspective       -- perspective angle (default=45.0)
        Viewer position and orientation
    - viewerposition        -- position of viewer (default=(0,0,0))
    - lookat                -- look at point (default= (0,0,-self.farPlaneDist))
    - up                    -- up vector (default(0,1,0))
        Fog
    - fog           -- tuple of fog distances (start, end). if not set, fog is disabled (default)
    - fog_colour    -- (r,g,b) fog colour (default=(255,255,255) )
    - fog_density   -- fog density (default=0.35)
        Event processing
    - hitall        -- boolean, if false, only the nearest object under the cursor gets activated (default=False)
    

    """

    Inboxes =  {
        "inbox"    : "Default inbox, not currently used",
        "control"  : "NOT USED",
        "notify"   : "For reception of requests for surfaces, overlays and events",
        "events"   : "For reception of pygame events",
    }
               
    Outboxes = {
        "outbox" : "NOT USED",
        "signal" : "NOT USED",
    }
                
                 
    def setDisplayService(display, tracker = None):
        """\
        Sets the given pygamedisplay as the service for the selected tracker or
        the default one.

        (static method)
        """
        if not tracker:
            tracker = _cat.coordinatingassistanttracker.getcat()
        tracker.registerService("ogl_display", display, "notify")
    setDisplayService = staticmethod(setDisplayService)

    def getDisplayService(tracker=None): # STATIC METHOD
        """\
        Returns any live pygamedisplay registered with the specified (or default)
        tracker, or creates one for the system to use.

        (static method)
        """
        if tracker is None:
            tracker = _cat.coordinatingassistanttracker.getcat()
        try:
            service = tracker.retrieveService("ogl_display")
            return service
        except KeyError:
            display = OpenGLDisplay()
            display.activate()
            OpenGLDisplay.setDisplayService(display, tracker)
            service=(display,"notify")
            return service
    getDisplayService = staticmethod(getDisplayService)
    
        
    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(OpenGLDisplay,self).__init__()
        self.caption = argd.get("title", "http://kamaelia.sourceforge.net")
        self.width = argd.get("width",800)
        self.height = argd.get("height",600)
        self.background_colour = argd.get("background_colour", (255,255,255))
        self.fullscreen = pygame.FULLSCREEN * argd.get("fullscreen", 0)
        
        self.show_fps = argd.get("show_fps", True)
        self.limit_fps = argd.get("limit_fps", 0)
        self.fps_delay = 0.0
        
        # for framerate limitation
        self.clock = pygame.time.Clock()

        # 3D component handling
        self.ogl_objects = []
        self.ogl_names = {}
        self.ogl_sizes = {}
        self.ogl_displaylists = {}
        self.ogl_transforms = {}
        self.ogl_nextName = 1

        # Eventspies (receive events of other components)
        self.eventspies = []

        # pygame component handling
        self.pygame_surfaces = []
        self.pygame_objectid_to_surface = {}
        self.pygame_sizes = {}
        self.pygame_positions = {}
        self.pygame_pow2surfaces = {}
        self.pygame_texnames = {}
        # used for surface positioning
        self.next_position = (0,0)
        
        # pygame wrapping
        self.wrappedsurfaces = []
        self.wrapper_requestcomms = {}
        self.pending_wrapperrequests = {}
        
        # Event handling
        self.eventcomms = {}
        self.eventservices = {}
        self.eventswanted = {}
        self.hitall = argd.get("hitall", False)
        
        # determine projection parameters
        self.nearPlaneDist = argd.get("near", 1.0)
        self.farPlaneDist = argd.get("far", 100.0)
        self.perspectiveAngle = argd.get("perspective", 45.0)
        self.aspectRatio = float(self.width)/float(self.height)
        global pi
        self.farPlaneHeight = self.farPlaneDist*2.0/tan(pi/2.0-self.perspectiveAngle*pi/360.0)
        self.farPlaneWidth = self.farPlaneHeight*self.aspectRatio
        self.farPlaneScaling = self.farPlaneWidth/self.width
        
        # determine viewer position and orientation
        self.viewerposition = Vector(*argd.get("viewerposition", (0,0,0)))
        self.lookat = Vector(*argd.get("lookat", (0,0,-self.farPlaneDist)))
        self.up = Vector(*argd.get("up", (0,1,0)))
        # transform used to correct the mouse click positions
        self.coordCorrectionTransform = Transform()
        self.coordCorrectionTransform.setLookAtRotation(-self.viewerposition, self.lookat, self.up)
        
        # initialize the display      
        pygame.init()
        display = pygame.display.set_mode((self.width, self.height), self.fullscreen| pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption(self.caption)
        pygame.mixer.quit()
        
        glClearColor(self.background_colour[0],self.background_colour[1],self.background_colour[2],1)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        
        # make fog settings if enabled
        fog_dists = argd.get("fog", None)
        if fog_dists is not None:
            glEnable(GL_FOG)
            glFog(GL_FOG_MODE, GL_LINEAR)
            glHint(GL_FOG_HINT, GL_NICEST)
            glFog(GL_FOG_START, fog_dists[0])
            glFog(GL_FOG_END, fog_dists[1])
            glFog(GL_FOG_DENSITY, argd.get("fog_density", 1.0) )
            fog_colour = argd.get("fog_colour", (255,255,255))
            fog_colour = [float(x)/255.0 for x in fog_colour]
            glFog(GL_FOG_COLOR, fog_colour)
        
        # set projection matrix
        glMatrixMode(GL_PROJECTION)                 
        glLoadIdentity()
        self.setProjection()
    

    def main(self):
        """Main loop."""
        while 1:
        
            # limit and show fps (if enabled)
            self.fps_delay += self.clock.tick(self.limit_fps)
            if self.show_fps and self.fps_delay > 1000.0:
                pygame.display.set_caption("%s FPS:%d" % (self.caption, self.clock.get_fps()) )
                self.fps_delay = 0
                
            self.handleRequests()
            self.handleEvents()
            self.updateDisplay()
            yield 1

    
    def handleRequests(self):
        """ Handles service requests. """
        while self.dataReady("notify"):
            message = self.recv("notify")

            if message.get("OGL_DISPLAYREQUEST", False):
                self.handleRequest_OGL_DISPLAYREQUEST(message)
                
            elif message.get("EVENTSPYREQUEST", False):
                self.handleRequest_EVENTSPYREQUEST(message)

            elif message.get("DISPLAYLIST_UPDATE", False):
                ident = message.get("objectid")
                try:
                    glDeleteLists(self.ogl_displaylists[ident], 1)
                except KeyError: pass
                self.ogl_displaylists[ident] = message.get("displaylist")
                
            elif message.get("TRANSFORM_UPDATE", False):
                ident = message.get("objectid")
                self.ogl_transforms[ident] = message.get("transform")
                
            elif message.get("ADDLISTENEVENT", False):
                ident = message.get("objectid")
                if ident is None:
                    ident = id(message.get("surface", None))

                if ident in self.wrappedsurfaces:
                    self.send(message, self.wrapper_requestcomms[id(surface)])
                else:
                    self.eventswanted[ident][message.get("ADDLISTENEVENT")] = True
                
            elif message.get("REMOVELISTENEVENT", False):
                ident = message.get("objectid")
                if ident is None:
                    ident = message.get("surface", None)

                if ident in self.wrappedsurfaces:
                    self.send(message, self.wrapper_requestcomms[id(surface)])
                else:
                    self.eventswanted[ident][message.get("REMOVELISTENEVENT")] = False

            elif message.get("DISPLAYREQUEST", False):
                self.handleRequest_DISPLAYREQUEST(message)

            elif message.get("REDRAW", False):
                surface = message["surface"]
                self.updatePygameTexture(surface, self.pygame_pow2surfaces[id(surface)], self.pygame_texnames[id(surface)])

            elif message.get("WRAPPERREQUEST", False):
                self.handleRequest_WRAPPERREQUEST(message)

                    
    def handleEvents(self):
        """ Handles pygame input events. """
        
        # pre-fetch all waiting events in one go
        events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # On pygame.QUIT send shutdownMicroprocess to signal
                self.send(Axon.Ipc.shutdownMicroprocess(), "signal")
            else:
                events.append(event)

        self.handleOGLComponentEvents(events)
        self.handlePygameComponentEvents(events)
    

    def updateDisplay(self):
        """ Draws all components, updates screen, clears the backbuffer and depthbuffer . """
        self.drawOpenGLComponents()
        self.drawPygameSurfaces()

        # show frame
        glFlush()
        pygame.display.flip()
        
        # clear drawing buffer
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        

    def genIdentifier(self):
        """ Returns a unique number. """
        ogl_name = self.ogl_nextName
        self.ogl_nextName += 1
        return ogl_name
        
    
    def handleRequest_OGL_DISPLAYREQUEST(self, message):
        ident = message.get("objectid")
        eventservice = message.get("events", None)
        callbackservice = message.get("callback")

        # store object
        self.ogl_objects.append(ident)
        self.ogl_sizes[ident] = message.get("size")

        # generate and store an ogl name for the requesting object
        ogl_name = self.genIdentifier()
        self.ogl_names[ident] = ogl_name

        # link to eventcallback
        if eventservice is not None:
            eventcomms = self.addOutbox("eventsfeedback")
            self.eventcomms[ident] = eventcomms
            self.eventswanted[ident] = {}
            self.link((self,eventcomms), eventservice)

        # link callback service                    
        callbackcomms = self.addOutbox("displayerfeedback")
        self.link((self, callbackcomms), callbackservice)

        # send response (generated name)
        self.send(ogl_name, callbackcomms)

        
    def handleRequest_EVENTSPYREQUEST(self, message):
        ident = message.get("objectid")
        target = message.get("target")
        eventservice = message.get("events", None)
        callbackservice = message.get("callback")
 
        # store object id
        self.eventspies.append(ident)
 
        # link eventservice
        if eventservice is not None:
            eventcomms = self.addOutbox("eventsfeedback")
            self.eventcomms[ident] = eventcomms
            self.eventswanted[ident] = {}
            self.link((self,eventcomms), eventservice)
 
        # link callbackservice
        callbackcomms = self.addOutbox("displayerfeedback")
        self.link((self, callbackcomms), callbackservice)
 
        # send response
        ogl_name = self.ogl_names[target]                    
        self.send(ogl_name, callbackcomms)

    
    def calcPow2Size(self, size):
        """ Calculates the power of 2 dimensions for a given size. """
        pow2size = (int(2**(ceil(log(size[0], 2)))), int(2**(ceil(log(size[1], 2)))))
        return pow2size
        
    def handleRequest_DISPLAYREQUEST(self, message):
        callbackservice = message["callback"]
        eventservice = message.get("events", None)
        size  = message["size"]
        alpha = message.get("alpha", 255)
        transparency = message.get("transparency", None)

        # create surface
        surface = pygame.Surface(size)
        self.pygame_surfaces.append(surface)
        self.pygame_sizes[id(surface)] = size
        position = message.get("position", self.surfacePosition(surface))

        # save objectid of requesting component
        # (this is needed for wrapperrequests)
        objectid = id(callbackservice[0])
        self.pygame_objectid_to_surface[objectid] = surface

        # create another surface, with dimensions a power of two
        # this is needed because otherwise texturing is REALLY slow
        pow2size = self.calcPow2Size(size)
        pow2surface = pygame.Surface(pow2size)
        self.pygame_pow2surfaces[id(surface)] = pow2surface

        # handle transparency
        surface.set_alpha(alpha)
        if transparency:
            surface.set_colorkey(transparency)

        # save position
        self.pygame_positions[id(surface)] = position

        # handle event comms
        if eventservice is not None:
            # save eventservice for later use
            self.eventservices[id(surface)] = eventservice
            # link eventservice
            eventcomms = self.addOutbox("eventsfeedback")
            self.eventswanted[id(surface)] = {}
            self.link((self,eventcomms), eventservice)
            self.eventcomms[id(surface)] = eventcomms

        # generate texture name
        texname = glGenTextures(1)
        self.pygame_texnames[id(surface)] = texname

        # link callback communications
        callbackcomms = self.addOutbox("displayerfeedback")
        self.link((self, callbackcomms), callbackservice)

        # send response
        self.send(surface, callbackcomms)     
        
        # if there is a wrapper request waiting for this component, handle it
        if objectid in self.pending_wrapperrequests:
            self.handleRequest_WRAPPERREQUEST(self.pending_wrapperrequests[objectid])
            self.pending_wrapperrequests.pop(objectid)

    
    def handleRequest_WRAPPERREQUEST(self, message):
        objectid = message.get("wrap_objectid")
        
        # if the component that shall be wrapped is not registered yet,
        # save wrapper request for later handling
        try:
            surface = self.pygame_objectid_to_surface[objectid]
        except KeyError:
            self.pending_wrapperrequests[objectid] = message
        else:
            callbackservice = message["wrapcallback"]
            eventrequestservice = message["eventrequests"]

            # store surface to wrap
            self.wrappedsurfaces.append(id(surface))

            # get and link callback comms
            callbackcomms = self.addOutbox("wrapfeedback")
            self.link((self,callbackcomms), callbackservice)

            # get and link eventrequest comms
            eventrequestcomms = self.addOutbox("eventrequests")
            self.link((self,eventrequestcomms), eventrequestservice)
            self.wrapper_requestcomms[id(surface)] = eventrequestcomms

            # find corresponding pow2surface
            pow2surface = self.pygame_pow2surfaces[id(surface)]

            #determine texture coordinate lengths
            tex_w = float(surface.get_width())/float(pow2surface.get_width())
            tex_h = float(surface.get_height())/float(pow2surface.get_height())

            # generate response
            response = { "texname": self.pygame_texnames[id(surface)],
                         "texsize": (tex_w, tex_h),
                         "size": self.pygame_sizes[id(surface)] }
            try:
                response["eventservice"] = self.eventservices[id(surface)]
                response["eventswanted"] = self.eventswanted[id(surface)]
            except KeyError:
                response["eventservice"] = None
                response["eventswanted"] = None
            # send response
            self.send(response, callbackcomms)
    

    def setProjection(self):
        """ Sets projection matrix. """
        glMatrixMode(GL_PROJECTION)
        gluPerspective(self.perspectiveAngle, self.aspectRatio, self.nearPlaneDist, self.farPlaneDist)
        # apply viewer transforms
        gluLookAt( *(self.viewerposition.toTuple() + self.lookat.toTuple() + self.up.toTuple() ) )

        
    def doPicking(self, pos):
        """\
        Uses OpenGL picking to determine objects that have been hit by mouse pointer.
        see e.g. OpenGL Redbook
        """
        # object picking
        glSelectBuffer(512)
        glRenderMode(GL_SELECT)

        # prepare matrices
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluPickMatrix(pos[0], self.height-pos[1], 1, 1)
        self.setProjection()

        # "draw" objects in select mode
        glInitNames()
        glPushName(0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        for obj in self.ogl_objects:
            try:
                glLoadMatrixf(self.ogl_transforms[obj].getMatrix())
                glLoadName(self.ogl_names[obj])
                glCallList(self.ogl_displaylists[obj])
            except KeyError: pass
        glPopMatrix()

        # restore matrices
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        # force completion
        glFlush()

        # process hits                
        hits = glRenderMode(GL_RENDER)
        hitlist = []
        if self.hitall:
            # list of hit objects
            hitlist = [hit[2][0] for hit in hits]
        else:
            nearest = 4294967295
            for hit in hits:
                if hit[0] < nearest:
                    nearest = hit[0]
                    hitlist = [hit[2][0]]
                    
        return hitlist


    def drawPygameSurfaces(self):
        """ Draws all surfaces of registered pygame components on top of everything else. """ 
        # disable depth testing temporarely to ensure that pygame components
        # are on top of everything
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        for surface in self.pygame_surfaces:
            # skip surfaces which get wrapped
            if id(surface) in self.wrappedsurfaces: continue

            # get needed vars
            texname = self.pygame_texnames[id(surface)]
            position = self.pygame_positions[id(surface)]
            size = self.pygame_sizes[id(surface)]
            pow2surface = self.pygame_pow2surfaces[id(surface)]

            # create texture if not already done
            if not glIsTexture(texname):
                self.updatePygameTexture(surface, pow2surface, texname)

            glBindTexture(GL_TEXTURE_2D, texname)

            # determine surface positions on far Plane
            l = position[0]*self.farPlaneScaling-self.farPlaneWidth/2
            t = -position[1]*self.farPlaneScaling+self.farPlaneHeight/2
            r = l + size[0]*self.farPlaneScaling
            b = t - size[1]*self.farPlaneScaling
            
            #determine texture coordinates
            tex_w = float(size[0])/float(pow2surface.get_width())
            tex_h = float(size[1])/float(pow2surface.get_height())
                
            # draw just the texture, no background
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)

            # draw faces 
            glBegin(GL_QUADS)
            glColor3f(1, 0, 0)
            glTexCoord2f(0.0, 1.0-tex_h);         glVertex3f( l, b,  -self.farPlaneDist)
            glTexCoord2f(tex_w, 1.0-tex_h);     glVertex3f( r, b,  -self.farPlaneDist)
            glTexCoord2f(tex_w, 1.0); glVertex3f( r,  t,  -self.farPlaneDist)
            glTexCoord2f(0.0, 1.0);     glVertex3f( l,  t,  -self.farPlaneDist)
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)        
  
  
    def drawOpenGLComponents(self):
        """ Draws all registered OpenGL components with their set transformation matrix. """
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        for obj in self.ogl_objects:
            try:
                # load transform of component
                glLoadMatrixf(self.ogl_transforms[obj].getMatrix())
                # call displaylist of component
                glCallList(self.ogl_displaylists[obj])
            except KeyError: pass
        glPopMatrix()

  
    def updatePygameTexture(self, surface, pow2surface, texname):
        """ Converts the surface of a pygame component to an OpenGL texture. """
#        print "UPDATE", texname
        # blit component surface to power of 2 sized surface
        pow2surface.blit(surface, (0,0))
        # set surface as texture
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texname)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        textureData = pygame.image.tostring(pow2surface, "RGBX", 1)
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, pow2surface.get_width(), pow2surface.get_height(), 0,
                        GL_RGBA, GL_UNSIGNED_BYTE, textureData );
        glDisable(GL_TEXTURE_2D)


    def surfacePosition(self,surface):
        """Returns a suggested position for a surface. No guarantees its any good!"""
        position = self.next_position
        self.next_position = position[0]+50, position[1]+50
        return position

        
    def handleOGLComponentEvents(self, events):
        """ Prepare and send input events for OpenGL components. """
        # Handle OpenGL component events
        for event in events:
            if event.type in [ pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN ]:
                # compose event data
                e = Bunch()
                e.type = event.type
                if event.type in [ pygame.KEYDOWN, pygame.KEYUP ]:
                    # key is the only data in keyevents
                    e.key = event.key
                else: #  type is one of pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN
                    # position
                    e.pos = event.pos
                    # add viewer position
                    e.viewerposition = self.viewerposition
                    # determine intersection ray
                    xclick = float(event.pos[0]-self.width/2)*self.farPlaneWidth/float(self.width)
                    yclick = float(-event.pos[1]+self.height/2)*self.farPlaneHeight/float(self.height)
                    untransformed_dir = Vector(xclick, yclick, -self.farPlaneDist)
                    e.direction = self.coordCorrectionTransform.transformVector(untransformed_dir)
                    # determine which objects have been hit
                    e.hitobjects = self.doPicking(event.pos)
                    # set specific event fields
                    if event.type in [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN]:
                        e.button = event.button
                    if event.type == pygame.MOUSEMOTION:
                        e.rel = event.rel
                        e.buttons = event.buttons
                  
                # send events to objects
                for ident in self.ogl_objects + self.eventspies:
                    try:
                        if self.eventswanted[ident][e.type]:
                            self.send(e, self.eventcomms[ident])
                    except KeyError: pass
       
       
    def handlePygameComponentEvents(self, events):
        """ Prepare and send input events for pygame components. """
        # Handle Pygame events
        for surface in self.pygame_surfaces:
            try:
                eventcomms = self.eventcomms[id(surface)]
                if eventcomms is not None:
                    bundle = []
                    for event in events:
                        wanted = False
                        try:   wanted = self.eventswanted[id(surface)][event.type]
                        except KeyError: pass
                        if wanted:
                            # if event contains positional information, remap it
                            # for the surface's coordiate origin
                            if event.type in [ pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN ]:
                                # skip wrapped components (they get events from their wrappers)
                                if id(surface) in self.wrappedsurfaces: continue
                                # assemble event
                                e = Bunch()
                                e.type = event.type
                                pos = event.pos[0],event.pos[1]
                                surfpos = self.pygame_positions[id(surface)]
                                # determine position on surface
                                e.pos  = ( pos[0]-surfpos[0], pos[1]-surfpos[1] )
                                if event.type == pygame.MOUSEMOTION:
                                    e.rel = event.rel
                                if event.type == pygame.MOUSEMOTION:
                                    e.buttons = event.buttons
                                else:
                                    e.button = event.button
                                event = e

                            bundle.append(event)

                    # only send events to listener if we've actually got some
                    if bundle != []:
                        self.send(bundle, eventcomms)
            except KeyError: pass


__kamaelia_components__ = (OpenGLDisplay,)

if __name__=='__main__':
    pass
# Licensed to the BBC under a Contributor Agreement: THF
