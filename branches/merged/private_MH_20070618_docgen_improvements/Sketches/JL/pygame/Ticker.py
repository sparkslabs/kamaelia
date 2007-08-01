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
"""\
====================
Pygame text 'Ticker'
====================

Displays text in pygame a word at a time as a 'ticker'.

NOTE: This component is very much a work in progress. Its capabilities and API
is likely to change substantially in the near future.



Example Usage
-------------

Ticker displaying text from a file::

    Pipeline( RateControlledFileReader("textfile","lines",rate=1000),
              Ticker(position=(100,100))
            ).run()



How does it work?
-----------------

The component requests a display surface from the Pygame Display service
component. This is used as the ticker.

Send strings containing *lines of text* to the Ticker component. Do not send
strings with words split between one string and the next. It displays the
words as a 'ticker' one word at a time. Text is automatically wrapped from one
line to the next. Once the bottom of the ticker is reached, the text
automatically jump-scrolls up a line to make more room.

The text is normalised by the ticker. Multiple spaces between words are
collapsed to a single space. Linefeeds are ignored.

NOTE: 2 consecutive linefeeds currently results in a special message being
sent out of the "signal" outbox. This is work-in-progress aimed at new features.
It is only documented here for completeness and should not be relied upon.

You can set the text size, colour and line spacing. You can also set the
background colour, outline (border) colour and width. You can also specify the
size and position of the ticker

NOTE: Specifying the outline width currently does not work for any value other
than 1.

NOTE: Specify the size of the ticker with the render_right and render_bottom
arguments. Specifying render_left and render_top arguments with values other
than 1 results in parts of the ticker being obscured.

The ticker displays words at a constant rate - it self regulates its display
speed.

Whilst it is running, sending any message to the "pausebox" inbox will pause
the Ticker. It will continue to buffer incoming text. Any message sent to the
"unpausebox" inbox will cause the Ticker to resume.

Whilst running, you can change the transparency of the ticker by sending a value
to the "alphacontrol" inbox between 0 (fully transparent) and 255 (fully opaque)
inclusive.

If a producerFinished message is received on the "control" inbox, this component
will send its own producerFinished message to the "signal" outbox and will
terminate.

However, if the ticker is paused (message sent to "pausebox" inbox) then the
component will ignore messages on its "control" inbox until it is unpaused by
sending a message to its "unpausebox" inbox.
"""


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#
# XXX VOMIT : "control" inbox used for communication with Pygame Display service.
#             This should be changed, so "control" can be used for shutdown
#             signalling.
#
#             similarly the "signal" outbox is used to send stuff to the
#             Pygame Display service. Also must be changed (for the same reasons)
#
#         __init__ args:
#             render_left, render_right, render_top, render_bottom are a bit
#             broken ... specify a render_left or render_top that are > 1
#             and text will spill off the RHS, or not be rendered correctly at
#             the bottom
#
#             outline_width is broken - specify a width > 1 and the outline only
#             appears on the bottom and RHS edges. Scrolling then destroys it.
#
#         main loop:
#             code duplication - checking for messages on "control"
#
#             component cannot be shutdown whilst 'paused' - it just busy waits
#             for a message on the "unpausebox" inbox only, ignoring "control"
#
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

import pygame
import Axon
from Kamaelia.UI.GraphicDisplay import PygameDisplay
from Axon.Ipc import WaitComplete
import time

class Ticker(Axon.Component.component):
   """\
   Ticker(...) -> new Ticker component.

   A pygame based component that displays incoming text as a ticker.

   Keyword arguments (all optional):
   
   - text_height        -- Font size in points (default=39)
   - line_spacing       -- (default=text_height/7)
   - background_colour  -- (r,g,b) background colour of the ticker (default=(128,48,128))
   - text_colour        -- (r,g,b) colour of text (default=(232,232,48))
   - outline_colour     -- (r,g,b) colour of the outline border (default=background_colour)
   - outline_width      -- pixels width of the border (default=1)
   - position           -- (x,y) pixels location of the top left corner
   - render_left        -- pixels distance of left of text from left edge (default=1)
   - render_top         -- pixels distance of top of text from top edge (default=1)
   - render_right       -- pixels width of ticker (default=399)
   - render_bottom      -- pixels height of ticker (default=299)

   NOTE: render_left and render_top currently behave incorrectly if not set to 1
   """
    
   Inboxes = { "inbox"        : "Specify (new) filename",
               "control"      : "Shutdown messages & feedback from Pygame Display service",
               "alphacontrol" : "Transparency of the ticker (0=fully transparent, 255=fully opaque)",
               "pausebox"     : "Any message pauses the ticker",
               "unpausebox"   : "Any message unpauses the ticker",
             }
   Outboxes = { "outbox" : "NOT USED",
                "signal" : "Shutdown signalling & sending requests to Pygame Display service",
              }

   def __init__(self, **argd):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(Ticker,self).__init__()
      #
      # Bunch of initial configs.
      #
      self.text_height = argd.get("text_height",39)
      self.line_spacing = argd.get("line_spacing", self.text_height/7)
      self.background_colour = argd.get("background_colour", (128,48,128))
      self.text_colour = argd.get("text_colour", (232, 232, 48))
      self.outline_colour = argd.get("outline_colour", self.background_colour)
      self.outline_width = argd.get("outline_width", 1)
      self.position = argd.get("position",(1,1))
