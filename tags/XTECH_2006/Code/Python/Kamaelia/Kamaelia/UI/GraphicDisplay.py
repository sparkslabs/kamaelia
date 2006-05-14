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
"""\
=====================
Pygame Display Access
=====================

This component provides a pygame window. Other components can request to be
notified of events, or ask for a pygame surface or video overlay that will be
rendered onto the display.

PygameDisplay is a service that registers with the Coordinating Assistant
Tracker (CAT).



Example Usage
-------------

See the Button component or VideoOverlay component for examples of how
PygameDisplay can be used.

    

How does it work?
-----------------

PygameDisplay is a service. obtain it by calling the
PygameDisplay.getDisplayService(...) static method. Any existing instance
will be returned, otherwise a new one is automatically created.

Alternatively, if you wish to configure PygameDisplay with options other than
the defaults, create your own instance, then register it as a service by
calling the PygameDisplay.setDisplayService(...) static method. NOTE that it
is only advisable to do this at the top level of your system, as other
components may have already requested and created a PygameDisplay component!

pygame only supports one display window at a time, you must not make more than
one PygameDisplay component.

PygameDisplay listens for requests arriving at its "notify" inbox. A request can
be to:
- create or destroy a surface,
- listen or stop listening to events (you must have already requested a surface)
- move an existing surface
- create a video overlay
- notify of ne to redraw

The requests are described in more detail below.

Once your component has been given the requested surface, it is free to render
onto it whenever it wishes. It should then immediately send a "REDRAW" request
to notify PygameDisplay that the window needs redrawing.

NOTE that you must set the alpha value of the surface before rendering and
restore its previous value before yielding. This is because PygameDisplay uses
the alpha value to control the transparency with which it renders the surface.

Overlays work differently: instead of being given something to render to, you
must provide, in your initial request, an outbox to which you will send raw
yuv (video) data, whenever you want to change the image on the overlay.

PygameDisplay instantiates a private, threaded component to listen for pygame
events. These are then forwarded onto PygameDisplay.

PygameDisplay's main loop continuously renders the surfaces and video overlays
onto the display, and dispatches any pygame events to listeners. The rendering
order is as follows:
- background fill (default=white)
- surfaces (in the order they were requested and created)
- video overlays (in the order they were requested and created)

In summary, to use a surface, your component should:
1. Obtain and wire up to the "notify" inbox of the PygameDisplay service
2. Request a surface
3. Render onto that surface in its main loop

And to use overlays, your component should:
1. Obtain and wire up to the "notify" inbox of the PygameDisplay service
2. Request an overlay, providing an outbox
3. Send yuv data to the outbox 

This component does not terminate. It ignores any messages arriving at its
"control" inbox and does not send anything out of its "outbox" or "signal"
outboxes.


Surfaces
^^^^^^^^
To request a surface, send a dictionary to the "notify" inbox. The following
keys are mandatory::
    {
        "DISPLAYREQUEST" : True,               # this is a 'new surface' request
        "size" : (width,height),               # pixels size for the new surface
        "callback" : (component, "inboxname")  # to send the new surface object to
    }

These keys are optional::
    {
        "position" : (left,top)                # location of the new surface in the window (default=arbitrary)
        "alpha" : 0 to 255,                    # alpha of the surface (255=opaque) (default=255)
        "transparency" : (r,g,b),              # colour that will appear transparent (default=None)
        "events" : (component, "inboxname"),   # to send event notification to (default=None)
    }

To deregister your surface, send a producerFinished(surface) message to the
"notify" inbox. Where 'surface' is your surface. This will remove your surface
and deregister any events you were listening to.

To change the position your surface is rendered at, send a dictionary to the
"notify" inbox containing the folling keys::
    {
        "CHANGEDISPLAYGEO" : True,             # this is a 'change geometry' request
        "surface" : surface,                   # the surface to affect
        "position" : (left,top)                # new location for the surface in the window
    }

The "surface" and "position" keys are optional. However if either are not
specified then there will be no effect!


Listening to events
^^^^^^^^^^^^^^^^^^^
Once your component has obtained a surface, it can request to be notified
of specific pygame events.

To request to listen to a given event, send a dictionary to the "notify" inbox,
containing the following::
    {
        "ADDLISTENEVENT" : pygame_eventtype,     # example: pygame.KEYDOWN
        "surface" : your_surface,
    }

To unsubscribe from a given event, send a dictionary containing::
    {
        "REMOVELISTENEVENT" : pygame_eventtype,
        "surface" : your_surface,
    }
    
Events will be sent to the inbox specified in the "events" key of the
"DISPLAYREQUEST" message. They arrive as a list of pygame event objects.

NOTE: If the event is MOUSEMOTION, MOUSEBUTTONUP or MOUSEBUTTONDOWN then you
will instead receive a replacement object, with the same attributes as the
pygame event, but with the 'pos' attribute adjusted so that (0,0) is the top
left corner of *your* surface.


Video Overlays
^^^^^^^^^^^^^^

To request an overlay, send a dictionary to the "notify" inbox. The following
keys are mandatory::
    {
        "OVERLAYREQUEST" : True,                      # this is a 'new overlay' request
        "size" : (width,height),                      # pixels size of the overlay
        "pixformat" : pygame_pixformat,               # example: pygame.IYUV_OVERLAY
    }

These keys are optional::
    {
        "position" : (left,top),                      # location of the overlay (default=(0,0))
        "yuv" : (ydata,udata,vdata),                  # first frame of yuv data
        "yuvservice" : (component,"outboxname"),      # source of future frames of yuv data
        "positionservice" : (component,"outboxname"), # source of changes to the overlay position
    }

"yuv" enables you to provide the first frame of video data. It should be 3
strings, containing the yuv data for a whole frame.

If you have supplied a (component,outbox) pair as a "yuvservice" then any
(y,u,v) data sent to that outbox will update the video overlay. Again the data
should be 3 strings, containing the yuv data for a *whole frame*.

If you have supplied a "positionservice", then sending (x,y) pairs to the
outbox you specified will update the position of the overlay.

There is currently no mechanism to destroy an overlay.

Redraw requests
^^^^^^^^^^^^^^^

To notify PygameDisplay that it needs to redraw the display, send a dictionary
containing the following keys to the "notify" inbox::
    {
        "REDRAW" : True,             # this is a redraw request
        "surface" : surface          # surface that has been changed
    }
"""

