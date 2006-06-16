#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
#

import Axon
import pygame
import zlib

from Axon.Component import component
from Axon.Ipc import WaitComplete, producerFinished, shutdownMicroprocess

from Kamaelia.UI.PygameDisplay import PygameDisplay
from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.Util.Console import ConsoleReader
from Kamaelia.Util.Graphline import Graphline
from Kamaelia.Util.Backplane import Backplane, publishTo, subscribeTo
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines import chunks_to_lines
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists as text_to_tokenlists

#
# The following application specific components will probably be rolled
# back into the repository.
#

from Whiteboard.TagFiltering import TagAndFilterWrapper, FilterAndTagWrapper
from Whiteboard.Tokenisation import tokenlists_to_lines, lines_to_tokenlists

class Canvas(component):
    """\
    Canvas component - pygame surface that accepts drawing instructions
    """
    
    Inboxes =  { "inbox"   : "Receives drawing instructions",
                 "control" : "",
                 "fromDisplay"  : "For receiving replies from PygameDisplay service",
                 "eventsIn" : "For receiving PygameDisplay events",
               }
    Outboxes = { "outbox" : "Issues drawing instructions",
                 "signal" : "",
                 "toDisplay" : "For sending requests to PygameDisplay service",
                 "eventsOut" : "Events forwarded out of here",
               }
    
    def __init__(self, position=(0,0), size=(1024,768), ):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Canvas,self).__init__()
        self.position = position
        self.size = size
        
        
    
    def waitBox(self,boxname):
        waiting = True
        while waiting:
            if self.dataReady(boxname):
                return
            else:
                yield 1
        
        
    def requestDisplay(self, **argd):
        displayservice = PygameDisplay.getDisplayService()
        self.link((self,"toDisplay"), displayservice)
        self.send(argd, "toDisplay")
        for _ in self.waitBox("fromDisplay"):
            yield 1
        self.surface = self.recv("fromDisplay")
        

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False
        
        
    def main(self):
        """Main loop"""
        
        yield WaitComplete(
              self.requestDisplay( DISPLAYREQUEST=True,
                                   callback = (self,"fromDisplay"),
                                   events = (self, "eventsIn"),
                                   size = self.size,
                                   position = self.position,
                                 )
              )
              
        self.surface.fill( (255,255,255) )
        self.send({"REDRAW":True, "surface":self.surface}, "toDisplay")

        
        self.send( {"ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN, "surface" : self.surface},
                   "toDisplay" )
        self.send( {"ADDLISTENEVENT" : pygame.MOUSEMOTION, "surface" : self.surface},
                   "toDisplay" )
        self.send( {"ADDLISTENEVENT" : pygame.MOUSEBUTTONUP, "surface" : self.surface},
                   "toDisplay" )
        
        while not self.finished():
            
            while self.dataReady("inbox"):
                msgs = self.recv("inbox")
                self.redrawNeeded = False
                for msg in msgs:
                    cmd = msg[0]
                    args = msg[1:]
                    # parse commands here
                    self.handleCommand(cmd, *args)
                if self.redrawNeeded:
                    self.send({"REDRAW":True, "surface":self.surface}, "toDisplay")
                
                
            # pass on events received from pygame display
            while self.dataReady("eventsIn"):
                self.send( self.recv("eventsIn"), "eventsOut" )
                
            self.pause()
            yield 1
            
            
    def handleCommand(self, cmd, *args):
        cmd = cmd.upper()
        if cmd=="CLEAR":
            if len(args) == 3:
                self.surface.fill( [int(a) for a in args[0:3]] )
            else:
                self.surface.fill( (255,255,255) )
            self.redrawNeeded = True
        elif cmd=="LINE":
            (r,g,b,sx,sy,ex,ey) = [int(v) for v in args[0:7]]
            pygame.draw.line(self.surface, (r,g,b), (sx,sy), (ex,ey))
            self.redrawNeeded = True
        elif cmd=="CIRCLE":
            (r,g,b,x,y,radius) = [int(v) for v in args[0:6]]
            pygame.draw.circle(self.surface, (r,g,b), (x,y), radius, 0)
            self.redrawNeeded = True
        elif cmd=="LOAD":
            filename = args[0]
            try:
                loadedimage = pygame.image.load(filename)
            except:
                pass
            else:
                self.surface.blit(loadedimage, (0,0))
            self.redrawNeeded = True
        elif cmd=="SAVE":
            filename = args[0]
            pygame.image.save(self.surface, filename)
        elif cmd=="GETIMG":
            imagestring = pygame.image.tostring(self.surface,"RGB")
            imagestring = zlib.compress(imagestring)
            w,h = self.surface.get_size()
            self.send( [["SETIMG",imagestring,str(w),str(h),"RGB"]], "outbox" )
        elif cmd=="SETIMG":
            w,h = int(args[1]), int(args[2])
            imagestring = zlib.decompress(args[0])
            recvsurface = pygame.image.fromstring(imagestring, (w,h), args[3])
            self.surface.blit(recvsurface, (0,0))
            self.redrawNeeded = True
        elif cmd=="WRITE":
            x,y,size,r,g,b = [int(a) for a in args[0:6]]
            text = args[6]
            font = pygame.font.Font(None,size)
            textimg = font.render(text, False, (r,g,b))
            self.surface.blit(textimg, (x,y))
            self.redrawNeeded = True

class Painter(component):
    """\
    Painter() -> new Painter component.
    """
    
    Inboxes =  { "inbox"   : "For receiving PygameDisplay events",
                 "control" : "",
                 "colour"  : "select drawing, using colour",
                 "erase"   : "select eraser",
               }
    Outboxes = { "outbox" : "outputs drawing instructions",
                 "signal" : "",
               }
    
    def __init__(self):
        super(Painter,self).__init__()
        self.sendbuffer = []
     
    
    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False
    
    
    def main(self):
        """Main loop"""
        
        yield 1
        r,g,b = 0,0,0
        dragging = False
        mode="LINE"
        
        
        while not self.finished():
        
            while self.dataReady("colour"):
                r,g,b = self.recv("colour")
                mode = "LINE"
                
            while self.dataReady("erase"):
                self.recv("erase")
                mode = "ERASE"
        
            while self.dataReady("inbox"):
                message = self.recv("inbox")
                for data in message:
                    if data.type == pygame.MOUSEBUTTONDOWN:
                        if data.button==1:
                            oldpos = data.pos
                            dragging = True
                        elif data.button==3:
                            pygame.display.toggle_fullscreen()
                    elif data.type == pygame.MOUSEMOTION and dragging:
                        self.cmd(mode, oldpos, data.pos, r, g, b)
                        oldpos = data.pos
                    elif data.type == pygame.MOUSEBUTTONUP and dragging:
                        self.cmd(mode, oldpos, data.pos, r, g, b)
                        oldpos = data.pos
                        dragging = False
            self.flushbuffer()
            self.pause()
            yield 1

    def cmd(self, mode, oldpos, newpos, r, g, b):
        if mode=="LINE":
            self.sendbuffer.append( ["LINE", str(r),str(g),str(b), str(oldpos[0]), str(oldpos[1]), str(newpos[0]), str(newpos[1])] )
        elif mode=="ERASE":
            self.sendbuffer.append( ["CIRCLE", "255","255","255", str(newpos[0]), str(newpos[1]), "8"])

    def flushbuffer(self):
        if len(self.sendbuffer):
            self.send(self.sendbuffer[:], "outbox")
            self.sendbuffer = []

def buildPalette(cols, topleft=(0,0), size=32):
    buttons = {}
    links = {}
    pos = topleft
    i=0
    # Interesting/neat trick MPS
    for col in cols:
        buttons[str(i)] = Button(caption="", position=pos, size=(size,size), bgcolour=col, msg=col)
        links[ (str(i),"outbox") ] = ("self","outbox")
        pos = (pos[0] + size, pos[1])
        i=i+1
    return Graphline( linkages = links,  **buttons )

colours = [ (0,0,0), (192,0,0), (192,96,0), (160,160,0), (0,192,0),
            (0,160,160), (0,0,255), (192,0,192), (96,96,96), (192,192,192),
          ]


class OneShot(component):
    def __init__(self, msg=None):
        super(OneShot, self).__init__()
        self.msg = msg
    def main(self):
        self.send(self.msg,"outbox")
        yield 1


class TwoWaySplitter(component):
    Outboxes = { "outbox"  : "",
                 "outbox2" : "",
                 "signal"  : "",
                 "signal2" : "",
               }
               
    def main(self):
        done=False
        while not done:
            
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                self.send(data, "outbox")
                self.send(data, "outbox2")
                
            while self.dataReady("control"):
                data = self.recv("control")
                self.send(data, "signal")
                self.send(data, "signal2")
                if isinstance(data, (producerFinished, shutdownMicroprocess)):
                    done=True
                    
            self.pause()
            yield 1


def parseCommands():
    from Kamaelia.Util.Marshalling import Marshaller
    
    class CommandParser:
        def marshall(data):
            output = [data]
            if data[0].upper() == "LOAD":
                output.append(["GETIMG"])    # to propogate loaded image to other connected canvases
            return output
        marshall = staticmethod(marshall)
        
    return Marshaller(CommandParser)
                    

def makeSketcher(left=0,top=0,width=1024,height=768):
    return Graphline( CANVAS  = Canvas( position=(left,top+32),size=(width,height-32) ),
                      PAINTER = Painter(),
                      PALETTE = buildPalette( cols=colours, topleft=(left+64,top), size=32 ),
                      ERASER  = Button(caption="Eraser", size=(64,32), position=(left,top)),
                      SPLIT   = TwoWaySplitter(),
                
                      linkages = {
                          ("CANVAS",  "eventsOut") : ("PAINTER", "inbox"),
                          ("PALETTE", "outbox")    : ("PAINTER", "colour"),
                          ("ERASER", "outbox")     : ("PAINTER", "erase"),
                          ("PAINTER", "outbox")    : ("SPLIT", "inbox"),
                          ("SPLIT", "outbox")      : ("CANVAS", "inbox"),
                          
                          ("self", "inbox")        : ("CANVAS", "inbox"),
                          ("SPLIT", "outbox2")     : ("self", "outbox"),
                          ("CANVAS", "outbox")     : ("self", "outbox"),
                          },
                    )


if __name__=="__main__":
    import sys, getopt, re
    
    shortargs = ""
    longargs  = [ "serveport=", "connectto=" ]
            
    optlist, remargs = getopt.getopt(sys.argv[1:], shortargs, longargs)
    
    rhost, rport = None, None
    serveport = None
               
    for o,a in optlist:
        
        if o in ("-s","--serveport"):
            serveport = int(a)
            
        elif o in ("-c","--connectto"):
            rhost,rport = re.match(r"^([^:]+):([0-9]+)$", a).groups()
            rport = int(rport)

    
    mainsketcher = \
        Graphline( SKETCHER = makeSketcher(width=1024,height=768),
                   CONSOLE = pipeline(ConsoleReader(),text_to_tokenlists(),parseCommands()),
                   
                   linkages = { ('self','inbox'):('SKETCHER','inbox'),
                                ('SKETCHER','outbox'):('self','outbox'),
                                ('CONSOLE','outbox'):('SKETCHER','inbox'),
                              }
                 )
    
    # primary whiteboard
    pipeline( subscribeTo("WHITEBOARD"),
              TagAndFilterWrapper(mainsketcher),
              publishTo("WHITEBOARD")
            ).activate()
    
    # setup a server, if requested
    if serveport:
        # server
        # any requests for connections get plugged into the backplane
        # does the same tagging and filtering, and conversion tokenlists <-> lines
        from Kamaelia.Chassis.ConnectedServer import SimpleServer
        from Kamaelia.Util.Console import ConsoleEchoer
        
        def clientconnector():
            return pipeline(
                chunks_to_lines(),
                lines_to_tokenlists(),
                FilterAndTagWrapper(
                    pipeline( publishTo("WHITEBOARD"),
                                # well, should be to separate pipelines, this is lazier!
                                subscribeTo("WHITEBOARD"),
                            )
                    ),
                tokenlists_to_lines(),
                )
        
        SimpleServer(protocol=clientconnector, port=serveport).activate()

    # connect to remote host & port, if requested
    if rhost and rport:
        # plug a TCPClient into the backplae
        from Kamaelia.Internet.TCPClient import TCPClient
        
        loadingmsg = "Fetching sketch from server..."
        
        pipeline( subscribeTo("WHITEBOARD"),
                  TagAndFilterWrapper(
                      Graphline( GETIMG = OneShot(msg=[["GETIMG"]]),
                                 PIPE = pipeline(
                                            tokenlists_to_lines(),
                                            TCPClient(host=rhost,port=rport),
                                            chunks_to_lines(),
                                            lines_to_tokenlists(),
                                        ),
                                 BLACKOUT = OneShot(msg=[["CLEAR",0,0,0],["WRITE",100,100,24,255,255,255,loadingmsg]]),
                                 linkages = { ("self","inbox") : ("PIPE","inbox"),
                                              ("self","control") : ("PIPE","control"),
                                              ("PIPE","outbox") : ("self","outbox"),
                                              ("PIPE","signal") : ("self","signal"),
                                              ("GETIMG","outbox") : ("PIPE","inbox"),
                                              ("BLACKOUT","outbox") : ("self","outbox"),
                                            },
                               )
                      ),
                  publishTo("WHITEBOARD"),
                ).activate()
        

    
    Backplane("WHITEBOARD").run()
