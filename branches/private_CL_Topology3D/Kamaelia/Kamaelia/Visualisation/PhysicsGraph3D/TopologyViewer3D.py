#!/usr/bin/env python
#
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
Generic 3D Topology Viewer
===========================

TopologyViewer3D is a 3D version of TopologyViewer, which shows Topology in PyGame surface.



Example Usage
-------------
A simple console driven topology viewer::

    Pipeline( ConsoleReader(),
              lines_to_tokenlists(),
              TopologyViewer(),
            ).run()

Then at runtime try typing these commands to change the topology in real time::

    >>> DEL ALL
    >>> ADD NODE 1 "1st node" randompos -
    >>> ADD NODE 2 "2nd node" randompos -
    >>> ADD NODE 3 "3rd node" randompos -
    >>> ADD LINK 1 2
    >>> ADD LINK 3 2
    >>> DEL LINK 1 2
    >>> DEL NODE 1



User Interface
--------------

TopologyViewer3D manifests as a pygame OpenGL display surface. As it is sent
topology information nodes and links between them will appear.

You can click a node with the mouse to select it. Depending on the application,
this may display additional data or, if integrated into another app,  have some
other effect.

Click and drag with the left mouse button to move nodes around. Note that a
simple physics model or repulsion and attraction forces is always active. This
causes nodes to move around to help make it visually clearer, however you may
still need to drag nodes about to tidy it up.


Operation supported:
* esc --- quit

* a --- viewer position move left
* d --- viewer position move right
* w --- viewer position move up
* s --- viewer position move down
* pgup --- viewer position move forward (zoom in)
* pgdn --- viewer position move backward (zoom out)

* left --- rotate selected particles to left around y axis  (all particles if none of them is selected)
* right --- rotate selected particles to right around y axis  (all particles if none of them is selected)
* up --- rotate selected  particles to up around x axis  (all particles if none of them is selected)
* down --- rotate selected particles to down around x axis  (all particles if none of them is selected)
* < --- rotate selected particles anticlock-wise around z axis  (all particles if none of them is selected)
*> --- rotate selected particles clock-wise around z axis  (all particles if none of them is selected)
return --- show next level's topology
backspace --- show last level's topology

* Mouse click --- click node to select one, click empty area to deselect all
* Mouse drag: move particles
* Mouse double-click --- show next level's topology
* Mouse right-click --- show last level's topology

* shift --- multi Select Mode; shift+click for multiple selection/deselection
* ctrl ---  rotation Mode; when ctrl is pressed, mouse dragging will rotate the selected particle (all particles if none of them is selected) rather than move it



How does it work?
-----------------

TopologyViewer3D is a Kamaeila component which renders Topology on an OpenGL pygame display surface.

A 3D topology (graph) of nodes and links between them is rendered to the surface.

You can specify an initial topology by providing a list of instantiated
particles and another list of pairs of those particles to show how they are 
linked.

TopologyViewer reponds to commands arriving at its "inbox" inbox
instructing it on how to change the topology. A command is a list/tuple.

Commands recognised are:

    [ "ADD", "NODE", <id>, <name>, <posSpec>, <particle type> ]
        Add a node, using:
          
        - id            -- a unique ID used to refer to the particle in other topology commands. Cannot be None.
        - name          -- string name label for the particle
        - posSpec       -- string describing initial x,y (see _generateXY)
        - particleType  -- particle type (default provided is "-", unless custom types are provided - see below)
                           currently supported: "-" same as cuboid, cuboid, sphere and teapot
      
    [ "DEL", "NODE", <id> ]
        Remove a node (also removes all links to and from it)
        
    [ "ADD", "LINK", <id from>, <id to> ]
        Add a link, directional from fromID to toID
           
    [ "DEL", "LINK", <id from>, <id to> ]
        Remove a link, directional from fromID to toID
               
    [ "DEL", "ALL" ]
        Clears all nodes and links

    [ "GET", "ALL" ]
        Outputs the current topology as a list of commands, just like
        those used to build it. The list begins with a 'DEL ALL'.

    [ "UPDATE_NAME", "NODE", <id>, <new name> ]
        If the node does not already exist, this does NOT cause it to be created.

    [ "GET_NAME", "NODE", <id> ]
        Returns UPDATE_NAME NODE message for the specified node

Commands are processed immediately, in the order in which they arrive. You
therefore cannot refer to a node or linkage that has not yet been created, or
that has already been destroyed.

If a stream of commands arrives in quick succession, rendering and physics will
be temporarily stopped, so commands can be processed more quickly. This is
necessary because when there is a large number of particles, physics and
rendering starts to take a long time, and will therefore bottleneck the
handling of commands.

However, there is a 1 second timeout, so at least one update of the visual
output is guaranteed per second.

