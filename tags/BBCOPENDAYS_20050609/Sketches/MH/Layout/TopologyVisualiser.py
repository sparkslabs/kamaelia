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
        self.left = 0
        self.top  = 0
        self.selected = False
       
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
        x = int(self.pos[0]) - self.left
        y = int(self.pos[1]) - self.top
        
        yield 1
        for p in self.bondedTo:
            pygame.draw.line(surface, (128,128,255), (x,y),  (int(p.pos[0] -self.left),int(p.pos[1] - self.top)) )
        
        yield 2
        pygame.draw.circle(surface, (255,128,128), (x,y), self.radius)
        if self.selected:
            pygame.draw.circle(surface, (0,0,0), (x,y), self.radius, 2)
        surface.blit(self.label, (x - self.label.get_width()/2, y - self.label.get_height()/2))
        
        
    def setOffset( self, (left,top) ):
        """Inform of a change to the coords of the top left of the drawing surface,
        so that this entity can render, as if the top left had moved
        """
        self.left = left
        self.top  = top

        
    def select( self ):
        """Tell this particle it is selected"""
        self.selected = True

    def deselect( self ):
        """Tell this particle it is selected"""
        self.selected = False



class ParticleDragger(DragHandler):
    """Works with the TopologyViewerComponent to provide particle selecting
    and dragging functionality"""

    def detect(self, pos, button):
        # find particles under the mouse pos
        pos = int(pos[0] + self.app.left), int(pos[1] + self.app.top)
        inRange = self.app.physics.withinRadius( pos, self.app.biggestRadius )
        inRange = filter(lambda (p, rsquared) : p.radius*p.radius >= rsquared, inRange)
        
        # deselect any particle already selected
        if self.app.selectedParticle != None:
            self.app.selectedParticle.deselect()
            
        if len(inRange) > 0:
            # of those in range, find one whose centre is nearest to the mouse pos
            best = -1
            for (p,rsquared) in inRange:
                if best < 0 or rsquared < best:
                    best = rsquared
                    self.particle = p
                  
            self.particle.freeze() # tell the particle its not allowed to move (zero velocity)
             
            # select this particle
            self.app.selectedParticle = self.particle
            self.particle.select()

            # return the drag start coordinates             
            return self.particle.getLoc()
        else:
            self.app.selectedParticle = None
            return False

    def drag(self,newx,newy):
        self.particle.pos = (newx,newy)
        self.app.physics.updateLoc(self.particle)

    def release(self,newx, newy):
        self.drag(newx, newy)
        self.particle.unFreeze()                


