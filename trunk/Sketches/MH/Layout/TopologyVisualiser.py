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

# Simple topography viewer server - takes textual commands from a single socket
# and renders the appropriate graph

import pygame
from pygame.locals import *

import random, time, re, sys

from Axon.Scheduler import scheduler as _scheduler
import Axon as _Axon

import Physics
from Physics import Particle as BaseParticle
from PyGameApp import PyGameApp, DragHandler

component = _Axon.Component.component

from Kamaelia.Util.PipelineComponent import pipeline



class Particle(BaseParticle):
    """Version of Physics.Particle with added rendering functions.
    """

    def __init__(self, ID, position, name):
        super(Particle,self).__init__(position=position, ID = ID )
        self.radius = 20
        self.labelText = name
        
        font = pygame.font.Font(None, 24)
        self.label = font.render(self.labelText, False, (0,0,0))
       
    def render(self, surface):
        """Rendering passes. A generator method that renders in multiple passes.
        Use yields to specify a wait until the pass the next stage of rendering
        should take place at.
        
        Example, that renders bonds 'behind' the blobs.
            def render(self, surface):
                yield 1
                self.renderBonds(surface)        # render bonds on pass 1
                yield 5 
                self.renderSelf(surface)         # render 'blob' on pass 5
        
         If another particle type rendered, for example, on pass 3, then it
         would be rendered on top of the bonds, but behind the blobs.
         
         Use this mechanism to order rendering into layers.
         """
        yield 1
        self.renderBonds(surface)
        yield 2
        self.renderSelf(surface)
        
        
    def renderBonds(self, surface):
        """Renders lines representing the bonds going from this particle"""
        for p in self.bondedTo:
            pygame.draw.line(surface, (128,128,255), [int(i) for i in self.pos],  [int(i) for i in p.pos])
        
    def renderSelf(self, surface):
        """Renders a circle with the particle name in it"""
        pygame.draw.circle(surface, (255,128,128), (int(self.pos[0]), int(self.pos[1])), self.radius)
        surface.blit(self.label, (int(self.pos[0]) - self.label.get_width()/2, int(self.pos[1]) - self.label.get_height()/2))

        

class ParticleDragger(DragHandler):
     def detect(self, pos, button):
         inRange = self.app.physics.withinRadius( pos, self.app.biggestRadius )
         inRange = filter(lambda (p, rsquared) : p.radius*p.radius >= rsquared, inRange)
         
         nearestRS = self.app.biggestRadius ** 2 + 1
         for (p,rsquared) in inRange:
             if rsquared < nearestRS:
                 nearestRS = rsquared
                 nearest = p
                  
         if len(inRange) > 0:
             self.particle = p
             self.particle.freeze()
             return self.particle.getLoc()
         else:
             return False

     def drag(self,newx,newy):
         self.particle.pos = (newx,newy)
         self.app.physics.updateLoc(self.particle)

     def release(self,newx, newy):
         self.drag(newx, newy)
         self.particle.unFreeze()                

         
