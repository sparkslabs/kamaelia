---
pagename: Components/pydoc.old/Kamaelia.UI.Pygame.Ticker.Ticker
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.UI.Pygame.Ticker.Ticker
================================

class Ticker(Axon.Component.component)
--------------------------------------

Ticker(\...) -\> new Ticker component.

A pygame based component that displays incoming text as a ticker.

Keyword arguments (all optional): - text\_height \-- Font size in points
(default=39) - line\_spacing \-- (default=text\_height/7) -
background\_colour \-- (r,g,b) background colour of the ticker
(default=(128,48,128)) - text\_colour \-- (r,g,b) colour of text
(default=(232,232,48)) - outline\_colour \-- (r,g,b) colour of the
outline border (default=background\_colour) - outline\_width \-- pixels
width of the border (default=1) - position \-- (x,y) pixels location of
the top left corner - render\_left \-- pixels distance of left of text
from left edge (default=1) - render\_top \-- pixels distance of top of
text from top edge (default=1) - render\_right \-- pixels width of
ticker (default=399) - render\_bottom \-- pixels height of ticker
(default=299)

NOTE: render\_left and render\_top currently behave incorrectly if not
set to 1

#### Inboxes

-   control : Shutdown messages & feedback from PygameDisplay service
-   pausebox : Any message pauses the ticker
-   inbox : Specify (new) filename
-   unpausebox : Any message unpauses the ticker
-   alphacontrol : Transparency of the ticker (0=fully transparent,
    255=fully opaque)

#### Outboxes

-   outbox : NOT USED
-   signal : Shutdown signalling & sending requests to PygameDisplay
    service

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### clearDisplay(self)

Clears the ticker of any existing text.

### handleAlpha(self)

### main(self)

Main loop.

### renderBorder(self, display)

Draws a rectangle to form the \'border\' of the ticker

### requestDisplay(self)

Generator. Gets a display surface from the PygameDisplay service.

Makes the request, then yields 1 until a display surface is returned.

### waitBox(self, boxname)

Generator. yields 1 until data ready on the named inbox.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
