---
pagename: Components/pydoc.old/Kamaelia.UI.Pygame.BasicSprite.BasicSprite
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.UI.Pygame.BasicSprite.BasicSprite
==========================================

class BasicSprite(pygame.sprite.Sprite,Axon.Component.component)
----------------------------------------------------------------

BasicSprite(image\[,position\]) -\> new BasicSprite component.

A sprite for a pygame application. Can be changed, moved, scaled and
rotated on the fly.

Does not use the standard component \'main\' loop - must be used in
conjunction with SpriteSheduler.

Keyword arguments: - image \-- pygame surface containing the image -
position \-- (x,y) pixels position of the top left corner
(default=(10,10))

#### Inboxes

-   control : NOT USED
-   scaler : Change size (1.0=original)
-   inbox : NOT USED
-   rotator : Rotate by \'n\' degrees counterclockwise
-   translation : Change position to (x,y) in pixels
-   imaging : Change the image

#### Outboxes

-   outbox : NOT USED
-   signal : Diagnostic messages

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### main(self)

Main loop

### pause(self)

Set paused flag, and signal \"pause\"

### shutdown(self)

Send shutdown message

### sprite\_logic(self)

Effectively the main loop. Listens for messages on inboxes and adjusts
the sprite accordingly, unless \'paused\'.

### togglePause(self)

Toggle between paused and unpaused states

### unpause(self)

Unset paused flag, and signal \"unpause\"

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