class GridRenderer(object):
    def __init__(self, size, colour):
        super(GridRenderer,self).__init__(size, colour)
        self.gridSize = int(size)
        self.colour   = colour
        self.left     = 0
        self.top      = 0

    def render(self, surface):
        yield -1
        for i in range((self.top // self.gridSize) * self.gridSize - self.top,
                       surface.get_height(),
                       self.gridSize):
            pygame.draw.line(surface, self.colour,
                             (0,i),
                             (surface.get_width(),i) )

        for i in range((self.left // self.gridSize) * self.gridSize - self.left,
                       surface.get_width(), 
                       self.gridSize):
            pygame.draw.line(surface, self.colour, 
                             (i, 0                   ), 
                             (i, surface.get_height()) )

    def setOffset( self, (left,top) ):
        """Inform of a change to the coords of the top left of the drawing surface,
        so that this entity can render, as if the top left had moved
        """
        self.left = left
        self.top  = top
                                      
                  
class TopologyViewerComponent(PyGameApp,component):
    """Generic Topology Viewer Component
    
       Displays a topology in a pygame application. It can be interacted
       with by dragging nodes with the mouse.
    
       Receives command tuples on its inbox. See handleCommunication()
       for command syntax.
       
       Outputs diagnostic and error messages on its outbox
       
       See keyDownHandler() for keyboard controls.
    """
    def __init__(self, screensize         = (640,480),
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
            self.particleTypes = {"-":Particle}
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
        self.addHandler(MOUSEBUTTONDOWN, lambda event: ParticleDragger(event,self))
        self.addHandler(KEYDOWN, self.keyDownHandler)
        self.addHandler(KEYUP,   self.keyUpHandler)
        
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
        if event.key==K_ESCAPE or event.key==K_q:
            self.quit()
        elif event.key==K_f:
            pygame.display.toggle_fullscreen()
            
        elif event.key == K_UP:
            self.dtop = -4
        elif event.key == K_DOWN:
            self.dtop = +4
        elif event.key == K_LEFT:
            self.dleft = -4
        elif event.key == K_RIGHT:
            self.dleft = +4
    
    def keyUpHandler(self, event):
        """Handle releases of keys"""
        if event.key == K_UP:
            self.dtop = 0
        elif event.key == K_DOWN:
            self.dtop = 0
        elif event.key == K_LEFT:
            self.dleft = 0
        elif event.key == K_RIGHT:
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

                             

class lines_to_tokenlists(component):
    """Takes in lines and outputs a list of tokens on each line.
      
       Tokens are separated by white space.
      
       Tokens can be encapsulated with single or double quote marks, allowing you
       to include white space. If you do this, backslashs should be used to escape
       a quote mark that you want to include within the token. Represent backslash
       with a double backslash.
      
       Example:
           Hello world "how are you" 'john said "hi"' "i replied \"hi\"" end
      
         Becomes:
         [ 'Hello',
           'world',
           'how are you',
           'john said "hi"', 
           'i replied "hi"',
           'end' ]
    """
    def __init__(self):
        super(lines_to_tokenlists, self).__init__()
        
        doublequoted = r'(?:"((?:(?:\\.)|[^\\"])*)")'
        singlequoted = r"(?:'((?:(?:\\.)|[^\\'])*)')"
        unquoted     = r'([^"\'][^\s]*)'
        
        self.tokenpat = re.compile( r'\s*(?:' + unquoted +
                                          "|" + singlequoted +
                                          "|" + doublequoted +
                                          r')(?:\s+(.*))?$' )
        
   
    def main(self):
       
        while 1:
           while self.dataReady("inbox"):
               line = self.recv("inbox")
               tokens = self.lineToTokens(line)
               if tokens != []:
                   self.send(tokens, "outbox")
           yield 1
    
           
    def lineToTokens(self, line):
        tokens = []    #re.split("\s+",line.strip())
        while line != None and line.strip() != "":
            match = self.tokenpat.match(line)
            if match != None:
                (uq, sq, dq, line) = match.groups()
                if uq != None:
                    tokens += [uq]
                elif sq != None:
                    tokens += [ re.sub(r'\\(.)', r'\1', sq) ]
                elif dq != None:
                    tokens += [ re.sub(r'\\(.)', r'\1', dq) ]
            else:
                return []
        return tokens
        

class chunks_to_lines(component):
   """Takes in chunked textual data and breaks it at line breaks into lines."""

   def main(self):
      gotLine = False
      line = ""
      while 1: 
         pos = line.find("\n")
         if pos > -1:
            self.send(line[:pos], "outbox")
            line = line[pos+1:] 
         else:
            if self.dataReady("inbox"):
               chunk = self.recv("inbox")
               chunk = chunk.replace("\r", "")
               line = line + chunk
            else:
               self.pause()
         yield 1


class TopologyViewerServer(pipeline):
    def __init__(self, noServer = False, serverPort = None, **dictArgs):
        """particleTypes = dictionary mapping names to particle classes
        
           All remaining named arguments are passed onto the TopologyViewerComponent
        """
        
        from Kamaelia.SingleServer import SingleServer
        from Kamaelia.Util.ConsoleEcho import consoleEchoer
        
        pipe = [chunks_to_lines(),
                lines_to_tokenlists(),
                TopologyViewerComponent(**dictArgs),
                consoleEchoer() ]
                
        if not noServer:
            if serverPort == None:
                serverPort = 1500
            pipe.insert(0, SingleServer(port=serverPort))
            

        super(TopologyViewerServer, self).__init__(*pipe)
         


def parseArgs(argv, extraShortArgs="", extraLongArgs=[]):
    import getopt
    
    shortargs = "fh" + extraShortArgs
    longargs  = ["help","fullscreen","resolution=","port="] + extraLongArgs
            
    optlist, remargs = getopt.getopt(argv, shortargs, longargs)
    
    dictArgs = {}
    for o,a in optlist:
        if o in ("-h","--help"):
            dictArgs['help'] = "Arguments:\n" + \
                               "   -h, --help\n" + \
                               "      This help message\n\n" + \
                               "   -f, --fullscreen\n" + \
                               "      Full screen mode\n\n" + \
                               "   --resolution=WxH\n" + \
                               "      Set window size to W by H pixels\n\n" + \
                               "   --port=N\n" + \
                               "      Listen on port N (default is 1500)\n\n"
    
        elif o in ("-f","--fullscreen"):
            dictArgs['fullscreen'] = True
            
        elif o in ("--resolution"):
            match = re.match(r"^(\d+)[x,-](\d+)$", a)
            x=int(match.group(1))
            y=int(match.group(2))
            dictArgs['screensize'] = (x,y)
            
        elif o in ("--port"):
            dictArgs['serverPort'] = int(a)
            
    return dictArgs, optlist, remargs
                    
                    
if __name__=="__main__":
    import sys
    dictArgs, remargs = parseArgs(sys.argv[1:])
    
    if "help" in dictArgs:
        print dictArgs["help"]
        
    else:
        app = TopologyViewerServer(**dictArgs)
        app.activate()
        _scheduler.run.runThreads(slowmo=0)


