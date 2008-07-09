#!/usr/bin/env python

"""
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

import Axon
import Kamaelia.Support.Particles
import Kamaelia.UI

from Kamaelia.Visualisation.PhysicsGraph.GridRenderer import GridRenderer
from Kamaelia.Visualisation.PhysicsGraph.ParticleDragger import ParticleDragger
from Kamaelia.Visualisation.PhysicsGraph.RenderingParticle import RenderingParticle

from Kamaelia.UI.OpenGL.OpenGLComponent import OpenGLComponent
from Kamaelia.UI.OpenGL.OpenGLDisplay import OpenGLDisplay
from Kamaelia.UI.OpenGL.Vector import Vector
from Kamaelia.UI.OpenGL.Intersect import Intersect
from Kamaelia.UI.OpenGL.Transform import Transform

_cat = Axon.CoordinatingAssistantTracker

from Particles3D import Particle3D
from ParticleSystemX import ParticleSystemX

                 
class TopologyViewer3D(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    """\
   
    """
    
    Inboxes = { "inbox"          : "Topology (change) data describing an Axon system",
                "control"        : "Shutdown signalling",
                "alphacontrol"   : "Alpha (transparency) of the image (value 0..255)",
                "callback": "for the response after a displayrequest",
                "events"         : "Place where we recieve events from the outside world",
                "displaycontrol" : "Replies from Pygame Display service",
              }
              
    Outboxes = { "signal"        : "NOT USED",
                 "outbox"        : "Notification and topology output",
                 "display_signal" : "Requests to Pygame Display service",
               }
                                                     
    
    def __init__(self, screensize         = (800,600),
                       fullscreen         = False, 
                       caption            = "Topology Viewer", 
                       particleTypes      = None,
                       initialTopology    = None,
                       laws               = None,
                       simCyclesPerRedraw = 1,
                       border             = 0,
                       extraDrawing       = None,
                       showGrid           = True,
                       transparency       = None,
                       position           = None):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        
        super(TopologyViewer3D, self).__init__()
        
        tracker = _cat.coordinatingassistanttracker.getcat()
        self.display = OpenGLDisplay(width=screensize[0], height=screensize[1],fullscreen=fullscreen,
                                title=caption)
        self.display.activate()
        OpenGLDisplay.setDisplayService(self.display, tracker)                
        self.link((self,"display_signal"), (self.display,"notify"))
        
        self.border = border
        
        if particleTypes == None:
            self.particleTypes = {"-":Particle3D}
        else:
            self.particleTypes = particleTypes
            
        
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
        
        
    def main(self):
        """\
 
        
        """
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
        
        self.addListenEvents( [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.KEYDOWN, pygame.KEYUP ])
        
        while True:
            # process incoming messages
            if self.dataReady("inbox"):
                message = self.recv("inbox")
                self.doCommand(message)
                #print message

                # wait for response on displayrequest and get identifier of the particle
                cmd = message[0].upper(), message[1].upper()
                if cmd == ("ADD", "NODE") and len(message) == 6:
                    while not self.dataReady("callback"):  yield 1
                    self.physics.particles[-1].identifier = self.recv("callback")
            else:
                self.lastIdleTime = 0
            
            yield 1        
            
            if self.lastIdleTime + 1.0 < time.time():
                #print [particle.pos for particle in self.physics.particles]
                avoidedList = []
                avoidedList.extend(self.hitParticles)
                avoidedList.extend(self.selectedParticles)                    
                self.physics.run(self.simCyclesPerRedraw, avoidedList=avoidedList)
                #print [particle.pos for particle in self.physics.particles]
                
                # Draw particles if new or updated
                for particle in self.physics.particles:
                    if particle.needRedraw:
                        self.drawParticles(particle)
                        #particle.needRedraw = False                        
                
                self.handleEvents()
                
                # Perform transformation
                for particle in self.physics.particles:
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
                    self.send(msg, "signal")
                    self.quit()
            
        
    
    
    def draw(self):
        """\
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
            
            
            
            #print particle
    
    
    
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
        """ Handle events. """
        while self.dataReady("events"):
            event = self.recv("events")
            if event.type == pygame.MOUSEBUTTONDOWN or pygame.MOUSEMOTION and self.grabbed:
                if not self.rotationMode:
                    for particle in self.hitParticles:
                        p1 = Vector(*particle.pos).copy()
                        p1.x += 10
                        p2 = Vector(*particle.pos).copy()
                        p2.y += 10
                        #z = Intersect.ray_Plane(Vector(0,0,0), event.direction, [Vector(*particle.pos)-self.display.viewerposition, p1, p2])
                        z = Intersect.ray_Plane(Vector(0,0,0), event.direction, [Vector(*particle.pos)-Vector(0,0,self.display.viewerposition.z), p1-Vector(0,0,self.display.viewerposition.z), p2-Vector(0,0,self.display.viewerposition.z)])
                        newpoint = event.direction * z
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not self.rotationMode:
                        for particle in self.physics.particles:
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
                if event.button == 4:
                    if self.selectedParticles:
                        particles = self.selectedParticles
                    else:
                        particles = self.physics.particles
                    for particle in particles:
                        posVector = Vector(*particle.pos)
                        posVector.z -= 1
                        particle.pos = posVector.toTuple()
                if event.button == 5:
                    if self.selectedParticles:
                        particles = self.selectedParticles
                    else:
                        particles = self.physics.particles
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
                if not self.rotationMode and self.grabbed: 
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
                elif self.rotationMode:
                    if self.selectedParticles:
                        particles = self.selectedParticles
                    else:
                        particles = self.physics.particles
                    
                    centrePoint = Vector() 
                    for particle in particles:
                        posVector = Vector(*particle.pos)
                        centrePoint += posVector
                    centrePoint /= len(particles)
                    dAnglex = float(event.rel[1])*math.pi/180
                    dAngley = -float(event.rel[0])*math.pi/180
                    for particle in particles:
                        posVector = Vector(*particle.pos)
                        relativePosVector = posVector - centrePoint
                        radius = (relativePosVector.z*relativePosVector.z+relativePosVector.y*relativePosVector.y)**0.5
                        newAnglex = (math.atan2(relativePosVector.z,relativePosVector.y)+dAnglex)
                        particle.pos = (posVector.x, radius*math.cos(newAnglex)+centrePoint.y, radius*math.sin(newAnglex)+centrePoint.z)
                        posVector = Vector(*particle.pos)
                        relativePosVector = posVector - centrePoint
                        radius = (relativePosVector.z*relativePosVector.z+relativePosVector.x*relativePosVector.x)**0.5
                        newAngley = (math.atan2(relativePosVector.z,relativePosVector.x)+dAngley)
                        particle.pos = (radius*math.cos(newAngley)+centrePoint.x, posVector.y, radius*math.sin(newAngley)+centrePoint.z)      
                        particle.drotation.y = float(event.rel[0])
                        particle.drotation.x = float(event.rel[1])
                        particle.drotation %= 360
            
            try:
                for particle in self.hitParticles:
                    particle.oldpoint = newpoint                    
            except NameError: pass    
                    
            # Keyboard events handling
            if event.type == pygame.KEYDOWN:
                #print self.display.viewerposition
                viewerOldPos = self.display.viewerposition.copy()
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.multiSelectMode = True
                elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.rotationMode = True
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
                elif event.key == pygame.K_UP:
                    if self.selectedParticles:
                        particles = self.selectedParticles
                    else:
                        particles = self.physics.particles
                    centrePoint = Vector() 
                    for particle in particles:
                        posVector = Vector(*particle.pos)
                        centrePoint += posVector
                    centrePoint /= len(particles)
                    dAngle = -20*math.pi/180
                    for particle in particles:
                        posVector = Vector(*particle.pos)
                        relativePosVector = posVector - centrePoint
                        radius = (relativePosVector.z*relativePosVector.z+relativePosVector.y*relativePosVector.y)**0.5
                        newAngle = (math.atan2(relativePosVector.z,relativePosVector.y)+dAngle)
                        particle.pos = (posVector.x, radius*math.cos(newAngle)+centrePoint.y, radius*math.sin(newAngle)+centrePoint.z)
                        particle.drotation = Vector(dAngle*180/math.pi,0,0)      
                elif event.key == pygame.K_DOWN:
                    if self.selectedParticles:
                        particles = self.selectedParticles
                    else:
                        particles = self.physics.particles
                    centrePoint = Vector() 
                    for particle in particles:
                        posVector = Vector(*particle.pos)
                        centrePoint += posVector
                    centrePoint /= len(particles)
                    dAngle = 20*math.pi/180
                    for particle in particles:
                        posVector = Vector(*particle.pos)
                        relativePosVector = posVector - centrePoint
                        radius = (relativePosVector.z*relativePosVector.z+relativePosVector.y*relativePosVector.y)**0.5
                        newAngle = (math.atan2(relativePosVector.z,relativePosVector.y)+dAngle)
                        particle.pos = (posVector.x, radius*math.cos(newAngle)+centrePoint.y, radius*math.sin(newAngle)+centrePoint.z)
                        particle.drotation = Vector(dAngle*180/math.pi,0,0) 
                elif event.key == pygame.K_LEFT:
                    if self.selectedParticles:
                        particles = self.selectedParticles
                    else:
                        particles = self.physics.particles
                    centrePoint = Vector() 
                    for particle in particles:
                        posVector = Vector(*particle.pos)
                        centrePoint += posVector
                    centrePoint /= len(particles)
                    dAngle = 20*math.pi/180
                    for particle in particles:
                        posVector = Vector(*particle.pos)
                        relativePosVector = posVector - centrePoint
                        radius = (relativePosVector.z*relativePosVector.z+relativePosVector.x*relativePosVector.x)**0.5
                        newAngle = (math.atan2(relativePosVector.z,relativePosVector.x)+dAngle)
                        particle.pos = (radius*math.cos(newAngle)+centrePoint.x, posVector.y, radius*math.sin(newAngle)+centrePoint.z)
                        particle.drotation = Vector(0,-dAngle*180/math.pi,0)
                elif event.key == pygame.K_RIGHT:
                    if self.selectedParticles:
                        particles = self.selectedParticles
                    else:
                        particles = self.physics.particles
                    centrePoint = Vector() 
                    for particle in particles:
                        posVector = Vector(*particle.pos)
                        centrePoint += posVector
                    centrePoint /= len(particles)
                    dAngle = -20*math.pi/180
                    for particle in particles:
                        posVector = Vector(*particle.pos)
                        relativePosVector = posVector - centrePoint
                        radius = (relativePosVector.z*relativePosVector.z+relativePosVector.x*relativePosVector.x)**0.5
                        newAngle = (math.atan2(relativePosVector.z,relativePosVector.x)+dAngle)
                        particle.pos = (radius*math.cos(newAngle)+centrePoint.x, posVector.y, radius*math.sin(newAngle)+centrePoint.z)
                        particle.drotation = Vector(0,-dAngle*180/math.pi,0)
                elif event.key == pygame.K_COMMA:
                    if self.selectedParticles:
                        particles = self.selectedParticles
                    else:
                        particles = self.physics.particles
                    centrePoint = Vector() 
                    for particle in particles:
                        posVector = Vector(*particle.pos)
                        centrePoint += posVector
                    centrePoint /= len(particles)
                    dAngle = 20*math.pi/180
                    for particle in particles:
                        posVector = Vector(*particle.pos)
                        relativePosVector = posVector - centrePoint
                        radius = (relativePosVector.x*relativePosVector.x+relativePosVector.y*relativePosVector.y)**0.5
                        newAngle = (math.atan2(relativePosVector.y,relativePosVector.x)+dAngle)
                        particle.pos = (radius*math.cos(newAngle)+centrePoint.x, radius*math.sin(newAngle)+centrePoint.y, posVector.z)
                        particle.drotation = Vector(0,0,dAngle*180/math.pi)
                elif event.key == pygame.K_PERIOD:
                    if self.selectedParticles:
                        particles = self.selectedParticles
                    else:
                        particles = self.physics.particles
                    centrePoint = Vector() 
                    for particle in particles:
                        posVector = Vector(*particle.pos)
                        centrePoint += posVector
                    centrePoint /= len(particles)
                    dAngle = -20*math.pi/180
                    for particle in particles:
                        posVector = Vector(*particle.pos)
                        relativePosVector = posVector - centrePoint
                        radius = (relativePosVector.x*relativePosVector.x+relativePosVector.y*relativePosVector.y)**0.5
                        newAngle = (math.atan2(relativePosVector.y,relativePosVector.x)+dAngle)
                        particle.pos = (radius*math.cos(newAngle)+centrePoint.x, radius*math.sin(newAngle)+centrePoint.y, posVector.z)
                        particle.drotation = Vector(0,0,dAngle*180/math.pi)
                
                #print self.display.viewerposition
                # Scroll if self.display.viewerposition changes
                if self.display.viewerposition.copy() != viewerOldPos:
                    self.scroll()
                    for particle in self.physics.particles:
                        particle.oldpoint = None
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.multiSelectMode = False
                elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.rotationMode = False                 
    
    def scroll( self ):
        # Scroll the surface by resetting gluLookAt
        glMatrixMode(GL_PROJECTION)                 
        glLoadIdentity()
        self.display.setProjection()
        
        
        
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
        #print 'doCommand'        

        if len(msg) >= 2:
            cmd = msg[0].upper(), msg[1].upper()

            if cmd == ("ADD", "NODE") and len(msg) == 6:
                #print 'ADD NODE begin'
                if self.particleTypes.has_key(msg[5]):
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
                    #print id(particle)
                    
                    #print 'ADD NODE end'
                
                
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
                raise "Command Error"
        else:
            raise "Command Error"

  
  
  
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
        DATASOURCE = DataSource(['ADD NODE 1Node 1Node randompos -'
                                 , 'ADD NODE 2Node 2Node randompos -',
                                 'ADD NODE 3Node 3Node randompos -', 'ADD NODE 4Node 4Node randompos -',
                                 'ADD NODE 5Node 5Node randompos -', 'ADD NODE 6Node 6Node randompos -',
                                 'ADD NODE 7Node 7Node randompos -',
                                 'ADD LINK 1Node 2Node'
                                 ,'ADD LINK 1Node 3Node', 'ADD LINK 1Node 4Node',
                                 'ADD LINK 1Node 5Node','ADD LINK 1Node 6Node', 'ADD LINK 1Node 7Node'
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
                
