---
pagename: Components/pydoc.old/Kamaelia.Codec.Dirac.DiracDecoder
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Codec.Dirac.DiracDecoder
=================================

class DiracDecoder(Axon.Component.component)
--------------------------------------------

DiracDecoder() -\> new Dirac decoder component

Creates a component that decodes Dirac video.

#### Inboxes

-   control : for shutdown signalling
-   inbox : Strings containing an encoded dirac video stream

#### Outboxes

-   outbox : YUV decoded video frames
-   signal : for shutdown/completion signalling

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

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
