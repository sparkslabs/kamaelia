---
pagename: Components/pydoc/Kamaelia.UI.MH.PyGameApp.PyGameApp
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[MH](/Components/pydoc/Kamaelia.UI.MH.html){.reference}.[PyGameApp](/Components/pydoc/Kamaelia.UI.MH.PyGameApp.html){.reference}.[PyGameApp](/Components/pydoc/Kamaelia.UI.MH.PyGameApp.PyGameApp.html){.reference}
================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.UI.MH.PyGameApp.html){.reference}

------------------------------------------------------------------------

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
