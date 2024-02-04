---
pagename: Components/pydoc.old/Kamaelia.UI.Pygame.SpriteScheduler.SpriteScheduler
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.UI.Pygame.SpriteScheduler.SpriteScheduler
==================================================

class SpriteScheduler(Axon.Component.component)
-----------------------------------------------

SpriteScheduler(cat\_args, cat\_sprites, background, display\_surface,
eventHandlerClass) -\> new SpriteScheduler component.

Manages updating and blitting a collection of pygame sprites.
Instantiates an event handler object to handle dispatching of events
from pygame.

Keyword arguments: - cat\_args \-- arguments for event handler class
instantiation - cat\_sprites \-- Pygame sprite objects to be rendered -
background \-- Pygame surface to be rendered as a background image -
display\_surface \-- Pygame surface to render sprites onto -
eventHandlerClass \-- Event handler class, with method:
dispatch(event,source)

#### Inboxes

-   control : NOT USED
-   inbox : NOT USED

#### Outboxes

-   outbox : NOT USED
-   signal : NOT USED

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, cat\_args, cat\_sprites, background, display\_surface, eventHandlerClass)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### main(self)

Main loop.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
