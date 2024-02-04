---
pagename: Components/pydoc.old/Kamaelia.UI.Pygame.VideoOverlay.VideoOverlay
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.UI.Pygame.VideoOverlay.VideoOverlay
============================================

class VideoOverlay(Axon.Component.component)
--------------------------------------------

VideoOverlay() -\> new VideoOverlay component

Displays a pygame video overlay using the PygameDisplay service
component. The overlay is sized and configured by the first frame of
(uncompressed) video data is receives.

NB: Currently, the only supported pixel format is \"YUV420\_planar\"

#### Inboxes

-   control : Shutdown signalling
-   inbox : Receives uncompressed video frames

#### Outboxes

-   outbox : NOT USED
-   signal : Shutdown signalling
-   yuvdata : Sending yuv video data to overlay display service
-   displayctrl : Sending requests to the PygameDisplay service

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### formatChanged(self, frame)

Returns True if frame size or pixel format is new/different for this
frame.

### main(self)

Main loop.

### newOverlay(self, frame)

Request an overlay to suit the supplied frame of data

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