class TopologyViewerComponent(PyGameApp,component):
    """Generic Topology Viewer Component
    
       Displays a topology in a pygame application. It can be interacted
       with by dragging nodes with the mouse.
    
       Receives command tuples on its inbox. See handleCommunication()
       for command syntax.
       
       Outputs diagnostic and error messages on its outbox
       
       See keyHandler() for keyboard controls.
    """

    def __init__(self, screensize         = (640,480),
                       fullscreen         = False, 
                       caption            = "Topology Viewer", 
                       initialTopology    = None,
                       laws               = None,
                       simCyclesPerRedraw = None,
                       border             = 100,
                       extraDrawing       = None):
                       
        super(TopologyViewerComponent, self).__init__(screensize, caption, fullscreen)
        self.border = border
        
        if initialTopology == None:
            initialTopology = ([],[])
        self.initialNodes   = list(initialTopology[0])
        self.initialBonds   = list(initialTopology[1])
        
        if laws==None:
            self.laws = Physics.SimpleLaws(bondLength=100)
        else:
            self.laws = laws
            
        if simCyclesPerRedraw==None:
            self.simCyclesPerRedraw = 1
        else:
            self.simCyclesPerRedraw = simCyclesPerRedraw
        
        self.extraDrawing = extraDrawing
            
        self.biggestRadius = 0
          
          

    def initialiseComponent(self):
        self.addHandler(MOUSEBUTTONDOWN, lambda event: ParticleDragger(event,self))
        self.addHandler(KEYDOWN, self.keyHandler)
        
        self.physics = Physics.ParticleSystem(self.laws, [], 0)
        
        for node in self.initialNodes:
           self.makeParticle(*node)

        for source,dest in self.initialBonds:
           self.makeBond(source, dest)
        return 1

        
    def mainLoop(self):
        """Main loop.
           1) Processing incoming commands.
           2) Runs the physics simulation
           3) Draws the white graph paper
           4) Draws particles and any extra 'furniture'
        """
    
        # process incoming messages
        while self.dataReady("inbox"):
            message = self.recv("inbox")
            self.handleCommunication(message)
        
        self.physics.run(self.simCyclesPerRedraw)
        
        # draw the background
        self.screen.fill( (255,255,255) )
        self.drawGrid()
        
        # rendering is done in multiple passes
        # renderPasses is a dictionary of pass-number -> list of 'render' generators
        # each render generator yields the next pass number on which it wishes to be called
        renderPasses = {}

                
        extra = []
        if self.extraDrawing != None:
            extra = [self.extraDrawing]
                
        # do the first pass - filling the renderPasses dictionary with rendering
        # generators from all particles, and also the 'extra' rendering 
        for p in extra + self.physics.particles:
            r = p.render(self.screen)
            if r != None:
                try:
                    n = r.next()
                    if not renderPasses.has_key(n):
                        renderPasses[n] = [r]
                    else:
                        renderPasses[n].append(r)
                except StopIteration:
                    pass
        
        # keep going through, extracting the lowers render pass number in the dictionary and
        # processing generators listed in it, until the renderPasses dictionary is empty
        while renderPasses:
            nextPass = reduce( min, renderPasses.keys() )
            for r in renderPasses.pop(nextPass):
                try:
                    n = r.next()
                    if not renderPasses.has_key(n):
                        renderPasses[n] = [r]
                    else:
                        renderPasses[n].append(r)
                except StopIteration:
                    pass
                    
        return 1
        

    def keyHandler(self, event):
        """Handle keyboard input:
           ESCAPE, Q : quits
           F         : toggles fullscreen mode
        """
        if event.key==K_ESCAPE or event.key==K_q:
            self.quit()
        elif event.key==K_f:
            pygame.display.toggle_fullscreen()
        
            
    def handleCommunication(self,message):
        """Command processor
        
           Commands:
           ("+NODE", nodeFactory, posSpec)
               Add a node
               nodeFactory( (x,y) ) should return a particle
               posSpec is a string describing initial x,y (see _generateXY)
           
           ("-NODE", id)
               Remove a node (also removes all links to and from it)
        
           ("+LINK", fromId, toId)
               Add a link, directional from fromID to toID
           
           ("-LINK", fromId, toId)
               Remove a link, directional from fromID to toID
               
           ("-ALL", )
               Clears all nodes and links
        """
        
        try:
            if message[0] == "+NODE":
                ptype = message[1]
                argDict = message[2]
                posSpec = message[3]
                pos = self._generateXY(posSpec)
                particle = ptype(position = pos, **argDict)
                self.addParticle(particle)
                
            elif message[0] == "-NODE":
                id = message[1]
                self.removeParticle(id)
            
            elif message[0] == "+LINK":
                src, dst = message[1], message[2]
                self.makeBond(src, dst)
            
            elif message[0] == "-LINK":
                src, dst = message[1], message[2]
                self.breakBond(src, dst)
                                
            elif message[0] == "-ALL":
                self.removeParticle(*self.physics.particleDict.keys())
            
            else:
                raise
        except:     
            import traceback
            msg = reduce(lambda a,b: a+b, traceback.format_exception(*sys.exc_info()) )
            self.send("Error processing message : "+str(message) + " resason:\n"+msg, "outbox")

                
    def _generateXY(self, posSpec):
        """Takes a string specifying a position specification and returns
           a tuple (x,y). Raises ValueError if the specification is wrong"""
        posSpec = posSpec.lower()
        if posSpec == "randompos" or posSpec == "auto" :
            x = random.randrange(self.border,self.screensize[0]-self.border,1)
            y = random.randrange(self.border,self.screensize[1]-self.border,1)
            return x,y            

        else:
            match = re.match("^([+-]?[0-9]+),([+-]?[0-9]+)$", posSpec)
            if match:
                x = int(match.group(1))
                y = int(match.group(2))
                return x,y            
        
        raise ValueError("Unrecognised position specification")


        
    def addParticle(self, *particles):
        """Adds particles to the system"""
        for p in particles:
            if p.radius > self.biggestRadius:
                self.biggestRadius = p.radius
        self.physics.add( *particles )
        
    def removeParticle(self, *ids):
        """Removes particles from the system by ID.
           Also breaks bonds to/from that particle.
        """
        for id in ids:
            self.physics.particleDict[id].breakAllBonds()
        self.physics.removeByID(*ids)
        
    def makeBond(self, source, dest):
        """Make a bond from source to destination particle, specified by IDs"""
        self.physics.particleDict[source].makeBond(self.physics.particleDict, dest)

    def breakBond(self, source, dest):
        """Break a bond from source to destination particle, specified by IDs"""
        self.physics.particleDict[source].breakBond(self.physics.particleDict, dest)

    
    def quit(self, event=None):
        raise "QUITTING"
        
    def drawGrid(self):
        for i in range(0,self.screen.get_height(), int(self.laws.maxInteractRadius)):
            pygame.draw.line(self.screen, (200,200,200),
                             (0,i),
                             (self.screen.get_width(),i) )

        for i in range(0,self.screen.get_width(), int(self.laws.maxInteractRadius)):
            pygame.draw.line(self.screen, (200,200,200), 
                             (i,0), 
                             (i,self.screen.get_height()) )

                             

