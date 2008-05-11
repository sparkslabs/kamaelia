#!/usr/bin/env python
#
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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


import pygame
import Axon
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *
from Util3D import *
from Axon.ThreadedComponent import threadedcomponent
import time
from Kamaelia.UI.PygameDisplay import PygameDisplay

_cat = Axon.CoordinatingAssistantTracker

class Bunch: pass

class Display3D(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    Inboxes =  { "inbox"    : "Default inbox, not currently used",
                     "control" : "NOT USED",
                     "notify"  : "Receive requests for surfaces, overlays and events",
                     "events" : "Receive pygame events",
                  }
    Outboxes = { "outbox" : "NOT USED",
                     "signal" : "NOT USED",
                  }
                
                
                 
    def setDisplayService(pygamedisplay, tracker = None):
        """\
        Sets the given pygamedisplay as the service for the selected tracker or
        the default one.

        (static method)
        """
        if not tracker:
            tracker = _cat.coordinatingassistanttracker.getcat()
        tracker.registerService("3ddisplay", pygamedisplay, "notify")
    setDisplayService = staticmethod(setDisplayService)




    def getDisplayService(tracker=None): # STATIC METHOD
        """\
        Returns any live pygamedisplay registered with the specified (or default)
        tracker, or creates one for the system to use.

        (static method)
        """
        if tracker is None:
            tracker = _cat.coordinatingassistanttracker.getcat()
        try:
            service = tracker.retrieveService("3ddisplay")
            return service
        except KeyError:
            display = Display3D()
            display.activate()
            Display3D.setDisplayService(display, tracker)
            service=(display,"notify")
            return service
    getDisplayService = staticmethod(getDisplayService)
    
    
    def overridePygameDisplay():
        PygameDisplay.setDisplayService(Display3D.getDisplayService()[0])
    overridePygameDisplay = staticmethod(overridePygameDisplay)    
    
    
    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Display3D,self).__init__()
        self.caption = argd.get("title", "http://kamaelia.sourceforge.net")
        self.width = argd.get("width",800)
        self.height = argd.get("height",600)
        self.background_colour = argd.get("background_colour", (255,255,255))
        self.fullscreen = pygame.FULLSCREEN * argd.get("fullscreen", 0)
        self.next_position = (0,0)

        # 3D component handling
        self.objects = []
        self.movementMode = False
        
        # Pygame component handling
        self.surfaces = []
        self.overlays = []
        self.visibility = {}
        self.events_wanted = {}
        self.surface_to_eventcomms = {}
        self.surface_to_eventservice = {}
        self.surface_to_texnames = {}
        self.surface_to_pow2surface = {}
        self.surface_to_eventrequestcomms = {}
        
        self.wrappedsurfaces = []
       
        # determine projection parameters
        self.nearPlaneDist = argd.get("near", 1.0)
        self.farPlaneDist = argd.get("far", 100.0)
        self.perspectiveAngle = argd.get("perspective", 45.0)
        self.aspectRatio = float(self.width)/float(self.height)
        global pi
        self.farPlaneHeight = self.farPlaneDist*2.0/tan(pi/2.0-self.perspectiveAngle*pi/360.0)
        self.farPlaneWidth = self.farPlaneHeight*self.aspectRatio
        self.farPlaneScaling = self.farPlaneWidth/self.width
        
        # initialize the display      
        pygame.init()
        display = pygame.display.set_mode((self.width, self.height), self.fullscreen| pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption(self.caption)
        pygame.mixer.quit()
        
        glClearColor(1.0,1.0,1.0,0.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        
        # enable translucency
        glEnable (GL_BLEND);
        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

        # projection matrix
        glMatrixMode(GL_PROJECTION)                 
        glLoadIdentity()                                
        gluPerspective(self.perspectiveAngle, self.aspectRatio, self.nearPlaneDist, self.farPlaneDist)
        
        self.texnum = -1



    
    
    
    def surfacePosition(self,surface):
        """Returns a suggested position for a surface. No guarantees its any good!"""
        position = self.next_position
        self.next_position = position[0]+50, position[1]+50
        return position

        
        
    def handleDisplayRequest(self):
            """\
            Check "notify" inbox for requests for surfaces, events and overlays and
            process them.
            """
            # changed from if to while
            while self.dataReady("notify"):
                message = self.recv("notify")
                if isinstance(message, Axon.Ipc.producerFinished): ### VOMIT : mixed data types
#                    print "SURFACE", message
                    surface = message.message
#                    print "SURFACE", surface
                    message.message = None
                    message = None
#                    print "BEFORE", [id(x[0]) for x in self.surfaces]
                    self.surfaces = [ x for x in self.surfaces if x[0] is not surface ]
#                    print "AFTER", self.surfaces
#                    print "Hmm...", self.surface_to_eventcomms.keys()
                    try:
                         eventcomms = self.surface_to_eventcomms[str(id(surface))]
                    except KeyError:
                         # This simply means the component wasn't listening for events!
                         pass
                    else:
#                         print "EVENT OUTBOX:", eventcomms
                         self.visibility = None
                         try:
                              self.removeOutbox(eventcomms)
                         except:
                              "This sucks"
                              pass
#                         print "REMOVED OUTBOX"
                elif message.get("3DDISPLAYREQUEST", False):
                    eventservice = message.get("events", None)
                    eventcomms = None
                    if eventservice is not None:
                        eventcomms = self.addOutbox("eventsfeedback")
                        self.link((self,eventcomms), eventservice)
                    self.objects.append( (message.get("object"), eventcomms) )
                    
                elif message.get("WRAPPERREQUEST", False):
                    surface = message.get("surface")
                    self.wrappedsurfaces.append(str(id(surface)));
                    callbackservice = message["wrapcallback"]
                    callbackcomms = self.addOutbox("wrapfeedback")
                    pow2surface = self.surface_to_pow2surface[str(id(surface))]
                    #determine texture coordinates
                    tex_w = float(surface.get_width())/float(pow2surface.get_width())
                    tex_h = float(surface.get_height())/float(pow2surface.get_height())
                    # send display data
                    self.link((self,callbackcomms), callbackservice)
                    b = Bunch()
                    b.texname = self.surface_to_texnames[str(id(surface))]
                    b.tex_w = tex_w
                    b.tex_h = tex_h
                    b.width = surface.get_width()
                    b.height = surface.get_height()
                    try:
                        b.eventservice = self.surface_to_eventservice[str(id(surface))]
                    except KeyError:
                        b.eventservice = None
                    self.send(b, callbackcomms)
                    #handle only events if wrapped components can receive them
                    try :
                        eventcomms = self.surface_to_eventcomms[str(id(surface))]
                        # save callback for event requests
                        eventrequestservice = message["eventrequests"]
                        eventrequestcomms = self.addOutbox("eventrequests")
                        self.link((self,eventrequestcomms), eventrequestservice)
                        self.surface_to_eventrequestcomms[str(id(surface))] = eventrequestcomms
                        # transmit already requested eventtypes
                        for (etype, wanted) in self.events_wanted[eventcomms].items():
                            if wanted == True:
                                self.send( {"ADDLISTENEVENT":etype}, eventrequestcomms)
                    except KeyError: pass
                    
                elif message.get("DISPLAYREQUEST", False):
                    self.needsRedrawing = True
                    callbackservice = message["callback"]
                    eventservice = message.get("events", None)
                    size = message["size"]
                    surface = pygame.Surface(size)

                    #create another surface, with dimensions a power of two
                    # this is needed because otherwise texturing is REALLY slow
                    pow2size = (int(2**(ceil(log(size[0], 2)))), int(2**(ceil(log(size[1], 2)))))
                    pow2surface = pygame.Surface(pow2size)

                    alpha = message.get("alpha", 255)
                    surface.set_alpha(alpha)
                    if message.get("transparency", None):
                        surface.set_colorkey(message["transparency"])
                    position = message.get("position", self.surfacePosition(surface))
                    callbackcomms = self.addOutbox("displayerfeedback")
                    eventcomms = None
                    if eventservice is not None:
                        eventcomms = self.addOutbox("eventsfeedback")
                        self.events_wanted[eventcomms] = {}
                        self.link((self,eventcomms), eventservice)
                        self.visibility[eventcomms] = (surface,size,position)
                        self.surface_to_eventcomms[str(id(surface))] = eventcomms
                        self.surface_to_eventservice[str(id(surface))] = eventservice
                    self.link((self, callbackcomms), callbackservice)
                    self.send(surface, callbackcomms)

                    # generate texture name
                    texname = glGenTextures(1)
                    self.surface_to_texnames[str(id(surface))] = texname
                    self.surface_to_pow2surface[str(id(surface))] = pow2surface

                    self.surfaces.append( (surface, position, size, callbackcomms, eventcomms, pow2surface, texname) )
                    
                elif message.get("ADDLISTENEVENT", None) is not None:
                    # test if surface is beeing wrapped
                    if str(id(surface)) in self.wrappedsurfaces:
                        self.send(message, self.surface_to_eventrequestcomms[str(id(surface))])
                    else:
                        eventcomms = self.surface_to_eventcomms[str(id(message["surface"]))]
                        self.events_wanted[eventcomms][message["ADDLISTENEVENT"]] = True

                elif message.get("REMOVELISTENEVENT", None) is not None:
                   # test if surface is beeing wrapped
                    if str(id(surface)) in self.wrappedsurfaces:
                        self.send(message, self.surface_to_eventrequestcomms[str(id(surface))])
                    else:
                        eventcomms = self.surface_to_eventcomms[str(id(message["surface"]))]
                        self.events_wanted[eventcomms][message["REMOVELISTENEVENT"]] = False
                    
                elif message.get("CHANGEDISPLAYGEO", False):
                    try:
                        surface = message.get("surface", None)
                        if surface is not None:
                            self.needsRedrawing = True
                            c = 0
                            found = False
                            while c < len(self.surfaces) and not found:
                                if self.surfaces[c][0] == surface:
                                    found = True
                                    break
                                c += 1
                            if found:
                                (surface, position, size, callbackcomms, eventcomms, pow2surface, texname) = self.surfaces[c]
                                new_position = message.get("position", position)
                                # update texture
                                self.updatePygameTexture(surface, texname)
                                
                                self.surfaces[c] = (surface, new_position, callbackcomms, eventcomms, texname)
                    except Exception, e:
                        print "It all went horribly wrong", e   
                
                elif message.get("OVERLAYREQUEST", False):
                    self.needsRedrawing = True
                    size = message["size"]
                    pixformat = message["pixformat"]
                    position = message.get("position", (0,0))
                    overlay = pygame.Overlay(pixformat, size)
                    yuvdata = message.get("yuv", ("","",""))
                    
                    # transform (y,u,v) to (y,v,u) because pygame seems to want that(!)
                    if len(yuvdata) == 3:
                          yuvdata = (yuvdata[0], yuvdata[2], yuvdata[1])

                    yuvservice = message.get("yuvservice",False)
                    if yuvservice:
                        yuvinbox = self.addInbox("overlay_yuv")
                        self.link( yuvservice, (self, yuvinbox) )
                        yuvservice = (yuvinbox, yuvservice)

                    posservice = message.get("positionservice",False)
                    if posservice:
                        posinbox = self.addInbox("overlay_position")
                        self.link (posservice, (self, posinbox) )
                        posservice = (posinbox, posservice)
                    
                    self.overlays.append( {"overlay":overlay,
                                           "yuv":yuvdata,
                                           "position":position,
                                           "size":size,
                                           "yuvservice":yuvservice,
                                           "posservice":posservice}
                                        )
                                        
                elif message.get("REDRAW", False):
                    self.needsRedrawing=True
                    surface = message["surface"]
                    self.updatePygameTexture(surface, self.surface_to_pow2surface[str(id(surface))], self.surface_to_texnames[str(id(surface))])

                        

    def handleEvents(self):
        # pre-fetch all waiting events in one go
        events = [ event for event in pygame.event.get() ]

        # Handle Pygame events
        for surface, position, size, callbackcomms, eventcomms, pow2surface, texname in self.surfaces:
            # see if this component is interested in events
            # skip surfaces which get wrapped

            if eventcomms is not None:
                listener = eventcomms
                # go through events, for each, check if the listener is interested in that time of event         
                bundle = []
                for event in events:
                    wanted = False
                    try:   wanted = self.events_wanted[listener][event.type]
                    except KeyError: pass
                    if wanted:
                        # if event contains positional information, remap it
                        # for the surface's coordiate origin
                        if event.type in [ pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN ]:
                            if str(id(surface)) in self.wrappedsurfaces: continue
                            e = Bunch()
                            e.type = event.type
                            pos = event.pos[0],event.pos[1]
                            try:
                                e.pos  = ( pos[0]-self.visibility[listener][2][0], pos[1]-self.visibility[listener][2][1] )
                                if event.type == pygame.MOUSEMOTION:
                                    e.rel = event.rel
                                if event.type == pygame.MOUSEMOTION:
                                    e.buttons = event.buttons
                                else:
                                    e.button = event.button
                                event = e
                            except TypeError:
                                "XXXX GRRR"
                                pass

                        bundle.append(event)

                # only send events to listener if we've actually got some
                if bundle != []:
                    self.send(bundle, listener)


        directions = {}
        for event in events:
            # Determine input mode
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL:
#                print "Movement mode on"
                self.movementMode = True
            if event.type == pygame.KEYUP and event.key == pygame.K_LCTRL:
#                print "Movement mode off"
                self.movementMode = False
            # Determine direction vectors
            if event.type in [ pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN ]:
                # determine intersection ray
                xclick = float(event.pos[0]-self.width/2)*self.farPlaneWidth/float(self.width)
                yclick = float(-event.pos[1]+self.height/2)*self.farPlaneHeight/float(self.height)
                directions[id(event)] = Vector(xclick, yclick, -self.farPlaneDist).norm()

        # Handle 3D object events
        for obj, eventcomms in self.objects:
            # see if this component is interested in events
            if eventcomms is not None:
                # go through events, for each, check if the listener is interested in that time of event         
                bundle = []
                for event in events:
                    if event.type in [ pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN ]:
                        e = Bunch()
                        e.type = event.type
                        e.dir = directions[id(event)]
                        e.movementMode = self.movementMode
                        if event.type in [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN]:
                            e.button = event.button
                        if event.type == pygame.MOUSEMOTION:
                            e.rel = event.rel
                            e.buttons = event.buttons
    
                        bundle.append(e)
    
                # only send events to listener if we've actually got some
                if bundle != []:
                    self.send(bundle, eventcomms)



    def updatePygameTexture(self, surface, pow2surface, texname):
#        print "UPDATE", texname
        # blit component surface to power of 2 sized surface
        pow2surface.blit(surface, (0,0))
        # set surface as texture
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texname)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        textureData = pygame.image.tostring(pow2surface, "RGBX", 1)
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, pow2surface.get_width(), pow2surface.get_height(), 0,
                        GL_RGBA, GL_UNSIGNED_BYTE, textureData );
        glDisable(GL_TEXTURE_2D)



    def drawPygameSurfaces(self):
        # disable depth testing temporarely to ensure that pygame components
        # are on top of everything
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        for surface, position, size, callbackcomms, eventcomms, pow2surface, texname in self.surfaces:
            # create texture if not already done
            if not glIsTexture(texname):
                self.updatePygameTexture(surface, pow2surface, texname)

            # skip surfaces which get wrapped
            if str(id(surface)) in self.wrappedsurfaces: continue
            
            glBindTexture(GL_TEXTURE_2D, texname)

            # determine surface positions on far Plane
            l = position[0]*self.farPlaneScaling-self.farPlaneWidth/2
            t = -position[1]*self.farPlaneScaling+self.farPlaneHeight/2
            r = l + size[0]*self.farPlaneScaling
            b = t - size[1]*self.farPlaneScaling
            
            #determine texture coordinates
            tex_w = float(size[0])/float(pow2surface.get_width())
            tex_h = float(size[1])/float(pow2surface.get_height())
                
            # draw just the texture, no background
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)

            # draw faces 
            glBegin(GL_QUADS)
            glColor3f(1, 0, 0)
            glTexCoord2f(0.0, 1.0-tex_h);         glVertex3f( l, b,  -self.farPlaneDist)
            glTexCoord2f(tex_w, 1.0-tex_h);     glVertex3f( r, b,  -self.farPlaneDist)
            glTexCoord2f(tex_w, 1.0); glVertex3f( r,  t,  -self.farPlaneDist)
            glTexCoord2f(0.0, 1.0);     glVertex3f( l,  t,  -self.farPlaneDist)
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)        
  
        
        
    def drawBackground(self):        
        glBegin(GL_QUADS)
        glColor4f(0.85, 0.85, 1.0, 1.0)
        glVertex3f(-self.farPlaneWidth/2.0, self.farPlaneHeight/2.0, -self.farPlaneDist)
        glVertex3f(self.farPlaneWidth/2.0, self.farPlaneHeight/2.0, -self.farPlaneDist)
        glVertex3f(self.farPlaneWidth/2.0, 0.0, -self.farPlaneDist)
        glVertex3f(-self.farPlaneWidth/2.0, 0.0, -self.farPlaneDist)
        glColor4f(0.75, 1.0, 0.75, 1.0)
        glVertex3f(-self.farPlaneWidth/2.0, 0.0, -self.farPlaneDist)
        glVertex3f(self.farPlaneWidth/2.0, 0.0, -self.farPlaneDist)
        glVertex3f(self.farPlaneWidth/2.0, -self.farPlaneHeight/2.0, -self.farPlaneDist)
        glVertex3f(-self.farPlaneWidth/2.0, -self.farPlaneHeight/2.0, -self.farPlaneDist)
        glEnd()
        

        
    def updateDisplay(self):
        
        #display pygame components
        self.drawPygameSurfaces()
        
        # show frame
        glFlush()
        pygame.display.flip()
        
        # clear drawing buffer
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # draw background
        self.drawBackground()

        

    def main(self):
        """Main loop."""

        while 1:
            self.handleDisplayRequest()
            self.handleEvents()
            self.updateDisplay()
            yield 1




