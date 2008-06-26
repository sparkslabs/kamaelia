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

from THF.Kamaelia.UI.OpenGL.OpenGLComponent import OpenGLComponent
from THF.Kamaelia.UI.OpenGL.OpenGLDisplay import OpenGLDisplay
from THF.Kamaelia.UI.OpenGL.Vector import Vector
from THF.Kamaelia.UI.OpenGL.Intersect import Intersect

_cat = Axon.CoordinatingAssistantTracker

from Particles3D import Particle3D

                 
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
                       simCyclesPerRedraw = None,
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
            
        
        # TODO: will be replaced by ParticleSystem3D
        self.particles = []
        self.hitParticles = []
        
        self.grabbed = False
        
        
        
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
        
        self.addListenEvents( [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.KEYDOWN ])
        
        while True:
            # process incoming messages
            if self.dataReady("inbox"):
                message = self.recv("inbox")
                self.doCommand(message)
                #print message
                #print self.particles
                # Draw new particles
                self.draw()
                # wait for response on displayrequest and get identifier of the particle
                while not self.dataReady("callback"):  yield 1
                self.particles[-1].identifier = self.recv("callback")
            yield 1
            
            self.handleEvents()
            
            # Perform transformation
            for particle in self.particles:
                transform_update = particle.applyTransforms()
                if transform_update is not None:
                    self.send(transform_update, "display_signal")
                    #print transform_update

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
        self.drawParticles()
    
    def drawParticles(self):
        for particle in self.particles:
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
                    for particle in self.hitParticles:
                        p1 = particle.position.copy()
                        p1.x += 10
                        p2 = particle.position.copy()
                        p2.y += 10
                        z = Intersect.ray_Plane(Vector(0,0,0), event.direction, [particle.position, p1, p2])
                        newpoint = event.direction * z
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for particle in self.particles:
                        if particle.identifier in event.hitobjects:
                            self.grabbed = True
                            particle.scaling = Vector(0.9,0.9,0.9)
                            self.hitParticles.append(particle)
                            #print str(id(particle))+'hit'
                            #print self.hitParticles
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  
                    for particle in self.hitParticles:
                        self.grabbed = False
                        particle.scaling = Vector(1,1,1)
                        self.send( "('SELECT', 'NODE', '"+particle.name+"')", "outbox" )
                        self.hitParticles.pop(self.hitParticles.index(particle))
                        #print self.hitParticles
            if event.type == pygame.MOUSEMOTION and self.grabbed:  
                for particle in self.hitParticles:
                    try:
                        particle.position = newpoint
                    except NameError: pass
          
    
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
                    self.particles.append(particle)
                    #print self.particles[0]
                    #self.addParticle(particle)
                    
                    
                    # create display request for every particle added
                    disprequest = { "OGL_DISPLAYREQUEST" : True,
                                         "objectid" : id(particle),
                                         "callback" : (self,"callback"),
                                         "events" : (self, "events"),
                                         "size": particle.size
                                       }
                    # send display request
                    self.send(disprequest, "display_signal")
                    #print id(particle)
                    
                    #print 'ADD NODE end'
                            
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


    
    
            
            
            
if __name__ == "__main__":
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
    from Kamaelia.Util.Console import ConsoleEchoer,ConsoleReader
    from Kamaelia.Chassis.Pipeline import Pipeline
        
    Pipeline(
        #DataSource(['ADD NODE 1 1Node randompos -', 'ADD NODE 2 2Node randompos -']),
        ConsoleReader(">>> "),
        lines_to_tokenlists(),
        TopologyViewer3D(),
        ConsoleEchoer(),
    ).run()   
