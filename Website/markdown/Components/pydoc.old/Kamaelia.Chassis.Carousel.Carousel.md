---
pagename: Components/pydoc.old/Kamaelia.Chassis.Carousel.Carousel
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Chassis.Carousel.Carousel
==================================

class Carousel(Axon.Component.component)
----------------------------------------

Carousel(componentFactory,\[make1stRequest\]) -\> new Carousel component

Create a Carousel component that makes child components one at a time
(in carousel fashion) using the supplied factory function.

Keyword arguments: componentFactory \-- function that takes a single
argument and returns a component make1stRequest \-- if True, Carousel
will send an initial \"NEXT\" request. (default=False)

#### Inboxes

-   control :
-   \_control : internal use: to receive \'producerFinished\' or
    \'shutdownMicroprocess\' from child
-   inbox : child\'s inbox
-   next : requests to replace child

#### Outboxes

-   outbox : child\'s outbox
-   signal :
-   \_signal : internal use: for sending \'shutdownMicroprocess\' to
    child
-   requestNext : for requesting new child component

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, componentFactory, make1stRequest)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### handleFinishedChild(self)

Unplugs the child if a shutdownMicroprocess or producerFinished message
is received from it. Also sends a \"NEXT\" request if one has not
already been sent.

### handleNewChild(self)

If data received on \"next\" inbox, removes any existing child and
creates and wires in a new one.

Received data is passed as an argument to the factory function (supplied
at initialisation) that creates the new child.

### main(self)

Main loop

### requestNext(self)

Sends \'next\' out the \'requestNext\' outbox

### shutdown(self)

Returns True if a shutdownMicroprocess or producerFinished message was
received.

### unplugChildren(self)

Sends \'shutdownMicroprocess\' to children and unwires and disowns them.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
