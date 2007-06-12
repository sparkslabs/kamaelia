#!/usr/bin/env python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
from Axon.ThreadedComponent import threadedcomponent
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

from Kamaelia.UI.PygameDisplay import PygameDisplay
from Util3D import *
import time

_cat = Axon.CoordinatingAssistantTracker

class Bunch: pass

class Display3D(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):#(Axon.ThreadedComponent.threadedadaptivecommscomponent):
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
    
        
    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Display3D,self).__init__()
        self.caption = argd.get("title", "http://kamaelia.sourceforge.net")
        self.width = argd.get("width",800)
        self.height = argd.get("height",600)
        self.background_colour = argd.get("background_colour", (255,255,255))
        self.fullscreen = pygame.FULLSCREEN * argd.get("fullscreen", 0)
        self.showFPS = argd.get("showFPS", True)
        
        # data for FPS measurement
        self.lastTime = 0
        self.fps = 0
        self.fpscounter = 0

        # 3D component handling
        self.ogl_objects = []
        self.ogl_names = {}
        self.ogl_sizes = {}
        self.ogl_displaylists = {}
        self.ogl_transforms = {}
        self.ogl_nextName = 1

        # Eventspies (receive events of other components)
        self.eventspies = []

        # pygame component handling
        self.pygame_surfaces = []
        self.pygame_sizes = {}
        self.pygame_positions = {}
        self.pygame_pow2surfaces = {}
        self.pygame_texnames = {}
        # used for surface positioning
        self.next_position = (0,0)
        
        # pygame wrapping
        self.wrappedsurfaces = []
        self.wrapper_requestcomms = {}

        # Event handling
        self.eventcomms = {}
        self.eventservices = {}
        self.eventswanted = {}
        
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
        
        # projection matrix
        glMatrixMode(GL_PROJECTION)                 
        glLoadIdentity()                                
        gluPerspective(self.perspectiveAngle, self.aspectRatio, self.nearPlaneDist, self.farPlaneDist)
    
        
    def handleDisplayRequest(self):
            while self.dataReady("notify"):
                message = self.recv("notify")
                if isinstance(message, Axon.Ipc.producerFinished): ### VOMIT : mixed data types
                    surface = message.message
                    message.message = None
                    message = None
                    self.surfaces = [ x for x in self.surfaces if x[0] is not surface ]
                    try:
                         eventcomms = self.surface_to_eventcomms[str(id(surface))]
                    except KeyError:
                         pass
                    else:
                         self.visibility = None
                         try:
                              self.removeOutbox(eventcomms)
                         except:
                              "This sucks"
                              pass
                elif message.get("OGL_DISPLAYREQUEST", False):
                    # store object
                    ident = message.get("objectid")
                    self.ogl_objects.append(ident)
                    self.ogl_sizes[ident] = message.get("size")
                    # generate and store an ogl name for the requesting object
                    ogl_name = self.ogl_nextName
                    self.ogl_nextName += 1
                    self.ogl_names[ident] = ogl_name
                    # connect to eventcallback
                    eventservice = message.get("events", None)
                    if eventservice is not None:
                        eventcomms = self.addOutbox("eventsfeedback")
                        self.eventcomms[ident] = eventcomms
                        self.link((self,eventcomms), eventservice)
                        self.eventswanted[ident] = {}
                    
                    callbackservice = message.get("callback")
                    callbackcomms = self.addOutbox("displayerfeedback")
                    self.link((self, callbackcomms), callbackservice)
                    self.send(ogl_name, callbackcomms)
                    
                elif message.get("EVENTSPYREQUEST", False):
                    ident = message.get("objectid")
                    self.eventspies.append(ident)
                    
                    victim = message.get("victim")
                    
                    eventservice = message.get("events", None)
                    if eventservice is not None:
                        eventcomms = self.addOutbox("eventsfeedback")
                        self.eventcomms[ident] = eventcomms
                        self.link((self,eventcomms), eventservice)
                        self.eventswanted[ident] = {}

                    ogl_name = self.ogl_names[victim]                    
                    callbackservice = message.get("callback")
                    callbackcomms = self.addOutbox("displayerfeedback")
                    self.link((self, callbackcomms), callbackservice)
                    self.send(ogl_name, callbackcomms)

                elif message.get("DISPLAYLIST_UPDATE", False):
                    ident = message.get("objectid")
                    try:
                        glDeleteLists(self.ogl_displaylists[ident], 1)
                    except KeyError: pass
                    self.ogl_displaylists[ident] = message.get("displaylist")
                    
                elif message.get("TRANSFORM_UPDATE", False):
                    ident = message.get("objectid")
                    self.ogl_transforms[ident] = message.get("transform")
                    
                elif message.get("ADDLISTENEVENT", False):
                    ident = message.get("objectid")
                    if ident is None:
                        ident = id(message.get("surface", None))
    
                    if ident in self.wrappedsurfaces:
                        self.send(message, self.wrapper_requestcomms[id(surface)])
                    else:
                        self.eventswanted[ident][message.get("ADDLISTENEVENT")] = True
                    
                elif message.get("REMOVELISTENEVENT", False):
                    ident = message.get("objectid")
                    if ident is None:
                        ident = message.get("surface", None)
    
                    if ident in self.wrappedsurfaces:
                        self.send(message, self.wrapper_requestcomms[id(surface)])
                    else:
                       self.eventswanted[ident][message.get("REMOVELISTENEVENT")] = False

                elif message.get("DISPLAYREQUEST", False):
                    # get communication services
                    callbackservice = message["callback"]
                    eventservice = message.get("events", None)
                
                    # get size
                    size  = message["size"]
                    
                    # create surface
                    surface = pygame.Surface(size)
                    self.pygame_surfaces.append(surface)
                    # save size
                    self.pygame_sizes[id(surface)] = size

                    #create another surface, with dimensions a power of two
                    # this is needed because otherwise texturing is REALLY slow
                    pow2size = (int(2**(ceil(log(size[0], 2)))), int(2**(ceil(log(size[1], 2)))))
                    pow2surface = pygame.Surface(pow2size)
                    self.pygame_pow2surfaces[id(surface)] = pow2surface

                    # handle transparency
                    alpha = message.get("alpha", 255)
                    surface.set_alpha(alpha)
                    if message.get("transparency", None):
                        surface.set_colorkey(message["transparency"])
                    
                    # get or generate position
                    position = message.get("position", self.surfacePosition(surface))
                    self.pygame_positions[id(surface)] = position

                    # handle event comms
                    if eventservice is not None:
                        # save eventservice for later use
                        self.eventservices[id(surface)] = eventservice
                        # link eventservice
                        eventcomms = self.addOutbox("eventsfeedback")
                        self.eventswanted[id(surface)] = {}
                        self.link((self,eventcomms), eventservice)
                        self.eventcomms[id(surface)] = eventcomms

                    # generate texture name
                    texname = glGenTextures(1)
                    self.pygame_texnames[id(surface)] = texname
                    
                    # link callback communications
                    callbackcomms = self.addOutbox("displayerfeedback")
                    self.link((self, callbackcomms), callbackservice)
                    self.send(surface, callbackcomms)

                elif message.get("REDRAW", False):
                    surface = message["surface"]
                    self.updatePygameTexture(surface, self.pygame_pow2surfaces[id(surface)], self.pygame_texnames[id(surface)])

                elif message.get("WRAPPERREQUEST", False):
                    # get and store surface to wrap
                    surface = message.get("surface")
                    self.wrappedsurfaces.append(id(surface))
                    # get and link callback comms
                    callbackservice = message["wrapcallback"]
                    callbackcomms = self.addOutbox("wrapfeedback")
                    self.link((self,callbackcomms), callbackservice)
                    # get and link eventrequest comms
                    eventrequestservice = message["eventrequests"]
                    eventrequestcomms = self.addOutbox("eventrequests")
                    self.link((self,eventrequestcomms), eventrequestservice)
                    self.wrapper_requestcomms[id(surface)] = eventrequestcomms
                    # find corresponding pow2surface
                    pow2surface = self.pygame_pow2surfaces[id(surface)]
                    #determine texture coordinate lengths
                    tex_w = float(surface.get_width())/float(pow2surface.get_width())
                    tex_h = float(surface.get_height())/float(pow2surface.get_height())
                    # generate response
                    response = { "texname": self.pygame_texnames[id(surface)],
                                           "texsize": (tex_w, tex_h),
                                           "size": self.pygame_sizes[id(surface)] }
                    try:
                        response["eventservice"] = self.eventservices[id(surface)]
                        response["eventswanted"] = self.eventswanted[id(surface)]
                    except KeyError:
                        response["eventservice"] = None
                        response["eventswanted"] = None
                    # send response
                    self.send(response, callbackcomms)
        

    def handleEvents(self):
        # pre-fetch all waiting events in one go
        events = [ event for event in pygame.event.get() ]

        # Handle 3D object events
        for event in events:
            if event.type in [ pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN ]:
                # compose event data
                e = Bunch()
                e.type = event.type
                if event.type in [ pygame.KEYDOWN, pygame.KEYUP ]:
                    # key is the only data in keyevents
                    e.key = event.key
                else: #  type is one of pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN
                    # position
                    e.pos = event.pos
                    # determine intersection ray
                    xclick = float(event.pos[0]-self.width/2)*self.farPlaneWidth/float(self.width)
                    yclick = float(-event.pos[1]+self.height/2)*self.farPlaneHeight/float(self.height)
                    e.dir = Vector(xclick, yclick, -self.farPlaneDist).norm()
                    # determine which objects have been hit
                    e.hitobjects = self.doPicking(event.pos)
                    # set specific event fields
                    if event.type in [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN]:
                        e.button = event.button
                    if event.type == pygame.MOUSEMOTION:
                        e.rel = event.rel
                        e.buttons = event.buttons
                  
                # send events to objects
                for ident in self.ogl_objects + self.eventspies:
                    try:
                        if self.eventswanted[ident][e.type]:
                            self.send(e, self.eventcomms[ident])
                    except KeyError: pass

        # Handle Pygame events
        for surface in self.pygame_surfaces:
            try:
                eventcomms = self.eventcomms[id(surface)]
                if eventcomms is not None:
                    bundle = []
                    for event in events:
                        wanted = False
                        try:   wanted = self.eventswanted[id(surface)][event.type]
                        except KeyError: pass
                        if wanted:
                            # if event contains positional information, remap it
                            # for the surface's coordiate origin
                            if event.type in [ pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN ]:
                                # skip wrapped components (they get events from their wrappers)
                                if id(surface) in self.wrappedsurfaces: continue
                                # assemble event
                                e = Bunch()
                                e.type = event.type
                                pos = event.pos[0],event.pos[1]
                                surfpos = self.pygame_positions[id(surface)]
                                # determine position on surface
                                e.pos  = ( pos[0]-surfpos[0], pos[1]-surfpos[1] )
                                if event.type == pygame.MOUSEMOTION:
                                    e.rel = event.rel
                                if event.type == pygame.MOUSEMOTION:
                                    e.buttons = event.buttons
                                else:
                                    e.button = event.button
                                event = e

                            bundle.append(event)

                    # only send events to listener if we've actually got some
                    if bundle != []:
                        self.send(bundle, eventcomms)
            except KeyError: pass
    

    def updateDisplay(self):
        #display pygame components
        self.drawPygameSurfaces()

        # draw all 3D objects
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        for obj in self.ogl_objects:
            try:
                glLoadMatrixf(self.ogl_transforms[obj].getMatrix())
                glCallList(self.ogl_displaylists[obj])
            except KeyError: pass
        glPopMatrix()
        
        # show frame
        glFlush()
        pygame.display.flip()
        
        # clear drawing buffer
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        

    def main(self):
        """Main loop."""
        while 1:
            #show fps
            if self.showFPS:
                self.fpscounter += 1
                if self.fpscounter > 100:
                    # determine fps
                    currentTime = time.time()
                    self.fps = 100/(currentTime-self.lastTime)
                    self.lastTime = currentTime
                    pygame.display.set_caption("%s FPS:%d" % (self.caption, self.fps) )
                    self.fpscounter = 0

            self.handleDisplayRequest()
            self.handleEvents()
            self.updateDisplay()
            yield 1
