---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.SimpleButton
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[SimpleButton](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleButton.html){.reference}
===============================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [SimpleButton](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleButton.SimpleButton.html){.reference}**
:::

-   [Simple Button component](#339){.reference}
    -   [Example Usage](#340){.reference}
    -   [How does it work?](#341){.reference}
:::

::: {.section}
Simple Button component {#339}
=======================

A simple cuboid shaped button without caption. Implements responsive
button behavoir.

Could be used to subclass differently shaped buttons from. The colours
of the front/back and the side faces can be specified.

::: {.section}
[Example Usage]{#example-usage} {#340}
-------------------------------

Two simple buttons which send messages to the console:

``` {.literal-block}
Graphline(
    button1 = SimpleButton(size=(1,1,0.3), position=(-2,0,-10), msg="PINKY"),
    button2 = SimpleButton(size=(2,2,1), position=(5,0,-15), msg="BRAIN"),
    echo = ConsoleEchoer(),
    linkages = {
        ("button1", "outbox") : ("echo", "inbox"),
        ("button2", "outbox") : ("echo", "inbox")
    }
).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#341}
--------------------------------------

This component is a subclass of OpenGLComponent (for OpenGLComponent
functionality see its documentation). It overrides \_\_init\_\_(),
setup(), draw() and handleEvents().

It draws a simple cuboid. It is activated on mouse button release over
the object and on key down if a key is assigned. On mouse button down it
is shrunk by a small amount until the button is released.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[SimpleButton](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleButton.html){.reference}.[SimpleButton](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleButton.SimpleButton.html){.reference}
===============================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class SimpleButton([Kamaelia.UI.OpenGL.OpenGLComponent.OpenGLComponent](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.OpenGLComponent.html){.reference}) {#symbol-SimpleButton}
---------------------------------------------------------------------------------------------------------------------------------------------------------------

SimpleButton(\...) -\> A new SimpleButton component.

A simple cuboid shaped button without caption. Implements responsive
button behavoir.

Keyword arguments:

-   bgcolour \-- Background colour (default=(244,244,244))
-   sidecolour \-- Colour of side planes (default=(200,200,244))
-   key \-- Activation key, pygame identifier (optional)
-   msg \-- Message that gets sent to the outbox when the button is
    activated (default=\"CLICK\")

::: {.section}
### [Inboxes]{#symbol-SimpleButton.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-SimpleButton.Outboxes}
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-SimpleButton.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [draw(self)]{#symbol-SimpleButton.draw}
:::

::: {.section}
#### [handleEvents(self)]{#symbol-SimpleButton.handleEvents}
:::

::: {.section}
#### [setup(self)]{#symbol-SimpleButton.setup}
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from [Kamaelia.UI.OpenGL.OpenGLComponent.OpenGLComponent](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.OpenGLComponent.html){.reference} :

-   [redraw](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.html#symbol-OpenGLComponent.redraw){.reference}(self)
-   [handleMovement](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.html#symbol-OpenGLComponent.handleMovement){.reference}(self)
-   [removeListenEvents](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.html#symbol-OpenGLComponent.removeListenEvents){.reference}(self,
    events)
-   [addListenEvents](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.html#symbol-OpenGLComponent.addListenEvents){.reference}(self,
    events)
-   [main](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.html#symbol-OpenGLComponent.main){.reference}(self)
-   [applyTransforms](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.html#symbol-OpenGLComponent.applyTransforms){.reference}(self)
-   [frame](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.html#symbol-OpenGLComponent.frame){.reference}(self)
:::
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