if __name__=='__main__':
    class Bunch: pass
        
    class CubeRotator(Axon.Component.component):
        def main(self):
            while 1:
                yield 1
                self.send( Control3D(Control3D.REL_ROTATION, Vector(0.1, 0.1, 0.1)), "outbox")

    class CubeMover(Axon.Component.component):
        def main(self):
            x,y,z = 3.0, 3.0, -20.0
            dx = -0.03
            dy = -0.03
            dz = -0.03
            while 1:
                yield 1
                self.send( Control3D(Control3D.POSITION, Vector(x, y, z)), "outbox")
                x +=dx
                y +=dy
                z +=dz
                if abs(x)>5: dx = -dx
                if abs(y)>5: dy = -dy
                if abs(z+20)>10: dz = -dz
#                print x, y, abs(x), abs(y)


    import random

    class CubeBuzzer(Axon.Component.component):
        def main(self):
            r = 1.00
            f = 0.01
            while 1:
                yield 1
                if  r>1.0: f -= 0.001
                else: f += 0.001
                r += f
                
                self.send( Control3D(Control3D.SCALING, Vector(r, r, r)), "outbox")

    text = """\
The lights begin to twinkle from the rocks;
The long day wanes; the slow moon climbs; the deep
Moans round with many voices.  Come, my friends.
'T is not too late to seek a newer world.Push off, and sitting well in order smite
The sounding furrows; for my purpose holds
To sail beyond the sunset, and the baths
Of all the western stars, until I die.
It may be that the gulfs will wash us down;
It may be we shall touch the Happy Isles,
And see the great Achilles, whom we knew.
Tho' much is taken, much abides; and tho'
We are not now that strength which in old days
Moved earth and heaven, that which we are, we are,--
One equal temper of heroic hearts,
Made weak by time and fate, but strong in will
To strive, to seek, to find, and not to yield.
"""
    class datasource(Axon.Component.component):
        def main(self):
            for x in text.split():
                self.send(x,"outbox")
                yield 1

    
    from Kamaelia.Util.ConsoleEcho import consoleEchoer
    from Kamaelia.Util.Graphline import Graphline
    from Kamaelia.UI.Pygame.Button import Button
    from Kamaelia.UI.Pygame.Ticker import Ticker
    from SimpleCube import SimpleCube
    from TexPlane import TexPlane
    from pygame.locals import *

    Display3D.getDisplayService()[0].overridePygameDisplay()
    
    Graphline(
        CUBE = SimpleCube(pos = Vector(3,3,-15)),
        PLANE = TexPlane(pos=Vector(-3, 0,-10), tex="Kamaelia.png", name="1st Tex Plane"),
        BUTTON1 = Button(caption="Press SPACE or click", key=K_SPACE),
        BUTTON2 = Button(caption="Reverse colours",fgcolour=(255,255,255),bgcolour=(0,0,0)),
        BUTTON3 = Button(caption="Mary...",msg="Mary had a little lamb", position=(200,100)),
        ROTATOR = CubeRotator(),
        MOVER = CubeMover(),
        BUZZER = CubeBuzzer(),
        ECHO = consoleEchoer(),
        TICKER = Ticker(position = (400, 300), render_left = 0, render_right=350, render_top=0, render_bottom=257),
        TEXT = datasource(),
        linkages = {
            ("PLANE", "outbox") : ("ECHO", "inbox"),
            ("ROTATOR", "outbox") : ("PLANE", "control3d"),
            ("BUTTON1", "outbox") : ("ECHO", "inbox"),
            ("BUTTON2", "outbox") : ("ECHO", "inbox"),
            ("BUTTON3", "outbox") : ("TICKER", "inbox"),
            ("TEXT", "outbox") : ("TICKER", "inbox"),
            ("MOVER", "outbox") : ("CUBE", "control3d"),
        } ).run()
        
    Axon.Scheduler.scheduler.run.runThreads()  
