#!/usr/bin/python
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
#

import pygame
import Axon

_cat = Axon.CoordinatingAssistantTracker

#"events" : (self, "events"),#


class Bunch: pass

class PygameDisplay(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
   Inboxes={ "inbox" : "Default inbox, not currently used",
             "control": "Default control inbox, not currently used",
             "notify":  "Inbox on which we expect to receive requests for surfaces, overlays and events" }

   def setDisplayService(pygamedisplay, tracker = None):
        "Sets the given pygamedisplay as the service for the selected tracker or the default one."
        if not tracker:
            tracker = _cat.coordinatingassistanttracker.getcat()
        tracker.registerService("pygamedisplay", pygamedisplay, "notify")
   setDisplayService = staticmethod(setDisplayService)

   def getDisplayService(tracker=None): # STATIC METHOD
      "Returns any live pygamedisplay in the system, or creates one for the system to use"
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
      super(PygameDisplay,self).__init__()
      self.width = argd.get("width",800)
      self.height = argd.get("height",600)
#      self.background_colour = argd.get("background_colour", (48,48,128))
      self.background_colour = argd.get("background_colour", (255,255,255))
      self.fullscreen = pygame.FULLSCREEN * argd.get("fullscreen", 0)
      self.next_position = (0,0)
      self.surfaces = []
      self.overlays = []
      self.visibility = {}
      self.events_wanted = {}
      self.surface_to_eventcomms = {}

   def surfacePosition(self,surface):
      position = self.next_position
      self.next_position = position[0]+50, position[1]+50
      return position

   def handleDisplayRequest(self):
         if self.dataReady("notify"):
            message = self.recv("notify")
            if message.get("DISPLAYREQUEST", False):
               callbackservice = message["callback"]
               eventservice = message.get("events", None)
               size = message["size"]
               surface = pygame.Surface(size)
               alpha = message.get("alpha", 255)
               surface.set_alpha(alpha)
               if message.get("transparency", None):
                  surface.set_colorkey(message["transparency"])
#               position = self.surfacePosition(surface)
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

            elif message.get("OVERLAYREQUEST", False):
                size = message["size"]
                pixformat = message["pixformat"]
                position = message.get("position", (0,0))
                overlay = pygame.Overlay(pixformat, size)
                yuvdata = message.get("yuv", ("","",""))

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
                

            elif message.get("ADDLISTENEVENT", None) is not None:
               eventcomms = self.surface_to_eventcomms[str(id(message["surface"]))]
               self.events_wanted[eventcomms][message["ADDLISTENEVENT"]] = True
###               print message

            elif message.get("REMOVELISTENEVENT", None) is not None:
               eventcomms = self.surface_to_eventcomms[str(id(message["surface"]))]
               self.events_wanted[eventcomms][message["REMOVELISTENEVENT"]] = False
# Does this *really* need to be here?
#
#            elif message.get("CHANGEALPHA", None) is not None:
#               surface = self.surface_to_eventcomms[str(id(message["surface"]))]
#               alpha = message.get("alpha", 255)
#               surface.set_alpha(alpha)

   def updateDisplay(self,display):
      display.fill(self.background_colour)
      
      # pre-fetch all waiting events in one go
      events = [ event for event in pygame.event.get() ]
#      if events != []: print events

      for surface, position, callbackcomms, eventcomms in self.surfaces:
         display.blit(surface, position)
         
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
###                  if event.type == pygame.KEYDOWN:
###                     print "BANG", wanted, listener, event
                  # if event contains positional information, remap it
                  # for the surface's coordiate origin
                  if event.type in [ pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN ]:
                     e = Bunch()
                     e.type = event.type
                     pos = event.pos[0],event.pos[1]
                     e.pos  = ( pos[0]-self.visibility[listener][2][0], pos[1]-self.visibility[listener][2][1] )
                     if event.type == pygame.MOUSEMOTION:
                        e.rel = event.rel
                     if event.type == pygame.MOUSEMOTION:
                        e.buttons = event.buttons
                     else:
                        e.button = event.button
                     event = e
                  bundle.append(event)
###                  print "BUNDLE", bundle

            # only send events to listener if we've actually got some
            if bundle != []:
               self.send(bundle, listener)
#               print "Sent "+repr(bundle)+" to "+str(listener)

      # now update overlays
      for theoverlay in self.overlays:

          # receive new image data for display
          if theoverlay['yuvservice']:
              theinbox, _ = theoverlay['yuvservice']
              while self.dataReady(theinbox):
                  theoverlay['yuv'] = self.recv(theinbox)

          # receive position updates
          if theoverlay['posservice']:
              theinbox, _ = theoverlay['posservice']
              while self.dataReady(theinbox):
                  theoverlay['position'] = self.recv(theinbox)
                  theoverlay['overlay'].set_location( (theoverlay['position'], theoverlay['size'] ))

          # redraw the overlay
          theoverlay['overlay'].display( theoverlay['yuv'] )




   def main(self):
      pygame.init()
      display = pygame.display.set_mode((self.width, self.height), self.fullscreen )

      while 1:
         pygame.display.update()
         self.handleDisplayRequest()
         self.updateDisplay(display)
         yield 1


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
                     pygame.display.update()
                  else:
                     position[1] += maxheight + self.line_spacing

               display.blit(word_render, position)
               position[0] += wordsize[0]
               if wordsize[1] > maxheight:
                  maxheight = wordsize[1]

            yield 1

   for _ in range(6):
      pipeline(datasource(),
                      TickTock()
              ).activate()

   Axon.Scheduler.scheduler.run.runThreads()