TopologyViewer sends any output to its "outbox" outbox in the same
list/tuple format as used for commands sent to its "inbox" inbox. The following
may be output:

    [ "SELECT", "NODE", <id> ]
        Notification that a given node has been selected.
    
    [ "SELECT", "NODE", None ]
       Notificaion that *no node* is now selected. 
        
    [ "TOPOLOGY", <topology command list> ]
        List of commands needed to build the topology, as it currently stands.
        The list will start with a ("DEL","ALL") command.
        This is sent in response to receiving a ("GET","ALL") command.

Error and tip information is printed out directly when encountered.



Termination
-----------

If a shutdownMicroprocess message is received on this component's "control"
inbox this it will pass it on out of its "signal" outbox and immediately
terminate.

NOTE: Termination is currently rather cludgy - it raises an exception which
will cause the rest of a kamaelia system to halt. Do not rely on this behaviour
as it will be changed to provide cleaner termination at some point.



Customising the 3D topology viewer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can customise:

- the 'types' of particles (nodes)
- visual appearance of particles (nodes) and the links between them;
- the physics laws used to assist with layout

Use the particleTypes argument of the initialiser to specify classes that
should be instantiated to render each type of particle (nodes). particleTypes 
should be a dictionary mapping names for particle types to the respective 
classes, for example::

    { "major" : BigParticle,  "minor"  : SmallParticle  }

See below for information on how to write your own particle classes.

Layout of the nodes on the surface is assisted by a physics model, provided
by an instance of the Kamaelia.Support.Particles.ParticleSystem class. Use 
Kamaelia.Support.Particles.ParticleSystemX if you want to make some particles
not subject to the law.

Customise the laws used for each particle type by providing a
Kamaelia.Phyics.Simple.MultipleLaws object at initialisation.



Writing your own particle class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

should inherit from Kamaelia.PhysicsGraph3D.Particle3D.Particle3D 
and implement the following method (for rendering purposes):

    draw()
        draw OpenGL particles and links in this method.



TODO: Reduce CPU usage, improve responsive speed



