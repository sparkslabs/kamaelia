---
pagename: Components/pydoc.old/Kamaelia.UI.Pygame.Button.Button
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.UI.Pygame.Button.Button
================================

class Button(Axon.Component.component)
--------------------------------------

Button(\...) -\> new Button component.

Create a button widget in pygame, using the PygameDisplay service. Sends
a message out of its outbox when clicked.

Keyword arguments (all optional): - caption \-- text (default=\"Button
\<component id\>\") - position \-- (x,y) position of top left corner in
pixels - margin \-- pixels margin between caption and button edge
(default=8) - bgcolour \-- (r,g,b) fill colour (default=(224,224,224)) -
fgcolour \-- (r,g,b) text colour (default=(0,0,0)) - msg \-- sent when
clicked (default=(\"CLICK\",self.id)) - key \-- if not None, pygame
keycode to trigger click (default=None) - transparent \-- draw
background transparent if True (default=False)

#### Inboxes

-   control : For shutdown messages
-   callback : Receive callbacks from PygameDisplay
-   inbox : Receive events from PygameDisplay

#### Outboxes

-   outbox : button click events emitted here
-   signal : For shutdown messages
-   display\_signal : Outbox used for communicating to the display
    surface

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, caption, position, margin, bgcolour, fgcolour, msg, key, transparent)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### blitToSurface(self)

Clears the background and renders the text label onto the button
surface.

### buildCaption(self, text)

Pre-render the text to go on the button label.

### main(self)

Main loop.

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