#      self.left = argd.get("render_left",1)
      self.render_area = pygame.Rect((argd.get("render_left",1),
                                      argd.get("render_top",1),
                                      argd.get("render_right",399),
                                      argd.get("render_bottom",299)))
      self.words_per_second = 8
      self.delay = 1.0/self.words_per_second

   def waitBox(self,boxname):
      """Generator. yields 1 until data ready on the named inbox."""
      waiting = True
      while waiting:
         if self.dataReady(boxname): return
         else: yield 1

   def clearDisplay(self):
       """Clears the ticker of any existing text."""
       self.display.fill(self.background_colour)
       self.renderBorder(self.display)
       self.send({"REDRAW":True, "surface":self.display}, "signal")
            
   def renderBorder(self, display):
      """Draws a rectangle to form the 'border' of the ticker"""
      pygame.draw.rect(display,
                       self.outline_colour,
                       ( self.render_area.left-self.outline_width,
                         self.render_area.top-self.outline_width,
                         self.render_area.width+self.outline_width,
                         self.render_area.height+self.outline_width),
                       self.outline_width)
   

   def requestDisplay(self, **argd):
      """\
      Generator. Gets a display surface from the Pygame Display service.

      Makes the request, then yields 1 until a display surface is returned.
      """
      displayservice = PygameDisplay.getDisplayService()
      self.link((self,"signal"), displayservice)
      self.send(argd, "signal")
      for _ in self.waitBox("control"): yield 1
      display = self.recv("control")
      self.display = display


   def handleAlpha(self):
       if self.dataReady("alphacontrol"):
            alpha = self.recv("alphacontrol")
            self.display.set_alpha(alpha)

   def main(self):
    """Main loop."""
    yield WaitComplete(
          self.requestDisplay(DISPLAYREQUEST=True,
                              callback = (self,"control"),
# SMELL                              transparency = (128,48,128),
                            size = (self.render_area.width, self.render_area.height),
                            position = self.position
                            )
    ) 
    display = self.display

    my_font = pygame.font.Font(None, self.text_height)
    initial_postition = (self.render_area.left,self.render_area.top)
    position = [ self.render_area.left, self.render_area.top ]

    self.clearDisplay()

    maxheight = 0
    last=time.time()
    blankcount = 0
    alpha = -1
    while 1:
       self.handleAlpha()
       if self.shutdown():
           return
       if self.dataReady("inbox"):
          word = self.recv("inbox")
          if word =="\n":
             word = ""
          if "\n" in word:
             lines = word.split("\n")[:-1]
             word = "BONG"
          else:
             lines = [word]
          c = len(lines) #definition of c
          for line in lines:
              word = line
              words = line.split()
              position[0] = initial_postition[0]
              for word in words:
                  self.handleAlpha()
                  if self.dataReady("pausebox"):
                      data = self.recv("pausebox")
                      while not self.dataReady("unpausebox"):
                          yield 1
                      self.recv("unpausebox")
                  if self.shutdown():
                      return
                  last = time.time()
                  word = " " + word
                  
                  alpha = self.display.get_alpha() # remember alpha for surface
                  self.display.set_alpha(255)      # change temporarily so we render text not faded out
                  wordsize = my_font.size(word)
                  word_render= my_font.render(word, 1, self.text_colour)

                  if position[0]+wordsize[0] > self.render_area.right or c > 1:
                     position[0] = initial_postition[0]
                     if position[1] + (maxheight + self.line_spacing)*2 > self.render_area.bottom:
                        display.set_colorkey(None)
                        display.blit(display,
                                     (self.render_area.left, self.render_area.top),
                                     (self.render_area.left, self.render_area.top+self.text_height+self.line_spacing,
                                      self.render_area.width-1, position[1]-self.render_area.top ))

                        pygame.draw.rect(display, 
                                        self.background_colour, 
                                        (self.render_area.left, position[1], 
                                         self.render_area.width-1,self.render_area.top+self.render_area.height-1-(position[1])),
                                        0)
                        # pygame.display.update()
                        if c>1:
                           c = c -1
                     else:
                        position[1] += maxheight + self.line_spacing

                  display.blit(word_render, position)
                  self.send({"REDRAW":True, "surface":self.display}, "signal")
                  position[0] += wordsize[0]
                  if wordsize[1] > maxheight:
                     maxheight = wordsize[1]
                  self.display.set_alpha(alpha)   # put alpha back to what it was
       yield 1

   def shutdown(self):
        if self.dataReady("control"): ### VOMIT : code duplication
          data = self.recv("control")
          if isinstance(data, (Axon.Ipc.producerFinished, Axon.Ipc.shutdownMicroprocess)):
               self.send(Axon.Ipc.producerFinished(message=display), "signal") # pass on the shutdown
               return True
        return False
        

__kamaelia_components__  = ( Ticker, )


if __name__ == "__main__":
   from Kamaelia.Chassis.Pipeline import Pipeline
   # Excerpt from Tennyson's Ulysses
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
         for x in text.split('\n'):
            time.sleep(0.5)
            self.send(x,"outbox")
            yield 1
         self.send(Axon.Ipc.shutdownMicroprocess(), 'signal')

   for _ in range(6):
      Pipeline(datasource(),
               Ticker()
              ).activate()
   Axon.Scheduler.scheduler.run.runThreads()