import pygame
import Axon

_cat = Axon.CoordinatingAssistantTracker

#"events" : (self, "events"),#

class Bunch: pass

from Axon.ThreadedComponent import threadedcomponent
import time

class _PygameEventSource(threadedcomponent):
    """\
    Event source for PygameDisplay
    """
    Inboxes = { "inbox" : "NOT USED",
                "control" : "NOT USED",
              }
    Outboxes = { "outbox" : "Pygame event objects, bundled into lists",
                 "signal" : "Not used",
               }
    def main(self):
        while 1:
            time.sleep(0.01)
            eventlist = pygame.event.get()  # and get any others waiting
            
            if eventlist:
                self.send(eventlist,"outbox")
            

class PygameDisplay(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
   """\
   PygameDisplay(...) -> new PygameDisplay component

   Use PygameDisplay.getDisplayService(...) in preference as it returns an
   existing instance, or automatically creates a new one.

   Or create your own and register it with setDisplayService(...)

   Keyword arguments (all optional):
   - width              -- pixels width (default=800)
   - height             -- pixels height (default=600)
   - background_colour  -- (r,g,b) background colour (default=(255,255,255))
   - fullscreen         -- set to True to start up fullscreen, not windowed (default=False)
   """
   
   Inboxes =  { "inbox"   : "Default inbox, not currently used",
                "control" : "NOT USED",
                "notify"  : "Receive requests for surfaces, overlays and events",
                "events"  : "Receive events from source of pygame events",
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
        tracker.registerService("pygamedisplay", pygamedisplay, "notify")
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
         service = tracker.retrieveService("pygamedisplay")
         return service
      except KeyError:
         pygamedisplay = PygameDisplay()
         pygamedisplay.activate()
         PygameDisplay.setDisplayService(pygamedisplay, tracker)
         service=(pygamedisplay,"notify")
         return service
   getDisplayService = staticmethod(getDisplayService)

   def __init__(self, **argd):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(PygameDisplay,self).__init__()
      self.width = argd.get("width",1024)
      self.height = argd.get("height",768)
      self.background_colour = argd.get("background_colour", (255,255,255))
      self.fullscreen = pygame.FULLSCREEN * argd.get("fullscreen", 0)
      self.next_position = (0,0)
      self.surfaces = []
      self.overlays = []
      self.visibility = {}
      self.events_wanted = {}
      self.surface_to_eventcomms = {}

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
         
         while self.dataReady("notify"):
            message = self.recv("notify")
            if isinstance(message, Axon.Ipc.producerFinished): ### VOMIT : mixed data types
               self.needsRedrawing = True
#               print "SURFACE", message
               surface = message.message
#               print "SURFACE", surface
               message.message = None
               message = None
#               print "BEFORE", [id(x[0]) for x in self.surfaces]
               self.surfaces = [ x for x in self.surfaces if x[0] is not surface ]
#               print "AFTER", self.surfaces
#               print "Hmm...", self.surface_to_eventcomms.keys()
               try:
                   eventcomms = self.surface_to_eventcomms[str(id(surface))]
               except KeyError:
                   # This simply means the component wasn't listening for events!
                   pass
               else:
#                   print "EVENT OUTBOX:", eventcomms
                   self.visibility = None
                   try:
                       self.removeOutbox(eventcomms)
                   except:
                       "This sucks"
                       pass
#                   print "REMOVED OUTBOX"
            elif message.get("DISPLAYREQUEST", False):
               self.needsRedrawing = True
               callbackservice = message["callback"]
               eventservice = message.get("events", None)
               size = message["size"]
               surface = pygame.Surface(size)
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
               self.link((self, callbackcomms), callbackservice)
               self.send(surface, callbackcomms)
               self.surfaces.append( (surface, position, callbackcomms, eventcomms) )

            elif message.get("ADDLISTENEVENT", None) is not None:
               eventcomms = self.surface_to_eventcomms[str(id(message["surface"]))]
               self.events_wanted[eventcomms][message["ADDLISTENEVENT"]] = True

            elif message.get("REMOVELISTENEVENT", None) is not None:
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
                            (surface, position, callbackcomms, eventcomms) = self.surfaces[c]
                            new_position = message.get("position", position)
                            self.surfaces[c] = (surface, new_position, callbackcomms, eventcomms)
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
                message["surface"]
                
                
# Does this *really* need to be here?
#
#            elif message.get("CHANGEALPHA", None) is not None:
#               surface = self.surface_to_eventcomms[str(id(message["surface"]))]
#               alpha = message.get("alpha", 255)
#               surface.set_alpha(alpha)

   def updateDisplay(self,display):
      """\
      Render all surfaces and overlays onto the specified display surface.

      Also dispatches events to event handlers.
      """
      display.fill(self.background_colour)
      
      for surface, position, callbackcomms, eventcomms in self.surfaces:
         display.blit(surface, position)
         
      for theoverlay in self.overlays:
          theoverlay['overlay'].display( theoverlay['yuv'] )
   
   def updateOverlays(self):
      #
      # Update overlays - We do these second, so as to avoid flicker.
      #
      for theoverlay in self.overlays:

          # receive new image data for display
          if theoverlay['yuvservice']:
              self.needsRedrawing=True
              theinbox, _ = theoverlay['yuvservice']
              while self.dataReady(theinbox):
                  yuv = self.recv(theinbox)

                  # transform (y,u,v) to (y,v,u) because pygame seems to want that(!)
                  if len(yuv) == 3:
                      theoverlay['yuv'] = (yuv[0], yuv[2], yuv[1])
                  else:
                      theoverlay['yuv'] = yuv

          # receive position updates
          if theoverlay['posservice']:
              self.needsRedrawing=True
              theinbox, _ = theoverlay['posservice']
              while self.dataReady(theinbox):
                  theoverlay['position'] = self.recv(theinbox)
                  theoverlay['overlay'].set_location( (theoverlay['position'], 
                                                       (theoverlay['size'][0]/2, theoverlay['size'][1])
                                                      ))
              
   
   def handleEvents(self):
      # pre-fetch all waiting events in one go
      while self.dataReady("events"):
            events = self.recv("events")
       
            for event in events:
                if event.type in [ pygame.VIDEORESIZE, pygame.VIDEOEXPOSE ]:
                    self.needsRedrawing = True
       
            for surface, position, callbackcomms, eventcomms in self.surfaces:
                # see if this component is interested in events
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

   def main(self):
      """Main loop."""
      pygame.init()
      pygame.mixer.quit()
      display = pygame.display.set_mode((self.width, self.height), self.fullscreen|pygame.DOUBLEBUF )
      
      eventsource = _PygameEventSource().activate()
      self.addChildren(eventsource)
      self.link( (eventsource,"outbox"), (self,"events") )
      
      while 1:
         self.needsRedrawing = False
         self.handleEvents()
         self.handleDisplayRequest()
         self.updateOverlays()
         
         if self.needsRedrawing:
             self.updateDisplay(display)
             pygame.display.update()
             
         self.pause()
         yield 1

__kamaelia_components__  = ( PygameDisplay, )

if __name__ == "__main__":
   component = Axon.Component.component
   from Kamaelia.Util.PipelineComponent import pipeline
   # Excerpt from Tennyson's Ulysses
   text = """\
The lights begin to twinkle from the rocks;
The long day wanes; the slow moon climbs; the deep
Moans round with many voices.  Come, my friends.
'T is not too late to seek a newer world.
Push off, and sitting well in order smite
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
   class datasource(component):
      def main(self):
         for x in text.split():
            self.send(x,"outbox")
            yield 1

   class TickTock(component):
      def __init__(self, **argd):
         super(TickTock,self).__init__()
         #
         # Bunch of initial configs.
         #
         self.text_height = argd.get("text_height",39)
         self.line_spacing = argd.get("line_spacing", self.text_height/7)
         self.background_colour = argd.get("background_colour", (48,48,128))
         self.background_colour = argd.get("background_colour", (128,48,128))
         self.text_colour = argd.get("text_colour", (232, 232, 48))
         self.outline_colour = argd.get("outline_colour", (128,232,128))
         self.outline_width = argd.get("outline_width", 1)
         self.render_area = pygame.Rect((argd.get("render_left",1),
                                         argd.get("render_top",1),
                                         argd.get("render_right",399),
                                         argd.get("render_bottom",299)))

      def waitBox(self,boxname):
         waiting = True
         while waiting:
            if self.dataReady(boxname): return
            else: yield 1

      def main(self):
         displayservice = PygameDisplay.getDisplayService()
         self.link((self,"signal"), displayservice)
         self.send({ "DISPLAYREQUEST":True, "callback" : (self,"control"), "size": (400,300)}, "signal")
         for _ in self.waitBox("control"): yield 1
         display = self.recv("control")

         my_font = pygame.font.Font(None, self.text_height)
         initial_postition = (self.render_area.left,self.render_area.top)
         position = [ self.render_area.left, self.render_area.top ]

         display.fill(self.background_colour)
         pygame.draw.rect(display,
                          self.outline_colour,
                          ( self.render_area.left-self.outline_width,
                            self.render_area.top-self.outline_width,
                            self.render_area.width+self.outline_width,
                            self.render_area.height+self.outline_width),
                          self.outline_width)
         self.send( {"REDRAW":True, "surface":display}, "signal" )

         maxheight = 0
         while 1:
            if self.dataReady("inbox"):
               word = self.recv("inbox")
               word = " " + word
               wordsize = my_font.size(word)
               word_render= my_font.render(word, 1, self.text_colour)

               if position[0]+wordsize[0] > self.render_area.right:
                  position[0] = initial_postition[0]
                  if position[1] + (maxheight + self.line_spacing)*2 > self.render_area.bottom:
                     display.blit(display,
                                  (self.render_area.left, self.render_area.top),
                                  (self.render_area.left, self.render_area.top+self.text_height+self.line_spacing,
                                     self.render_area.width-1, position[1]-self.render_area.top ))
                     pygame.draw.rect(display, 
                                     self.background_colour, 
                                     (self.render_area.left, position[1], 
                                      self.render_area.width-1,self.render_area.top+self.render_area.height-1-(position[1])),
                                     0)
                     self.send( {"REDRAW":True, "surface":display}, "signal" )
                  else:
                     position[1] += maxheight + self.line_spacing

               display.blit(word_render, position)
               self.send( {"REDRAW":True, "surface":display}, "signal" )
               position[0] += wordsize[0]
               if wordsize[1] > maxheight:
                  maxheight = wordsize[1]

            yield 1

   for _ in range(6):
      pipeline(datasource(),
                      TickTock()
              ).activate()

   Axon.Scheduler.scheduler.run.runThreads()


"""
"""