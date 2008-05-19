#!/usr/bin/env python

# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

import random
import time
import re
import sys
import pygame

import Axon
import Physics
import UI

from GridRenderer import GridRenderer
from ParticleDragger import ParticleDragger
from RenderingParticle import RenderingParticle
                  
class TopologyViewerComponent(UI.PyGameApp,Axon.Component.component):
    """Generic Topology Viewer Component
    
       Displays a topology in a pygame application. It can be interacted
       with by dragging nodes with the mouse.
    
       Receives command tuples on its inbox. See handleCommunication()
       for command syntax.
       
       Outputs diagnostic and error messages on its outbox
       
       See keyDownHandler() for keyboard controls.
    """
    def __init__(self, screensize         = (800,600),
                       fullscreen         = False, 
                       caption            = "Topology Viewer", 
                       particleTypes      = None,
                       initialTopology    = None,
                       laws               = None,
                       simCyclesPerRedraw = None,
                       border             = 100,
                       extraDrawing       = None):
                       
        super(TopologyViewerComponent, self).__init__(screensize, caption, fullscreen)
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
            self.laws = Physics.SimpleLaws(bondLength=100)
        else:
            self.laws = laws
            
        if simCyclesPerRedraw==None:
            self.simCyclesPerRedraw = 1
        else:
            self.simCyclesPerRedraw = simCyclesPerRedraw
        
        self.graphicalFurniture = []
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
          

    def initialiseComponent(self):
        self.addHandler(pygame.MOUSEBUTTONDOWN, lambda event: ParticleDragger(event,self))
        self.addHandler(pygame.KEYDOWN, self.keyDownHandler)
        self.addHandler(pygame.KEYUP,   self.keyUpHandler)
        
        self.physics = Physics.ParticleSystem(self.laws, [], 0)
        
        for node in self.initialNodes:
           self.addParticle(*node)

        for source,dest in self.initialBonds:
           self.makeBond(source, dest)
        return 1

        
    def mainLoop(self):
        """Main loop.
           1) Processing incoming commands.
           2) Runs the physics simulation
           3) Draws the white graph paper
           4) Draws particles and any extra 'furniture'
           
           If lots of commands are coming in, physics and redrawing is postponed until commands stop or
           a timeout (1 second) expires - thereby speeding up the processing of changes to the topology
        """
    
        # process incoming messages
        if self.dataReady("inbox"):
            message = self.recv("inbox")
            self.doCommand(message)
        else:
            self.lastIdleTime = 0
        
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

        return 1
        
    def render(self):        
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
#                    if not renderPasses.has_key(n):
#                        renderPasses[n] = [r]
#                    else:
#                        renderPasses[n].append(r)
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
#                    if not renderPasses.has_key(n):
#                        renderPasses[n] = [r]
#                    else:
#                        renderPasses[n].append(r)
                except StopIteration:
                    pass
                    
        

    def keyDownHandler(self, event):
        """Handle keyboard presses:
           ESCAPE, Q : quits
           F         : toggles fullscreen mode
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
        """Command processor
        
        Commands accepted are:
          [ "ADD", "NODE", <id>, <name>, <positionSpec>, <particle type> ]
               Add a node
               nodeFactory( (x,y) ) should return a particle
               posSpec is a string describing initial x,y (see _generateXY)
      
          [ "DEL", "NODE", <id> ]
               Remove a node (also removes all links to and from it)
        
          [ "ADD", "LINK", <id from>, <id to> ]
               Add a link, directional from fromID to toID
           
          [ "DEL", "LINK", <id from>, <id to> ]
               Remove a link, directional from fromID to toID
               
          [ "DEL", "ALL" ]
               Clears all nodes and links
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
    
                else:
                    raise "Command Error"
            else:
                raise "Command Error"
        except:     
            import traceback
            errmsg = reduce(lambda a,b: a+b, traceback.format_exception(*sys.exc_info()) )
            self.send("Error processing message : "+str(msg) + " resason:\n"+errmsg, "outbox")
                                                    
                
    def _generateXY(self, posSpec):
        """Takes a string specifying a position specification and returns
           a tuple (x,y). Raises ValueError if the specification is wrong"""
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
        """Adds particles to the system"""
        for p in particles:
            if p.radius > self.biggestRadius:
                self.biggestRadius = p.radius
            p.setOffset( (self.left, self.top) )
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
        
    def scroll( self, (dx, dy) ):
        self.left += dx
        self.top += dy
        for e in self.graphicalFurniture + self.physics.particles:
            e.setOffset( (self.left, self.top) )
