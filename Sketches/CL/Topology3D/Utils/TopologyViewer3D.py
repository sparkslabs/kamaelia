#!/usr/bin/env python


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
        
    def main(self):
        """\
 
        
        """
        # create display request
        self.disprequest = { "OGL_DISPLAYREQUEST" : True,
                             "objectid" : id(self),
                             "callback" : (self,"callback"),
                             "events" : (self, "events"),
                             "size": (0.8,0.5,0.3)
                           }
        # send display request
        self.send(self.disprequest, "display_signal")
        
        particle = Particle3D(position = (-1,0,-10))
        self.particles.append(particle)
        
        self.draw()    
        # wait for response on displayrequest
        while not self.dataReady("callback"):  yield 1
        self.identifier = self.recv("callback")
        
        
        yield 1
        while True:
            # process incoming messages
            if self.dataReady("inbox"):
                message = self.recv("inbox")
                self.doCommand(message)
                print message
            yield 1
            
            
        
            if self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, Axon.Ipc.shutdownMicroprocess):
                    self.send(msg, "signal")
                    self.quit()
                    
            
            self.display.updateDisplay()
            
        
                    
    
            
    
    def draw(self):
        """\
        Invoke draw() and save its commands to a newly generated displaylist.
        
        The displaylist name is then sent to the display service via a
        "DISPLAYLIST_UPDATE" request.
        """
        # display list id
        displaylist = glGenLists(1)
        # draw object to its displaylist
        glNewList(displaylist, GL_COMPILE)
        self.drawParticles()
        glEndList()

        #print displaylist
        dl_update = { "DISPLAYLIST_UPDATE": True,
                      "objectid": id(self),
                      "displaylist": displaylist
                    }
        self.send(dl_update, "display_signal")
    
    def drawParticles(self):
        for particle in self.particles:
            particle.draw()
    
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
                        self.particles.append(particle)
                        #self.addParticle(particle)
                else:
                    raise "Command Error"
            else:
                raise "Command Error"
        except:     
            import traceback
            errmsg = reduce(lambda a,b: a+b, traceback.format_exception(*sys.exc_info()) )
            self.send( ("ERROR", "Error processing message : "+str(msg) + " resason:\n"+errmsg), "outbox")
  
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
            yLim = -zLim[1]*2.0*math.tan(self.display.perspectiveAngle*math.pi/360.0), zLim[1]*2.0*math.tan(self.display.perspectiveAngle*math.pi/360.0)
            xLim = yLim[0]*self.display.aspectRatio, yLim[1]*self.display.aspectRatio
            z = -1*random.randrange(int((zLim[1]-zLim[0])/10)+self.border,int((zLim[1]-zLim[0])/20)-self.border,1)
            y = random.randrange(int((yLim[1]-yLim[0]))+self.border,int((yLim[1]-yLim[0]))-self.border,1)
            x = random.randrange(int((xLim[1]-xLim[0]))+self.border,int((xLim[1]-xLim[0]))-self.border,1)
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
        #ConsoleEchoer(),
    ).run()   