#            time.sleep(0.0001)


    def doPicking(self, pos):
        # object picking
        glSelectBuffer(512)
        glRenderMode(GL_SELECT)
        # prepare matrices
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluPickMatrix(pos[0], self.height-pos[1], 1, 1)
        gluPerspective(self.perspectiveAngle, self.aspectRatio, self.nearPlaneDist, self.farPlaneDist)
        # "draw" objects in select mode
        glInitNames()
        glPushName(0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        for obj in self.ogl_objects:
            try:
                glLoadMatrixf(self.ogl_transforms[obj].getMatrix())
                glLoadName(self.ogl_names[obj])
                glCallList(self.ogl_displaylists[obj])
            except KeyError: pass
        glPopMatrix()

        # restore matrices
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        # force completion
        glFlush()

        # process hits                
        hits = glRenderMode(GL_RENDER)
        
        # return list of hit objects
        return [hit[2][0] for hit in hits]


    def updatePygameTexture(self, surface, pow2surface, texname):
#        print "UPDATE", texname
        # blit component surface to power of 2 sized surface
        pow2surface.blit(surface, (0,0))
        # set surface as texture
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texname)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        textureData = pygame.image.tostring(pow2surface, "RGBX", 1)
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, pow2surface.get_width(), pow2surface.get_height(), 0,
                        GL_RGBA, GL_UNSIGNED_BYTE, textureData );
        glDisable(GL_TEXTURE_2D)


    def drawPygameSurfaces(self):
        # disable depth testing temporarely to ensure that pygame components
        # are on top of everything
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        for surface in self.pygame_surfaces:
            # skip surfaces which get wrapped
            if id(surface) in self.wrappedsurfaces: continue

            # get needed vars
            texname = self.pygame_texnames[id(surface)]
            position = self.pygame_positions[id(surface)]
            size = self.pygame_sizes[id(surface)]
            pow2surface = self.pygame_pow2surfaces[id(surface)]

            # create texture if not already done
            if not glIsTexture(texname):
                self.updatePygameTexture(surface, pow2surface, texname)

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
  
    def surfacePosition(self,surface):
        """Returns a suggested position for a surface. No guarantees its any good!"""
        position = self.next_position
        self.next_position = position[0]+50, position[1]+50
        return position

        
       



if __name__=='__main__':
        
    Axon.Scheduler.scheduler.run.runThreads()  