References: 1. Kamaelia.Visualisation.PhysicsGraph.TopologyViewer
2. Kamaelia.UI.OpenGL.OpenGLComponent
3. Kamaelia.UI.OpenGL.MatchedTranslationInteractor
"""

import math, random
import time
import re
import sys
import pygame

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import Axon
import Kamaelia.Support.Particles

from Kamaelia.UI.OpenGL.OpenGLDisplay import OpenGLDisplay
from Kamaelia.UI.OpenGL.Vector import Vector
from Kamaelia.UI.OpenGL.Intersect import Intersect

_cat = Axon.CoordinatingAssistantTracker

from Particles3D import CuboidParticle3D, SphereParticle3D, TeapotParticle3D
from Kamaelia.Support.Particles.ParticleSystemX import ParticleSystemWithAvoidedList as ParticleSystemX

                 
class TopologyViewer3D(Axon.Component.component):
    """\
    TopologyViewer3D(...) -> new TopologyViewer3D component.
    
    A component that takes incoming topology (change) data and displays it live
    using pygame OpenGL. A simple physics model assists with visual layout. Particle
    types, appearance and physics interactions can be customised.
    
    Keyword arguments (in order):
    
    - screensize          -- (width,height) of the display area (default = (800,600))
    - fullscreen          -- True to start up in fullscreen mode (default = False)
    - caption             -- Caption for the pygame window (default = "Topology Viewer")
    - particleTypes       -- dict("type" -> klass) mapping types of particle to classes used to render them (default = {"-":RenderingParticle})
    - initialTopology     -- (nodes,bonds) where bonds=list((src,dst)) starting state for the topology  (default=([],[]))
    - laws                -- Physics laws to apply between particles (default = SimpleLaws(bondlength=100))
    - simCyclesPerRedraw  -- number of physics sim cycles to run between each redraw (default=1)
    - border              -- Minimum distance from edge of display area that new particles appear (default=100)
    """
    
    Inboxes = { "inbox"          : "Topology (change) data describing an Axon system",
                "control"        : "Shutdown signalling",
                "alphacontrol"   : "Alpha (transparency) of the image (value 0..255)",
                "callback"       : "for the response after a displayrequest",
                "events"         : "Place where we recieve events from the outside world",
                "displaycontrol" : "Replies from OpenGL Display service",
              }
              
    Outboxes = { "signal"         : "NOT USED",
                 "outbox"         : "Notification and topology output",
                 "display_signal" : "Requests to Pygame Display service",
               }
                                                     
    
    def __init__(self, screensize         = (800,600),
                       fullscreen         = False, 
                       caption            = "3D Topology Viewer", 
                       particleTypes      = None,
                       initialTopology    = None,
                       laws               = None,
                       simCyclesPerRedraw = 1,
                       border             = 0):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        
        super(TopologyViewer3D, self).__init__()
        
        glutInit(sys.argv)
        
        tracker = _cat.coordinatingassistanttracker.getcat()
        try:
            self.display = tracker.retrieveService("ogl_display")[0]
        except KeyError:
            self.display = OpenGLDisplay(width=screensize[0], height=screensize[1],fullscreen=fullscreen,
                                    title=caption)
            self.display.activate()
            OpenGLDisplay.setDisplayService(self.display, tracker)
        self.display = OpenGLDisplay.getDisplayService()[0]                
        self.link((self,"display_signal"), (self.display,"notify"))
        self.link((self.display,"signal"), (self,"control"))
        
        self.border = border
        
        if particleTypes == None:
            self.particleTypes = {"-":CuboidParticle3D, "cuboid":CuboidParticle3D, "sphere":SphereParticle3D,
                                  "teapot":TeapotParticle3D}
        else:
            self.particleTypes = particleTypes
            
        if initialTopology == None:
            initialTopology = ([],[])
        self.initialNodes   = list(initialTopology[0])
        self.initialBonds   = list(initialTopology[1])
        
        self.hitParticles = []
        self.multiSelectMode = False
        self.selectedParticles = []
        self.grabbed = False
        self.rotationMode = False  
        
        if laws==None:
            self.laws = Kamaelia.Support.Particles.SimpleLaws(bondLength=2)
        else:
            self.laws = laws
            
        self.physics = ParticleSystemX(self.laws, [], 0)
        self.biggestRadius = 0
        
        # Do interaction
        self.simCyclesPerRedraw = simCyclesPerRedraw
        self.lastIdleTime = time.time()
        
        # Tell if new node is added; if true, new id needs adding to OpenGLDisplay list
        self.isNewNode = False
        
        # For hierarchy structure
        self.maxLevel = 0
        self.currentLevel = 0
        self.previousParentParticleID = self.currentParentParticleID = ''
        self.viewerOldPos = Vector()
        self.levelViewerPos = {}
        # The Physics particle system of current display level for display
        self.currentDisplayedPhysics = ParticleSystemX(self.laws, [], 0)
        
        # For double click
        self.lastClickPos = (0,0)
        self.lastClickTime = time.time()
        self.dClickRes = 0.3
    
    def initialiseComponent(self):
        """Initialises."""
        self.addListenEvents( [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.KEYDOWN, pygame.KEYUP ])
        pygame.key.set_repeat(100,100)
        
        for node in self.initialNodes:
            self.addParticle(*node)

        for source,dest in self.initialBonds:
            self.makeBond(source, dest)
    
    def main(self):
        """Main loop."""
        # create display request for itself
        self.size = Vector(0,0,0)
        disprequest = { "OGL_DISPLAYREQUEST" : True,
                             "objectid" : id(self),
                             "callback" : (self,"callback"),
                             "events" : (self, "events"),
                             "size": self.size
                           }
        # send display request
        self.send(disprequest, "display_signal")        
        # wait for response on displayrequest and get identifier of the viewer
        while not self.dataReady("callback"):  yield 1
        self.identifier = self.recv("callback")
        
        self.initialiseComponent()
        
        while True:
            # process incoming messages
            if self.dataReady("inbox"):
                message = self.recv("inbox")
                self.doCommand(message)

                # wait for response on displayrequest and get identifier of the particle
                if self.isNewNode:
                    while not self.dataReady("callback"):  yield 1
                    self.physics.particles[-1].identifier = self.recv("callback")
                    self.isNewNode = False
            else:
                self.lastIdleTime = 0
            
            yield 1        
            
            if self.lastIdleTime + 1.0 < time.time():
                #print [particle.pos for particle in self.physics.particles]
                avoidedList = []
                avoidedList.extend(self.hitParticles)
                avoidedList.extend(self.selectedParticles)
                
                
                # Do interaction between particles
                self.currentDisplayedPhysics.run(self.simCyclesPerRedraw, avoidedList=avoidedList)
                #print [particle.pos for particle in self.physics.particles]
                
                # Draw particles if new or updated
                for particle in self.currentDisplayedPhysics.particles:
                    if particle.needRedraw:
                        self.drawParticles(particle)
                        #particle.needRedraw = False                        
                
                self.handleEvents()
                
                # Perform transformation
                for particle in self.currentDisplayedPhysics.particles:
                    transform_update = particle.applyTransforms()
                    if transform_update is not None:
                        self.send(transform_update, "display_signal")
                        #print transform_update
                        #print [particle.pos for particle in self.physics.particles]
                
                self.lastIdleTime = time.time()
            else:
                yield 1
            if self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, Axon.Ipc.shutdownMicroprocess):
                    self.quit(msg)
            
    def quit(self,msg=Axon.Ipc.shutdownMicroprocess()):
        """Cause termination."""
        print 'Shut down...'
        self.send(msg, "signal")
        self.scheduler.stop()
    
    def draw(self):
        """\
        Dummy method reserved for future use
        
        Invoke draw() and save its commands to a newly generated displaylist.
        
        The displaylist name is then sent to the display service via a
        "DISPLAYLIST_UPDATE" request.
        """
        pass
    
    def drawParticles(self, *particles):
        for particle in particles:
            # display list id
            displaylist = glGenLists(1)
            # draw object to its displaylist
            glNewList(displaylist, GL_COMPILE)
            particle.draw()
            glEndList()
    
            #print displaylist
            dl_update = { "DISPLAYLIST_UPDATE": True,
                          "objectid": id(particle),
                          "displaylist": displaylist
                        }
            self.send(dl_update, "display_signal")
    
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
                       
    def handleEvents(self):
        """Handle events."""
        while self.dataReady("events"):
            event = self.recv("events")
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
                self.handleMouseEvents(event)
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self.handleKeyEvents(event)
                
            # Scroll if self.display.viewerposition changes
            if self.display.viewerposition.copy() != self.viewerOldPos:
                self.scroll()
                self.viewerOldPos = self.display.viewerposition.copy()
    #                for particle in self.currentDisplayedPhysics.particles:
    #                    particle.oldpoint = None
    
    def handleMouseEvents(self, event):
        """Handle mouse events."""
        if event.type == pygame.MOUSEBUTTONDOWN or pygame.MOUSEMOTION and self.grabbed:
            if not self.rotationMode:
                for particle in self.hitParticles:
                    p1 = Vector(*particle.pos).copy()
                    p1.x += 10
                    p2 = Vector(*particle.pos).copy()
                    p2.y += 10
                    # Get the position of mouse
                    #z = Intersect.ray_Plane(Vector(0,0,0), event.direction, [Vector(*particle.pos)-self.display.viewerposition, p1, p2])
                    z = Intersect.ray_Plane(Vector(0,0,0), event.direction, [Vector(*particle.pos)-Vector(0,0,self.display.viewerposition.z), p1-Vector(0,0,self.display.viewerposition.z), p2-Vector(0,0,self.display.viewerposition.z)])
                    newpoint = event.direction * z
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Handle double click
                clickPos = event.pos
                currentTime = time.time()
                elapsedTime = currentTime - self.lastClickTime
                # If it's a double-click
                if clickPos == self.lastClickPos and elapsedTime<self.dClickRes:
                    if self.currentLevel < self.maxLevel and len(self.selectedParticles) == 1:
                        hasChildParticles = False
                        for particle in self.physics.particles:
                            if particle.ID.find(self.selectedParticles[0].ID) == 0 and particle.ID != self.selectedParticles[0].ID:
                                hasChildParticles = True
                                break
                        if hasChildParticles:
                            self.previousParentParticleID = self.currentParentParticleID
                            self.currentParentParticleID = self.selectedParticles[0].ID
                            self.gotoDisplayLevel(1)
                        else:
                            print 'Warning: The particle you double-clicked has no children!'
                        
                    else:
                        if self.currentLevel == self.maxLevel:
                            print "Warning: max hierarchy level has reached!"
                        if len(self.selectedParticles) != 1:
                            print "Tips: To extend a node, please double-click the node you want to extend"
                else: # Single click
                    if not self.rotationMode: # Select particle
                        for particle in self.currentDisplayedPhysics.particles:
                            if particle.identifier in event.hitobjects:
                                #particle.oldpos = particle.oldpos - self.display.viewerposition
                                self.grabbed = True
                                #particle.scaling = Vector(0.9,0.9,0.9)
                                self.hitParticles.append(particle)
                                self.selectParticle(particle)
                                #print str(id(particle))+'hit'
                                #print self.hitParticles
                        # If click places other than particles in non multiSelectMode, deselect all
                        if not self.hitParticles and not self.multiSelectMode:
                            self.deselectAll()
                self.lastClickPos = clickPos
                self.lastClickTime = currentTime
            if event.button == 3: # Right-clicked
                if self.currentLevel > 0:
                    self.previousParentParticleID = self.currentParentParticleID
                    items = self.currentParentParticleID.split(':')
                    items.pop()
                    self.currentParentParticleID = ':'.join(items)
                    self.gotoDisplayLevel(-1)
                else:
                    print "Warning: The first hierarchy level has reached!"
            if event.button == 4: # Scrolled-up: zoom out
                if self.selectedParticles:
                    particles = self.selectedParticles
                else:
                    particles = self.currentDisplayedPhysics.particles
                for particle in particles:
                    posVector = Vector(*particle.pos)
                    posVector.z -= 1
                    particle.pos = posVector.toTuple()
            if event.button == 5: # Scrolled-down: zoom in
                if self.selectedParticles:
                    particles = self.selectedParticles
                else:
                    particles = self.currentDisplayedPhysics.particles
                for particle in particles:
                    posVector = Vector(*particle.pos)
                    posVector.z += 1
                    particle.pos = posVector.toTuple()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  
                for particle in self.hitParticles:
                    self.grabbed = False
                    particle.oldpoint = None
                    #particle.scaling = Vector(1,1,1)
                    self.hitParticles.pop(self.hitParticles.index(particle))
                    #print self.hitParticles
        if event.type == pygame.MOUSEMOTION: 
            if not self.rotationMode and self.grabbed: # Drag particles
                for particle in self.hitParticles:
                    try:
                        if particle.oldpoint is not None:
                            #print particle.pos
                            diff = newpoint-particle.oldpoint
                            amount = (diff.x, diff.y)
                            particle.pos = (Vector(*particle.pos)+Vector(*amount)).toTuple()
                    except NameError: pass
                    
                    # Redraw the link so that the link can move with the particle
                    for p in particle.bondedFrom:
                        p.needRedraw = True
            elif self.rotationMode: # Rotate particles
                dAnglex = float(event.rel[1])*math.pi/180
                dAngley = -float(event.rel[0])*math.pi/180
                self.rotateParticles(self.selectedParticles, (dAnglex,dAngley,0))
        
        try:
            for particle in self.hitParticles:
                particle.oldpoint = newpoint                    
        except NameError: pass    
    
    def handleKeyEvents(self, event):
        """Handle keyboard events."""            
        # Keyboard events handling
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quit()
            elif event.key == pygame.K_BACKSPACE:
                if self.currentLevel > 0:
                    self.previousParentParticleID = self.currentParentParticleID
                    items = self.currentParentParticleID.split(':')
                    items.pop()
                    self.currentParentParticleID = ':'.join(items)
                    self.gotoDisplayLevel(-1)
                else:
                    print "Warning: The first hierarchy level has reached!"
            elif event.key == pygame.K_RETURN:
                if self.currentLevel < self.maxLevel and len(self.selectedParticles) == 1:
                    hasChildParticles = False
                    for particle in self.physics.particles:
                        if particle.ID.find(self.selectedParticles[0].ID) == 0 and particle.ID != self.selectedParticles[0].ID:
                            hasChildParticles = True
                            break
                    if hasChildParticles:
                        self.previousParentParticleID = self.currentParentParticleID
                        self.currentParentParticleID = self.selectedParticles[0].ID
                        self.gotoDisplayLevel(1)
                    else:
                        print 'Warning: The particle you double-clicked has no children!'
                else:
                    if self.currentLevel == self.maxLevel:
                        print "Warning: max hierarchy level has reached!"
                    if len(self.selectedParticles) != 1:
                        print "Tips: To extend a node, please click to select the node (only one) you want to extend first."
                    
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                self.multiSelectMode = True
            elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                self.rotationMode = True
            # Change viewer position
            elif event.key == pygame.K_PAGEUP:
                self.display.viewerposition.z -= 0.5
            elif event.key == pygame.K_PAGEDOWN:
                self.display.viewerposition.z += 0.5
            elif event.key == pygame.K_w:
                self.display.viewerposition.y += 0.5
            elif event.key == pygame.K_s:
                self.display.viewerposition.y -= 0.5
            elif event.key == pygame.K_a:
                self.display.viewerposition.x -= 0.5
            elif event.key == pygame.K_d:
                self.display.viewerposition.x += 0.5
            # Rotate particles
            elif event.key == pygame.K_UP:
                self.rotateParticles(self.selectedParticles, (-20*math.pi/180,0,0))      
            elif event.key == pygame.K_DOWN:
                self.rotateParticles(self.selectedParticles, (20*math.pi/180,0,0))      
            elif event.key == pygame.K_LEFT:
                self.rotateParticles(self.selectedParticles, (0,20*math.pi/180,0))    
            elif event.key == pygame.K_RIGHT:
                self.rotateParticles(self.selectedParticles, (0,-20*math.pi/180,0))
            elif event.key == pygame.K_COMMA:
                self.rotateParticles(self.selectedParticles, (0,0,20*math.pi/180))    
            elif event.key == pygame.K_PERIOD:
                self.rotateParticles(self.selectedParticles, (0,0,-20*math.pi/180))
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                # Return to normal mode from multiSelectMode
                self.multiSelectMode = False
            elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                # Return to normal mode from rotationMode
                self.rotationMode = False                 
    
    def scroll( self ):
        """Scroll the surface by resetting gluLookAt."""
        glMatrixMode(GL_PROJECTION)                 
        glLoadIdentity()
        self.display.setProjection()
        
    def rotateParticles( self, particles, dAngle ):
        """Rotate the particles."""
        if particles == []:
            particles = self.currentDisplayedPhysics.particles
        centrePoint = Vector() 
        for particle in particles:
            posVector = Vector(*particle.pos)
            centrePoint += posVector
        centrePoint /= len(particles)
        if dAngle[0] != 0: 
            for particle in particles:
                posVector = Vector(*particle.pos)
                relativePosVector = posVector - centrePoint
                radius = (relativePosVector.z*relativePosVector.z+relativePosVector.y*relativePosVector.y)**0.5
                newAngle = (math.atan2(relativePosVector.z,relativePosVector.y)+dAngle[0])
                particle.pos = (posVector.x, radius*math.cos(newAngle)+centrePoint.y, radius*math.sin(newAngle)+centrePoint.z)
                particle.drotation = Vector(dAngle[0]*180/math.pi,0,0)
        if dAngle[1] != 0:     
            for particle in particles:
                    posVector = Vector(*particle.pos)
                    relativePosVector = posVector - centrePoint
                    radius = (relativePosVector.z*relativePosVector.z+relativePosVector.x*relativePosVector.x)**0.5
                    newAngle = (math.atan2(relativePosVector.z,relativePosVector.x)+dAngle[1])
                    particle.pos = (radius*math.cos(newAngle)+centrePoint.x, posVector.y, radius*math.sin(newAngle)+centrePoint.z)
                    particle.drotation = Vector(0,-dAngle[1]*180/math.pi,0)
        if dAngle[2] != 0:
            for particle in particles:
                posVector = Vector(*particle.pos)
                relativePosVector = posVector - centrePoint
                radius = (relativePosVector.x*relativePosVector.x+relativePosVector.y*relativePosVector.y)**0.5
                newAngle = (math.atan2(relativePosVector.y,relativePosVector.x)+dAngle[2])
                particle.pos = (radius*math.cos(newAngle)+centrePoint.x, radius*math.sin(newAngle)+centrePoint.y, posVector.z)
                particle.drotation = Vector(0,0,dAngle[2]*180/math.pi)
        
        particle.drotation %= 360
        
    def gotoDisplayLevel( self, dlevel):
        """Switch to another display level."""
        # Save current level's viewer position
        self.levelViewerPos[self.currentLevel, self.previousParentParticleID] = self.display.viewerposition.copy()
        # Deselect all
        self.deselectAll()
        # Display next level
        self.currentLevel += dlevel
        # Reset viewer position to previous
        try:
            self.display.viewerposition = self.levelViewerPos[self.currentLevel, self.currentParentParticleID].copy()
        except KeyError:
            self.display.viewerposition = self.levelViewerPos[self.currentLevel, self.currentParentParticleID] = Vector()
        # Remove current displayed particles
        for particle in self.currentDisplayedPhysics.particles:
            self.display.ogl_displaylists.pop(id(particle))
            self.display.ogl_transforms.pop(id(particle))
        self.currentDisplayedPhysics.removeByID(*self.currentDisplayedPhysics.particleDict.keys())
        
        # Add current level's particles to self.currentDisplayedPhysics.particles for display
        self.currentDisplayedPhysics.particles = []
        if self.physics.particles != []:
            for particle in self.physics.particles:
                if self.currentParentParticleID == '': # If no parent, it's the top level 
                    if ':' not in particle.ID:
                        self.currentDisplayedPhysics.add( particle )
                        particle.oldpos = particle.initialpos
                # The child particles of self.currentParentParticleID
                elif particle.ID.find(self.currentParentParticleID) == 0 and particle.ID.count(':') == self.currentLevel:
                    self.currentDisplayedPhysics.add( particle )
                    particle.oldpos = particle.initialpos
                            
    def doCommand(self, msg):
        """\
        Proceses a topology command tuple:
            [ "ADD", "NODE", <id>, <name>, <positionSpec>, <particle type> ] 
            [ "DEL", "NODE", <id> ]
            [ "ADD", "LINK", <id from>, <id to> ]
            [ "DEL", "LINK", <id from>, <id to> ]
            [ "DEL", "ALL" ]
            [ "GET", "ALL" ]
        """  
        if len(msg) >= 2:
            cmd = msg[0].upper(), msg[1].upper()
            
            if cmd == ("ADD", "NODE"):
                if len(msg) == 4:
                    msg += ['randompos', '-']
                elif len(msg) == 5:
                    msg += ['-']

            if cmd == ("ADD", "NODE") and len(msg) == 6:
                if msg[2] in [p.ID for p in self.physics.particles]:
                    print "Node exists, please use a new node ID!"
                else:
                    if self.particleTypes.has_key(msg[5]):
                        #print 'ADD NODE begin'
                        ptype = self.particleTypes[msg[5]]
                        ident    = msg[2]
                        name  = msg[3]
                        
                        posSpec = msg[4]
                        pos     = self._generatePos(posSpec)
                        #print pos
    
                        particle = ptype(position = pos, ID=ident, name=name)
                        
                        particle.originaltype = msg[5]
                        #self.particles.append(particle)
                        #print self.particles[0]
                        self.addParticle(particle)
                        self.isNewNode = True

            elif cmd == ("DEL", "NODE") and len(msg) == 3:
                    ident = msg[2]
                    self.removeParticle(ident)        
            
            elif cmd == ("ADD", "LINK") and len(msg) == 4:
                src = msg[2]
                dst = msg[3]
                self.makeBond(src, dst)
                
            elif cmd == ("DEL", "LINK") and len(msg) == 4:
                src = msg[2]
                dst = msg[3]
                self.breakBond(src, dst)
                
            elif cmd == ("DEL", "ALL") and len(msg) == 2:
                self.removeParticle(*self.physics.particleDict.keys())
                self.currentLevel = 0
                self.currentParentParticleID = ''
                
            elif cmd == ("GET", "ALL") and len(msg) == 2:
                topology = [("DEL","ALL")]
                topology.extend(self.getTopology())
                self.send( ("TOPOLOGY", topology), "outbox" )
            
            elif cmd == ("UPDATE_NAME", "NODE") and len(msg) == 4:
                node_id = msg[2]
                new_name = msg[3]
                self.updateParticleLabel(node_id, new_name)
                self.send( ("UPDATE_NAME", "NODE", node_id, new_name), "outbox" )
            elif cmd == ("GET_NAME", "NODE") and len(msg) == 3:
                node_id = msg[2]
                name = self.getParticleLabel(node_id)
                self.send( ("GET_NAME", "NODE", node_id, name), "outbox" )        
            else:
                print "Command Error: please check your command format!"
        else:
            print "Command Error: not enough parameters!"
  
    def _generatePos(self, posSpec):
        """\
        generateXY(posSpec) -> (x,y,z) or raises ValueError
        
        posSpec == "randompos" or "auto" -> random (x,y,z) within the surface (specified border distance in from the edege)
        posSpec == "(XXX,YYY,ZZZ)" -> specified x,y,z (positive or negative integers)
        """
        posSpec = posSpec.lower()
        if posSpec == "randompos" or posSpec == "auto" :
            # FIXME: need to consider camera/ viewer setting            
            zLim = self.display.nearPlaneDist, self.display.farPlaneDist                        
            z = -1*random.randrange(int((zLim[1]-zLim[0])/20)+self.border,int((zLim[1]-zLim[0])/8)-self.border,1)
            yLim = z*math.tan(self.display.perspectiveAngle*math.pi/360.0), -z*math.tan(self.display.perspectiveAngle*math.pi/360.0)            
            xLim = yLim[0]*self.display.aspectRatio, yLim[1]*self.display.aspectRatio
            y = random.randrange(int(yLim[0])+self.border,int(yLim[1])-self.border,1)
            x = random.randrange(int(xLim[0])+self.border,int(xLim[1])-self.border,1)
            #print x,y,z
            return x,y,z            

        else:
            match = re.match("^([+-]?\d+),([+-]?\d+),([+-]?\d+)$", posSpec)
            if match:
                x = int(match.group(1))
                y = int(match.group(2))
                z = int(match.group(3))
                return x,y,z            
        
        raise ValueError("Unrecognised position specification")

    def addParticle(self, *particles):
        """Add particles to the system"""
        for p in particles:
            if p.radius > self.biggestRadius:
                self.biggestRadius = p.radius
            pLevel = p.ID.count(':')
            if self.maxLevel < pLevel:
                self.maxLevel = pLevel
            # create display request for every particle added
            disprequest = { "OGL_DISPLAYREQUEST" : True,
                                 "objectid" : id(p),
                                 "callback" : (self,"callback"),
                                 "events" : (self, "events"),
                                 "size": p.size
                               }
            # send display request
            self.send(disprequest, "display_signal")
        self.physics.add( *particles )
        
        # Add new particles to self.currentDisplayedPhysics
        for particle in particles:
            if self.currentParentParticleID == '': # If no parent, it's the top level 
                if ':' not in particle.ID:
                    self.currentDisplayedPhysics.add( particle )
                    particle.oldpos = particle.initialpos
            # The child particles of self.currentParentParticleID
            elif particle.ID.find(self.currentParentParticleID) == 0 and particle.ID.count(':') == self.currentLevel:
                self.currentDisplayedPhysics.add( particle )
                particle.oldpos = particle.initialpos
        
    def removeParticle(self, *ids):
        """\
        Remove particle(s) specified by their ids.

        Also breaks any bonds to/from that particle.
        """
        for ident in ids:
            self.physics.particleDict[ident].breakAllBonds()
            try:
                self.display.ogl_objects.remove(id(self.physics.particleDict[ident]))
                self.display.ogl_names.pop(id(self.physics.particleDict[ident]))
                self.display.ogl_displaylists.pop(id(self.physics.particleDict[ident]))
                self.display.ogl_transforms.pop(id(self.physics.particleDict[ident]))
            except KeyError: pass
#            if self.selected == self.physics.particleDict[id]:
#                self.selectParticle(None)
        self.physics.removeByID(*ids)
        for ident in ids:
            try:
                self.currentDisplayedPhysics.removeByID(ident)
            except KeyError: pass
        #print self.currentDisplayedPhysics.particles
        #print self.physics.particles
        
    def selectParticle(self, particle):
        """Select the specified particle."""
        if self.multiSelectMode:
            if particle not in self.selectedParticles:
                particle.select()
                self.selectedParticles.append(particle)
                self.send( "('SELECT', 'NODE', '"+particle.name+"')", "outbox" )
            else:
                particle.deselect()
                self.selectedParticles.remove(particle)
                self.send( "('DESELECT', 'NODE', '"+particle.name+"')", "outbox" )
        else:
            self.deselectAll()
            self.selectedParticles = []
            particle.select()
            self.selectedParticles.append(particle)
            self.send( "('SELECT', 'NODE', '"+particle.name+"')", "outbox" )

    def deselectAll(self):
        """Deselect all particles."""
        for particle in self.selectedParticles:
            particle.deselect()
        self.selectedParticles = []
    
    def makeBond(self, source, dest):
        """Make a bond from source to destination particle, specified by IDs"""
        self.physics.particleDict[source].makeBond(self.physics.particleDict, dest)
        self.physics.particleDict[source].needRedraw = True

    def breakBond(self, source, dest):
        """Break a bond from source to destination particle, specified by IDs"""
        self.physics.particleDict[source].breakBond(self.physics.particleDict, dest)
        self.physics.particleDict[source].needRedraw = True
        
    def updateParticleLabel(self, node_id, new_name):
        """\
        updateParticleLabel(node_id, new_name) -> updates the given nodes name & visual label if it exists
        
        node_id - an id for an already existing node
        new_name - a string (may include spaces) defining the new node name
        """
        for p in self.physics.particles:
            if p.ID == node_id:
                p.set_label(new_name)
                p.needRedraw = True
                return

    def getParticleLabel(self, node_id):
        """\
        getParticleLabel(node_id) -> particle's name
        
        Returns the name/label of the specified particle.
        """
        for p in self.physics.particles:
            if p.ID == node_id:
                return p.name
    
    def getTopology(self):
        """getTopology() -> list of command tuples that would build the current topology"""
        topology = []
        
        # first, enumerate the particles
        for particle in self.physics.particles:
            topology.append( ( "ADD","NODE",
                               particle.ID,
                               particle.name,
                               "random",
                               particle.originaltype
                           ) )
                           
        # now enumerate the linkages
        for particle in self.physics.particles:
            for dst in particle.getBondedTo():
                topology.append( ( "ADD","LINK", particle.ID, dst.ID ) )
            
        return topology
            
__kamaelia_components__  = ( TopologyViewer3D, )            

            
if __name__ == "__main__":
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
    from Kamaelia.Util.Console import ConsoleEchoer,ConsoleReader
    from Kamaelia.Chassis.Graphline import Graphline
    
    # Data can be from both DataSource and console inputs
    print "Please type the command you want to draw"
    Graphline(
        CONSOLEREADER = ConsoleReader(">>> "),
#        DATASOURCE = DataSource(['ADD NODE 1Node 1Node randompos -', 'ADD NODE 2Node 2Node randompos -',
#                                 'ADD NODE 3Node 3Node randompos -', 'ADD NODE 4Node 4Node randompos -',
#                                 'ADD LINK 1Node 2Node','ADD LINK 2Node 3Node', 'ADD LINK 3Node 4Node',
#                                 'ADD LINK 4Node 1Node']),
        DATASOURCE = DataSource(['ADD NODE 1Node 1Node randompos teapot',
                                 'ADD NODE 2Node 2Node randompos -',
                                 'ADD NODE 3Node 3Node randompos sphere', 'ADD NODE 4Node 4Node randompos -',
                                 'ADD NODE 5Node 5Node randompos sphere', 'ADD NODE 6Node 6Node randompos -',
                                 'ADD NODE 7Node 7Node randompos sphere',
                                 'ADD LINK 1Node 2Node',
                                 'ADD LINK 1Node 3Node', 'ADD LINK 1Node 4Node',
                                 'ADD LINK 1Node 5Node','ADD LINK 1Node 6Node', 'ADD LINK 1Node 7Node',
                                 'ADD NODE 1Node:1Node 1Node:1Node randompos -', 'ADD NODE 1Node:2Node 1Node:2Node randompos -',
                                 'ADD NODE 1Node:3Node 1Node:3Node randompos -', 'ADD NODE 1Node:4Node 1Node:4Node randompos -',
                                 'ADD LINK 1Node:1Node 1Node:2Node', 'ADD LINK 1Node:2Node 1Node:3Node',
                                 'ADD LINK 1Node:3Node 1Node:4Node', 'ADD LINK 1Node:4Node 1Node:1Node',
                                 'ADD NODE 1Node:1Node:1Node 1Node:1Node:1Node randompos -',
                                 'ADD NODE 1Node:1Node:2Node 1Node:1Node:2Node randompos -',
                                 'ADD LINK 1Node:1Node:1Node 1Node:1Node:2Node',
                                 'ADD NODE 5Node:1Node 5Node:1Node randompos sphere',
                                 'ADD NODE 5Node:2Node 5Node:2Node randompos sphere',
                                 'ADD LINK 5Node:1Node 5Node:2Node'
                                 ]),
        TOKENS = lines_to_tokenlists(),
        VIEWER = TopologyViewer3D(),
        CONSOLEECHOER = ConsoleEchoer(),
    linkages = {
        ("CONSOLEREADER","outbox") : ("TOKENS","inbox"),
        ("DATASOURCE","outbox") : ("TOKENS","inbox"),
        ("TOKENS","outbox")   : ("VIEWER","inbox"),
        ("VIEWER","outbox")  : ("CONSOLEECHOER","inbox"),
    }
).run()
                
