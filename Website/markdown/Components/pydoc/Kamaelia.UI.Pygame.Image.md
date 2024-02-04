---
pagename: Components/pydoc/Kamaelia.UI.Pygame.Image
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[Image](/Components/pydoc/Kamaelia.UI.Pygame.Image.html){.reference}
=================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Image](/Components/pydoc/Kamaelia.UI.Pygame.Image.Image.html){.reference}**
:::

-   [Pygame image display](#382){.reference}
    -   [Example Usage](#383){.reference}
    -   [How does it work?](#384){.reference}
:::

::: {.section}
Pygame image display {#382}
====================

Component for displaying an image on a pygame display. Uses the Pygame
Display service component.

The image can be changed at any time.

::: {.section}
[Example Usage]{#example-usage} {#383}
-------------------------------

Display that rotates rapidly through a set of images:

``` {.literal-block}
imagefiles = [ "imagefile1", "imagefile2", ... ]

class ChangeImage(Axon.Component.component):
    def __init__(self, images):
        super(ChangeImage,self).__init__()
        self.images = images

    def main(self):
        while 1:
            for image in self.images:
                self.send( image, "outbox")
                print "boing",image
                for i in range(0,100):
                    yield 1

image = Image(image=None, bgcolour=(0,192,0))
ic    = ChangeImage(imagefiles)

Pipeline(ic, image).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#384}
--------------------------------------

This component requests a display surface from the Pygame Display
service component and renders the specified image to it.

The image, and other properties can be changed later by sending messages
to its \"inbox\", \"bgcolour\" and \"alphacontrol\" inboxes.

Note that the size of display area is fixed after initialisation. If an
initial size, or image is specified then the size is set to that,
otherwise a default value is used.

Change the image at any time by sending a new filename to the \"inbox\"
inbox. If the image is larger than the \'size\', then it will appear
cropped. If it is smaller, then the Image component\'s \'background
colour\' will show through behind it. The image is always rendered
aligned to the top left corner.

If this component receives a shutdownMicroprocess or producerFinished
message on its \"control\" inbox, then this will be forwarded out of its
\"signal\" outbox and the component will then terminate.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}.[Image](/Components/pydoc/Kamaelia.UI.Pygame.Image.html){.reference}.[Image](/Components/pydoc/Kamaelia.UI.Pygame.Image.Image.html){.reference}
============================================================================================================================================================================================================================================================================================================================

::: {.section}
class Image([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Image}
---------------------------------------------------------------------------------------------

Image(\[image\]\[,position\]\[,bgcolour\]\[,size\]\[,displayExtra\]\[,maxpect\])
-\> new Image component

Pygame image display component. Image, and other properties can be
changed at runtime.

Keyword arguments:

-   image \-- Filename of image (default=None)
-   position \-- (x,y) pixels position of top left corner
    (default=(0,0))
-   bgcolour \-- (r,g,b) background colour (behind the image if
    size\>image size)
-   size \-- (width,height) pixels size of the area to render the iamge
    in (default=image size or (240,192) if no image specified)
-   displayExtra \-- dictionary of any additional args to pass in
    request to Pygame Display service
-   maxpect \-- (xscale,yscale) scaling to apply to image (default=no
    scaling)

::: {.section}
### [Inboxes]{#symbol-Image.Inboxes}

-   **control** : Shutdown messages: shutdownMicroprocess or
    producerFinished
-   **bgcolour** : Set the background colour
-   **callback** : Receive callbacks from Pygame Display
-   **inbox** : Filename of (new) image
-   **events** : Place where we recieve events from the outside world
-   **alphacontrol** : Alpha (transparency) of the image (value 0..255)
:::

::: {.section}
### [Outboxes]{#symbol-Image.Outboxes}

-   **outbox** : NOT USED
-   **signal** : Shutdown signalling: shutdownMicroprocess or
    producerFinished
-   **display\_signal** : Outbox used for sending signals of various
    kinds to the display service
:::

::: {.section}
### Methods defined here

::: {.container}
::: {.boxright}
**Warning!**

You should be using the inbox/outbox interface, not these methods
(except construction). This documentation is designed as a roadmap as to
their functionalilty for maintainers and new component developers.
:::
:::

::: {.section}
#### [\_\_init\_\_(self\[, image\]\[, position\]\[, bgcolour\]\[, size\]\[, displayExtra\]\[, maxpect\]\[, expect\_file\_strings\])]{#symbol-Image.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [blitToSurface(self)]{#symbol-Image.blitToSurface}

Blits the background colour and image file to the surface
:::

::: {.section}
#### [fetchImage(self, newImage)]{#symbol-Image.fetchImage}

Load image from specified filename.

self.size is set to image dimensions if self.size is None.

Image is scaled by self.maxpect if self.maxpect evaluates to True.
:::

::: {.section}
#### [imageFromString(self, newImage)]{#symbol-Image.imageFromString}
:::

::: {.section}
#### [main(self)]{#symbol-Image.main}

Main loop.
:::

::: {.section}
#### [waitBox(self, boxname)]{#symbol-Image.waitBox}

Generator. yield\'s 1 until data is ready on the named inbox.
:::
:::

::: {.section}
:::
:::
:::
:::

::: {.section}
Feedback
========

Got a problem with the documentation? Something unclear that could be
clearer? Want to help improve it? Constructive criticism is very welcome
- especially if you can suggest a better rewording!

Please leave you feedback
[here](../../../cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1142023701){.reference}
in reply to the documentation thread in the Kamaelia blog.
:::

*\-- Automatic documentation generator, 05 Jun 2009 at 03:01:38 UTC/GMT*
