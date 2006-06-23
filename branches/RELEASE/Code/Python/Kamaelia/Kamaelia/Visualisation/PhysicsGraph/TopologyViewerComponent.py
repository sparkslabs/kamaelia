#!/usr/bin/env python

# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
=======================
Generic Topology Viewer
=======================

Pygame based display of graph topologies. A simple physics model assists with
visual layout. Rendering and physics laws can be customised for specific
applications.



Example Usage
-------------
A simple console driven topology viewer::
    pipeline( ConsoleReader(),
              lines_to_tokenlists(),
              TopologyViewerComponent(),
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

TopologyViewerComponent manifests as a pygame display surface. As it is sent
topology information nodes and links between them will appear.

You can click a node with the mouse to select it. Depending on the application,
this may display additional data or, if integrated into another app,  have some
other effect.

Click and drag with the left mouse button to move nodes around. Note that a
simple physics model or repulsion and attraction forces is always active. This
causes nodes to move around to help make it visually clearer, however you may
still need to drag nodes about to tidy it up.

The surface on which the nodes appear is notionally infinite. Scroll around
using the arrow keys.

Press the 'f' key to toggle between windowed and fullscreen modes.




How does it work?
-----------------

TopologyViewerComponent is a specialisation of the Kamaeila.UI.MH.PyGameApp
component. See documentation for that component to understand how it obtains
and handles events for a pygame display surface.

A topology (graph) of nodes and links between them is rendered to the surface.

You can specify an initial topology by providing a list of instantiated
particles and another list of pairs of those particles to show how they are 
linked.

TopologyViewerComponent reponds to commands arriving at its "inbox" inbox
instructing it on how to change the topology. A command is a list/tuple.

Commands recognised are:

    [ "ADD", "NODE", <id>, <name>, <posSpec>, <particle type> ]
        Add a node, using:
        - id            -- a unique ID used to refer to the particle in other topology commands. Cannot be None.
        - name          -- string name label for the particle
        - posSpec       -- string describing initial x,y (see _generateXY)
        - particleType  -- particle type (default provided is "-", unless custom types are provided - see below)
      
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

TopologyViewerComponent sends any output to its "outbox" outbox in the same
list/tuple format as used for commands sent to its "inbox" inbox. The following
may be output:

    [ "SELECT", "NODE", <id> ]
        Notification that a given node has been selected.
    
    [ "SELECT", "NODE", None ]
       Notificaion that *no node* is now selected. 
        
    [ "ERROR", <error string> ]
        Notification of errors - eg. unrecognised commands arriving at the
        "inbox" inbox
        
    [ "TOPOLOGY", <topology command list> ]
        List of commands needed to build the topology, as it currently stands.
        The list will start with a ("DEL","ALL") command.
        This is sent in response to receiving a ("GET","ALL") command.

If a shutdownMicroprocess or producerFinished message is received on this
component's "control" inbox this it will pass it on out of its "signal" outbox
and immediately terminate.

NOTE: Termination is currently rather cludgy - it raises an exception which
will cause the rest of a kamaelia system to halt. Do not rely on this behaviour
 as it will be changed to provide cleaner termination at some point.


Customising the topology viewer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can customise:
- the 'types' of particles (nodes)
- visual appearance of particles (nodes) and the links between them;
- the physics laws used to assist with layout
- extra visual furniture to be rendered

For example, see Kamaelia.Visualisation.Axon.AxonVisualiserServer. This
component uses two types of particle - to represent components and
inboxes/outboxes. Each has a different visual appearance, and the laws acting
between them differ depending on which particle types are involved in the
interaction.

Use the particleTypes argument of the initialiser to specify classes that
should be instantiated to render each type of particle (nodes). particleTypes 
should be a dictionary mapping names for particle types to the respective 
classes, for example::
    { "major" : BigParticle,  "minor"  : SmallParticle  }

See below for information on how to write your own particle classes.

Layout of the nodes on the surface is assisted by a physics model, provided
by an instance of the Kamaelia.Physics.Simple.ParticleSystem class.

Customise the laws used for each particle type by providing a
Kamaelia.Phyics.Simple.MultipleLaws object at initialisation.


Writing your own particle class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

should inherit from Kamaelia.Physics.Simple.Particle and implement the following
methods (for rendering purposes):

    setOffset( (left,top) )
        Notification that the surface has been scrolled by the user. Particles 
        should adjust the coordinates at which they render. For example, a
        particle at (x, y) should be rendered at (x-left, y-top). You can
        assume, until setOffset(...) is called, that (left,top) is (0,0).
    
    select()
        Called to inform the particle that it is selected (has been clicked on)
    
    deselect()
        Called to inform the particle that is has been deselected.
    
    render(surface) -> generator
        Called to get a generator for multi-pass rendering of the particle (see
        below)
    
The coordinates of the particle are updated automatically both due to mouse 
dragging and due to the physics model. See Kamaelia.Physics.Simple.Particle for
more information.

The render(...) method should return a generator that will render the particle
itself and its links/bonds to other particles.

Rendering by the TopologyViewerComponent is multi-pass. This is done so that
irrespective of the order in which particles are chosen to be rendered,
things that need to be rendered before (underneath) other things can be done
consistently.

The generator should yield the number of the rendering pass it wishes to be
next called on. Each time it is subsequently called, it should perform the
rendering required for that pass. It then yields the number of the next required
pass or completes if there is no more rendering required. Passes go in
ascending numerical order.

For example, Kamaelia.Visualisation.PhysicsGraph.RenderingParticle renders in
two passes::
    def render(self, surface):
        yield 1
        # render lines for bonds *from* this particle *to* others
        yield 2
        # render a blob and the name label for the particle

...in this case it ensures that the blobs for the particles always appear
on top of the lines representing the bonds between them.

Note that rendering passes must be coded in ascending order, but the numbering
can otherwise be arbitrary: The first pass can be any value you like; subsequent
passes can also be any value, provided it is higher.

When writing rendering code for particle(s), make sure they all agree on who
should render what. It is inefficient if all bonds are being rendered twice.
For example, RenderingParticle only renders links *from* that particle *to*
another, but not in another direction.

"""

import random
import time
import re
import sys
import pygame

import Axon
import Kamaelia.Physics.Simple
import Kamaelia.UI

from GridRenderer import GridRenderer
from ParticleDragger import ParticleDragger
from RenderingParticle import RenderingParticle
                  
class TopologyViewerComponent(Kamaelia.UI.MH.PyGameApp,Axon.Component.component):
    """\
    TopologyViewerComponent(...) -> new TopologyViewerComponent component.
    
    A component that takes incoming topology (change) data and displays it live
    using pygame. A simple physics model assists with visual layout. Particle
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
    - extraDrawing        -- Optional extra object to be rendered (default=None)
    - showGrid            -- False, or True to show gridlines (default=True)
    - transparency        -- None, or (r,g,b) colour to make transparent
    - position            -- None, or (left,top) position for surface within pygame window
    """
    
    Inboxes = { "inbox"          : "Topology (change) data describing an Axon system",
                "control"        : "Shutdown signalling",
                "alphacontrol"   : "Alpha (transparency) of the image (value 0..255)",
                "events"         : "Place where we recieve events from the outside world",
                "displaycontrol" : "Replies from PygameDisplay service",
              }
              
    Outboxes = { "signal"        : "NOT USED",
                 "outbox"        : "Notification and topology output",
                 "displaysignal" : "Requests to PygameDisplay service",
               }
                                                     
    
    def __init__(self, screensize         = (800,600),
                       fullscreen         = False, 
                       caption            = "Topology Viewer", 
                       particleTypes      = None,
                       initialTopology    = None,
                       laws               = None,
                       simCyclesPerRedraw = None,
                       border             = 100,
                       extraDrawing       = None,
                       showGrid           = True,
                       transparency       = None,
                       position           = None):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""

        super(TopologyViewerComponent, self).__init__(screensize, caption, fullscreen, transparency=transparency, position=position)
        self.border = border
        pygame.mixer.quit()
        
        if particleTypes == None:
            self.particleTypes = {"-":RenderingParticle}
        else:
            self.particleTypes = particleTypes
            
        if initialTopology == None:
            initialTopology = ([],[])
        self.initialNodes   = list(initialTopology[0])
        self.initialBonds   = list(initialTopology[1])
        
        if laws==None:
            self.laws = Kamaelia.Physics.Simple.SimpleLaws(bondLength=100)
        else:
            self.laws = laws
            
        if simCyclesPerRedraw==None:
            self.simCyclesPerRedraw = 1
        else:
            self.simCyclesPerRedraw = simCyclesPerRedraw
        
        self.graphicalFurniture = []
        if showGrid:
           self.graphicalFurniture.append( GridRenderer(self.laws.maxInteractRadius, (200,200,200)) )
        if extraDrawing != None:
            self.graphicalFurniture.append(extraDrawing)
            
        self.biggestRadius = 0
        self.selectedParticle = None

        self.left  = 0
        self.top   = 0
        self.dleft = 0
        self.dtop  = 0
                 
        self.lastIdleTime = time.time()

        self.selected = None
          

    def initialiseComponent(self):
        """Initialises."""
        self.addHandler(pygame.MOUSEBUTTONDOWN, lambda event,self=self: ParticleDragger.handle(event,self))
        self.addHandler(pygame.KEYDOWN, self.keyDownHandler)
        self.addHandler(pygame.KEYUP,   self.keyUpHandler)
        
        self.physics = Kamaelia.Physics.Simple.ParticleSystem(self.laws, [], 0)
        
        for node in self.initialNodes:
           self.addParticle(*node)

        for source,dest in self.initialBonds:
           self.makeBond(source, dest)
        return 1

        
    def mainLoop(self):
        """\
        Main loop.
        
        Proceses commands from "inbox" inbox, runs physics simulation, then renders display
        """
        # process incoming messages
        if self.dataReady("inbox"):
            message = self.recv("inbox")
            self.doCommand(message)
        else:
            self.lastIdleTime = 0
        
        if self.dataReady("alphacontrol"):
            alpha = self.recv("alphacontrol")
            self.screen.set_alpha(alpha)
            
        if self.lastIdleTime + 1.0 < time.time():
            self.physics.run(self.simCyclesPerRedraw)
            
            # draw the background
            self.screen.fill( (255,255,255) )
    
            # scroll, if scrolling is active, increasing velocity over time
            if self.dleft != 0 or self.dtop != 0:
                self.scroll( (self.dleft, self.dtop) )
                if self.dleft:
                    self.dleft = self.dleft + 1 * abs(self.dleft)/self.dleft
                if self.dtop:
                    self.dtop  = self.dtop + 1 * abs(self.dtop)/self.dtop
            
            self.render()
            self.flip = True
            self.lastIdleTime = time.time()
        else:
            self.flip = False

        if self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, Axon.Ipc.producerFinished) or isinstance(msg, Axon.Ipc.shutdownMicroprocess):
                self.send(msg, "signal")
                self.quit()
            
        return 1
        
    def render(self):        
        """Render elements to self.screen"""
        # rendering is done in multiple passes
        # renderPasses is a dictionary of pass-number -> list of 'render' generators
        # each render generator yields the next pass number on which it wishes to be called
        renderPasses = {}

                
        # do the first pass - filling the renderPasses dictionary with rendering
        # generators from all particles, and also the extra furniture rendering 
        for p in self.graphicalFurniture + self.physics.particles:
            r = p.render(self.screen)
            if r != None:
                try:
                    n = r.next()
                    try:
                        renderPasses[n].append(r)
                    except KeyError:
                        renderPasses[n] = [r]
                except StopIteration:
                    pass
        
        # keep going through, extracting the lowers render pass number in the dictionary and
        # processing generators listed in it, until the renderPasses dictionary is empty
        while renderPasses:
            nextPass = reduce( min, renderPasses.keys() )
            for r in renderPasses.pop(nextPass):
                try:
                    n = r.next()
                    try:
                        renderPasses[n].append(r)
                    except KeyError:
                        renderPasses[n] = [r]
                except StopIteration:
                    pass
                    
        

    def keyDownHandler(self, event):
        """Handle keypresses:
           ESCAPE, Q : quits
           F         : toggles fullscreen mode
           arrows    : scroll the view
        """
        if event.key==pygame.K_ESCAPE or event.key==pygame.K_q:
            self.quit()
        elif event.key==pygame.K_f:
            pygame.display.toggle_fullscreen()
            
        elif event.key == pygame.K_UP:
            self.dtop = -4
        elif event.key == pygame.K_DOWN:
            self.dtop = +4
        elif event.key == pygame.K_LEFT:
            self.dleft = -4
        elif event.key == pygame.K_RIGHT:
            self.dleft = +4
    
    def keyUpHandler(self, event):
        """Handle releases of keys"""
        if event.key == pygame.K_UP:
            self.dtop = 0
        elif event.key == pygame.K_DOWN:
            self.dtop = 0
        elif event.key == pygame.K_LEFT:
            self.dleft = 0
        elif event.key == pygame.K_RIGHT:
            self.dleft = 0
            
    
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
        
        try:            
            if len(msg) >= 2:
                cmd = msg[0].upper(), msg[1].upper()
    
                if cmd == ("ADD", "NODE") and len(msg) == 6:
                    if self.particleTypes.has_key(msg[5]):
                        ptype = self.particleTypes[msg[5]]
                        id    = msg[2]
                        name  = msg[3]
                        
                        posSpec = msg[4]
                        pos     = self._generateXY(posSpec)

                        particle = ptype(position = pos, ID=id, name=name)
                        particle.originaltype = msg[5]
                        self.addParticle(particle)
                
                elif cmd == ("DEL", "NODE") and len(msg) == 3:
                    id = msg[2]
                    self.removeParticle(id)
                        
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

                elif cmd == ("GET", "ALL") and len(msg) == 2:
                    topology = [("DEL","ALL")]
                    topology.extend(self.getTopology())
                    self.send( ("TOPOLOGY", topology), "outbox" )
                elif cmd == ("UPDATE_NAME", "NODE") and len(msg) == 4:
                    node_id = msg[2]
                    new_name = msg[3]
                    self.updateParticleLabel(node_id, new_name)
                elif cmd == ("GET_NAME", "NODE") and len(msg) == 3:
                    node_id = msg[2]
                    name = self.getParticleLabel(node_id)
                    self.send( ("UPDATE_NAME", "NODE", node_id, name), "outbox" )
                else:
                    raise "Command Error"
            else:
                raise "Command Error"
        except:     
            import traceback
            errmsg = reduce(lambda a,b: a+b, traceback.format_exception(*sys.exc_info()) )
            self.send( ("ERROR", "Error processing message : "+str(msg) + " resason:\n"+errmsg), "outbox")
                                                    
    def updateParticleLabel(self, node_id, new_name):
        """\
        updateParticleLabel(node_id, new_name) -> updates the given nodes name & visual label if it exists
        
        node_id - an id for an already existing node
        new_name - a string (may include spaces) defining the new node name
        """
        for p in self.physics.particles:
            if p.ID == node_id:
                p.set_label(new_name)
                return

    def getParticleLabel(self, node_id):
        """\
        getParticleLabel(node_id) -> particle's name
        
        Returns the name/label of the specified particle.
        """
        for p in self.physics.particles:
            if p.ID == node_id:
                return p.name

    def _generateXY(self, posSpec):
        """\
        generateXY(posSpec) -> (x,y) or raises ValueError
        
        posSpec == "randompos" or "auto" -> random (x,y) within the surface (specified border distance in from the edege)
        posSpec == "(XXX,YYY)" -> specified x,y (positive or negative integers)
        """
        posSpec = posSpec.lower()
        if posSpec == "randompos" or posSpec == "auto" :
            x = self.left + random.randrange(self.border,self.screensize[0]-self.border,1)
            y = self.top  + random.randrange(self.border,self.screensize[1]-self.border,1)
            return x,y            

        else:
            match = re.match("^([+-]?\d+),([+-]?\d+)$", posSpec)
            if match:
                x = int(match.group(1))
                y = int(match.group(2))
                return x,y            
        
        raise ValueError("Unrecognised position specification")


        
    def addParticle(self, *particles):
        """Add particles to the system"""
        for p in particles:
            if p.radius > self.biggestRadius:
                self.biggestRadius = p.radius
            p.setOffset( (self.left, self.top) )
        self.physics.add( *particles )
        
    def removeParticle(self, *ids):
        """\
        Remove particle(s) specified by their ids.

        Also breaks any bonds to/from that particle.
        """
        for id in ids:
            self.physics.particleDict[id].breakAllBonds()
            if self.selected == self.physics.particleDict[id]:
                self.selectParticle(None)
        self.physics.removeByID(*ids)
        
    def makeBond(self, source, dest):
        """Make a bond from source to destination particle, specified by IDs"""
        self.physics.particleDict[source].makeBond(self.physics.particleDict, dest)

    def breakBond(self, source, dest):
        """Break a bond from source to destination particle, specified by IDs"""
        self.physics.particleDict[source].breakBond(self.physics.particleDict, dest)

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
        
    
    def quit(self, event=None):
        """Cause termination."""
        super(TopologyViewerComponent,self).quit(event)
        raise "QUITTING"           ### XXX VOMIT : need better shutdown than this!
        
    def scroll( self, (dx, dy) ):
        """Scroll the contents being displayed on the surface by (dx,dy) left and up."""
        self.left += dx
        self.top += dy
        for e in self.graphicalFurniture + self.physics.particles:
            e.setOffset( (self.left, self.top) )

    def selectParticle(self, particle):
        """Select the specified particle."""
        if self.selected != particle:
            
            if self.selected != None:
                self.selected.deselect()
                
            self.selected = particle
            nodeid = None
            if self.selected != None:
                self.selected.select()
                nodeid = self.selected.ID
            self.send( ("SELECT","NODE", nodeid), "outbox" )

__kamaelia_components__  = ( TopologyViewerComponent, )
        