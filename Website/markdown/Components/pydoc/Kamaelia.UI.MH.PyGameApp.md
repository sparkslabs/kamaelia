---
pagename: Components/pydoc/Kamaelia.UI.MH.PyGameApp
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[MH](/Components/pydoc/Kamaelia.UI.MH.html){.reference}.[PyGameApp](/Components/pydoc/Kamaelia.UI.MH.PyGameApp.html){.reference}
=============================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [PyGameApp](/Components/pydoc/Kamaelia.UI.MH.PyGameApp.PyGameApp.html){.reference}**
:::

-   [Simple Pygame application framework](#352){.reference}
    -   [Example Usage](#353){.reference}
    -   [How does it work?](#354){.reference}
:::

::: {.section}
Simple Pygame application framework {#352}
===================================

A component that sets up a pygame display surface and provides a main
loop and simple event dispatch framework.

The rendering surface is requested from the Pygame Display service
component, so this component can coexist with other components using
pygame.

::: {.section}
[Example Usage]{#example-usage} {#353}
-------------------------------

::

:   class SimpleApp1(PyGameApp):

    > def initialiseComponent(self):
    > :   self.addHandler(MOUSEBUTTONDOWN, lambda event :
    >     self.mousedown(event))
    >
    > def mainLoop(self):
    > :   \... draw and do other stuff here\... return 1
    >
    > def mousedown(self, event):
    > :   print \"Mouse down!\"

    app = SimpleApp1( (800,600) ).run()
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#354}
--------------------------------------

Subclass this component to implement your own pygame \'app\'. Replace
the mainLoop() stub with your own code to redraw the display surface
etc. This method will be called every cycle - do not incorporate your
own loop!

The self.screen attribute is the pygame surface you should render to.

The component provides a simple event dispatch framework. Call
addHandler and removeHandler to register and deregister handlers from
events.

More than one handler can be registered for a given event. They are
called in the order in which they were registered. If a handler returns
True then the event is \'claimed\' and no further handlers will be
called.

The component will terminate if the user clicks the close button on the
pygame display window, however your mainLoop() method will not be
notified, and there is no specific \'quit\' event handler.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[MH](/Components/pydoc/Kamaelia.UI.MH.html){.reference}.[PyGameApp](/Components/pydoc/Kamaelia.UI.MH.PyGameApp.html){.reference}.[PyGameApp](/Components/pydoc/Kamaelia.UI.MH.PyGameApp.PyGameApp.html){.reference}
================================================================================================================================================================================================================================================================================================================================

::: {.section}
class PyGameApp([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-PyGameApp}
-------------------------------------------------------------------------------------------------

PyGameApp(screensize\[,caption\]\[,transparency\]\[,position\]) -\> new
PyGameApp component.

Creates a PyGameApp component that obtains a pygame display surface and
provides an internal pygame event dispatch mechanism.

Subclass to implement your own pygame \"app\".

Keyword arguments:

-   screensize \-- (width,height) of the display area (default =
    (800,600))
-   caption \-- Caption for the pygame window (default = \"Topology
    Viewer\")
-   fullscreen \-- True to start up in fullscreen mode (default = False)
-   transparency \-- None, or (r,g,b) colour to make transparent
-   position \-- None, or (left,top) position for surface within pygame
    window

::: {.section}
### [Inboxes]{#symbol-PyGameApp.Inboxes}

-   **control** : NOT USED
-   **displaycontrol** : Replies from Pygame Display service
-   **inbox** : NOT USED
-   **events** : Event notifications from Pygame Display service
:::

::: {.section}
### [Outboxes]{#symbol-PyGameApp.Outboxes}

-   **outbox** : NOT USED
-   **signal** : NOT USED
-   **displaysignal** : Requests to Pygame Display service
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
#### [\_\_init\_\_(self, screensize\[, caption\]\[, fullscreen\]\[, depth\]\[, transparency\]\[, position\])]{#symbol-PyGameApp.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [\_dispatch(self)]{#symbol-PyGameApp._dispatch}

Internal pygame event dispatcher.

For all events received, it calls all event handlers in sequence until
one returns True.
:::

::: {.section}
#### [addHandler(self, eventtype, handler)]{#symbol-PyGameApp.addHandler}

Add an event handler, for a given PyGame event type.

The handler is passed the pygame event object as its argument when
called.
:::

::: {.section}
#### [events(self)]{#symbol-PyGameApp.events}

Generator. Receive events on \"events\" inbox and yield then one at a
time.
:::

::: {.section}
#### [go(self)]{#symbol-PyGameApp.go}

Call this to run the pygame app, without using an
[Axon](/Docs/Axon/Axon.html){.reference} scheduler.

Returns when the app \'quits\'
:::

::: {.section}
#### [initialiseComponent(self)]{#symbol-PyGameApp.initialiseComponent}
:::

::: {.section}
#### [main(self)]{#symbol-PyGameApp.main}

Main loop. Do not override
:::

::: {.section}
#### [mainLoop(self)]{#symbol-PyGameApp.mainLoop}

Implement your runtime loop in this method here. FIXME: This is less
than ideal.
:::

::: {.section}
#### [quit(self\[, event\])]{#symbol-PyGameApp.quit}

Call this method/event handler to finish
:::

::: {.section}
#### [removeHandler(self, eventtype, handler)]{#symbol-PyGameApp.removeHandler}

Remove the specified pygame event handler from the specified event.
:::

::: {.section}
#### [waitBox(self, boxname)]{#symbol-PyGameApp.waitBox}

Generator. Yields until data ready on the named inbox.
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
