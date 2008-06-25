"""
REPLACEME:
1. It's a PyGame container rather than a OpenGLComponent
2. It needs a loop, but both setup and draw are only executed once
"""

import Axon
from THF.Kamaelia.UI.OpenGL.OpenGLComponent import OpenGLComponent
from Kamaelia.UI.OpenGL.OpenGLDisplay import OpenGLDisplay

from OpenGL.GL import *
from OpenGL.GLU import *

from THF.Kamaelia.UI.OpenGL.Vector import Vector
from THF.Kamaelia.UI.OpenGL.Button import Button
from THF.Kamaelia.UI.OpenGL.MatchedTranslationInteractor import MatchedTranslationInteractor

import pygame
from pygame.locals import *

import sys

from Particles3D import Particle3D

_cat = Axon.CoordinatingAssistantTracker

#class TopologyViewer3D(Axon.Component.component):
class TopologyViewer3D(OpenGLComponent):
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
        
        tracker = _cat.coordinatingassistanttracker.getcat()
        display = OpenGLDisplay(width=screensize[0], height=screensize[1],fullscreen=fullscreen,
                                title=caption)
        display.activate()
        OpenGLDisplay.setDisplayService(display, tracker)
        
        
        super(TopologyViewer3D, self).__init__()
        
        self.particle = None
        self.particleTypes = {"-":Particle3D}
    
#    """ main used if it inherits component """
#    def main(self):
#        self._deliver(['ADD','NODE', '1', 'aaa', 'randompos', '-'], "inbox")
#        yield
#        if self.dataReady("inbox"):
#            print 'ready...'
#            message = self.recv("inbox")
#            self.doCommand(message)
#            print message

    """ setup and draw are used if it inherits OpenGLComponent """
    def setup(self):
        """ Build caption and request reception of events."""
#        self.buildCaption()
#        self.addListenEvents( [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.KEYDOWN ])
        #self.addListenEvents( [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.KEYDOWN ])
        print 'setup...'
        #self.rotation = Vector(*(10,20,0))
        
#        self.particle = Particle3D(position = (-1,0,-10))
#        self.particle1 = Particle3D(position = (3,0,-10))
#        print self.Inboxes['inbox']
        self._deliver(['ADD','NODE', '1', 'aaa', 'randompos', '-'], "inbox")
        
        if self.dataReady("inbox"):
            print 'ready...'
            message = self.recv("inbox")
            self.doCommand(message)
            print message


    def draw(self):
        print 'draw...'
        if self.particle is not None:
            #self.position = Vector(-1,0,-10)
            #self.scaling = Vector(2.1,2.1,2.1)
            print 'here'
            self.particle.draw()
            #glLoadIdentity()
        #self.position = Vector(3,0,-10)
        #self.particle1.render()
        
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
        
        #try:            
        if len(msg) >= 2:
            cmd = msg[0].upper(), msg[1].upper()

            if cmd == ("ADD", "NODE") and len(msg) == 6:
                if self.particleTypes.has_key(msg[5]):
                    ptype = self.particleTypes[msg[5]]
                    id    = msg[2]
                    name  = msg[3]
                    #print 'here'
                    #posSpec = msg[4]
                    #pos     = self._generateXY(posSpec)

                    self.particle = ptype(position = (-1,0,-10))
                    
#                        # Use OpenGLComponent Button as particle, MatchedTranslationInteractor as dragHandler
#                        self.particle = Button(caption="Particle", msg="Particle", position=(-1,0,-10)).activate()
#                        MatchedTranslationInteractor(target=self.particle).activate()
                    #particle.originaltype = msg[5]
                    #self.addParticle(particle)
            
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
#        except:     
#            import traceback
#            errmsg = reduce(lambda a,b: a+b, traceback.format_exception(*sys.exc_info()) )
#            self.send( ("ERROR", "Error processing message : "+str(msg) + " resason:\n"+errmsg), "outbox")
            
if __name__ == "__main__":
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
    from Kamaelia.Util.Console import ConsoleEchoer,ConsoleReader
    from Kamaelia.Chassis.Pipeline import Pipeline
    
    TopologyViewer3D().run()
    
#    Pipeline(
#        #DataSource(['ADD NODE 1 aaa randompos -','']),
#        ConsoleReader(">>> "),
#        lines_to_tokenlists(),
#        TopologyViewer3D(),
#        #ConsoleEchoer(),
#    ).run()  