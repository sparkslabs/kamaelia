---
pagename: Components/pydoc.old/Kamaelia.UI.Pygame.Image.Image
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.UI.Pygame.Image.Image
==============================

class Image(Axon.Component.component)
-------------------------------------

Image(\[image\]\[,position\]\[,bgcolour\]\[,size\]\[,displayExtra\]\[,maxpect\])
-\> new Image component

Pygame image display component. Image, and other properties can be
changed at runtime.

Keyword arguments: - image \-- Filename of image (default=None) -
position \-- (x,y) pixels position of top left corner (default=(0,0)) -
bgcolour \-- (r,g,b) background colour (behind the image if size\>image
size) - size \-- (width,height) pixels size of the area to render the
iamge in (default=image size or (240,192) if no image specified) -
displayExtra \-- dictionary of any additional args to pass in request to
PygameDisplay service - maxpect \-- (xscale,yscale) scaling to apply to
image (default=no scaling)

#### Inboxes

-   control : Shutdown messages: shutdownMicroprocess or
    producerFinished
-   bgcolour : Set the background colour
-   callback : Receive callbacks from PygameDisplay
-   inbox : Filename of (new) image
-   events : Place where we recieve events from the outside world
-   alphacontrol : Alpha (transparency) of the image (value 0..255)

#### Outboxes

-   outbox : NOT USED
-   signal : Shutdown signalling: shutdownMicroprocess or
    producerFinished
-   display\_signal : Outbox used for sending signals of various kinds
    to the display service

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, image, position, bgcolour, size, displayExtra, maxpect)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### blitToSurface(self)

Blits the background colour and image file to the surface

### fetchImage(self, newImage)

Load image from specified filename.

self.size is set to image dimensions if self.size is None.

Image is scaled by self.maxpect if self.maxpect evaluates to True.

### main(self)

Main loop.

### waitBox(self, boxname)

Generator. yield\'s 1 until data is ready on the named inbox.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