class topology_message_parser(component):
   """Parses textual messages for the topology viewer.
   
      Commands accepted are:
      ADD NODE <id> <name> <positionSpec> <particle type>
      DEL NODE <id>
      ADD LINK <id from> <id to>
      DEL LINK <id from> <id to>
      DEL ALL
   """

   def __init__(self, particleTypes = None):
      """particleTypes = dictionary mapping strings describing particle types
         to classes/factory methods that take named arguments:
             ID
             position : (x,y) tuple
             name
      """
      super(topology_message_parser, self).__init__()
      self._thread = self.main()
      
      if particleTypes == None:
          self.pTypes = {"-":Particle}
      else:
          self.pTypes = particleTypes

   def main(self):
      while 1:
         if self.dataReady("inbox"):
            line = self.recv("inbox")
            message = re.split("\s+",line.strip())
            
            if len(message) >= 2:
                cmd = message[0].upper(), message[1].upper()
                
                if cmd == ("ADD","NODE") and len(message) >= 6:
                    if self.pTypes.has_key(message[5]):
                        ptype = self.pTypes[message[5]]
                        id    = message[2]
                        name  = message[3]
                        posSpec = message[4]

                        self.send( ("+NODE", ptype, {"ID":id, "name":name}, posSpec), "outbox")

                
                elif cmd == ("ADD","LINK") and len(message) >= 4:
                    src = message[2]
                    dst = message[3]
                    self.send( ("+LINK", src,dst), "outbox")
                
                elif cmd == ("DEL","NODE") and len(message) >= 3:
                    id = message[2]
                    self.send( ("-NODE", id), "outbox")
                
                elif cmd == ("DEL","LINK") and len(message) >= 3:
                    src = message[2]
                    dst = message[3]
                    self.send( ("-LINK", src, dst), "outbox")
                    
                elif cmd == ("DEL", "ALL"):
                    self.send( ("-ALL",), "outbox")
            
            yield 1
         else:
            yield None



class chunks_to_lines(component):
   """Takes in chunked textual data and breaks it at line breaks into lines."""

   def main(self):
      gotLine = False
      line = ""
      while 1: 
         pos = line.find("\n")
         if pos > -1:
            self.send(line[:line.find("\n")], "outbox")
            line = line[line.find("\n")+1:] 
         else:
            if self.dataReady("inbox"):
               chunk = self.recv("inbox")
               chunk = chunk.replace("\r", "")
               line = line + chunk
            else:
               self.pause()
         yield 1


class TopologyViewerServer(pipeline):
    def __init__(self, particleTypes=None, serverPort = None, **dictArgs):
        """particleTypes = dictionary mapping names to particle classes
        
           All remaining named arguments are passed onto the TopologyViewerComponent
        """
        
        from Kamaelia.SingleServer import SingleServer
        from Kamaelia.Util.ConsoleEcho import consoleEchoer
        
        if serverPort == None:
            serverPort = 1500

        super(TopologyViewerServer, self).__init__(
                        SingleServer(port=serverPort),
                        chunks_to_lines(),
                        topology_message_parser(particleTypes = particleTypes),
                        TopologyViewerComponent(**dictArgs),
                        consoleEchoer()
                    )
         

if __name__=="__main__":
    app = TopologyViewerServer()
    app.activate()
    _scheduler.run.runThreads(slowmo=0)


