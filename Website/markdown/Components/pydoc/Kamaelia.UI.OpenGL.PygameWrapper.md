---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.PygameWrapper
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[PygameWrapper](/Components/pydoc/Kamaelia.UI.OpenGL.PygameWrapper.html){.reference}
=================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [PygameWrapper](/Components/pydoc/Kamaelia.UI.OpenGL.PygameWrapper.PygameWrapper.html){.reference}**
:::

-   [Wrapper for pygame components](#345){.reference}
    -   [Example Usage](#346){.reference}
    -   [How does it work?](#347){.reference}
:::

::: {.section}
Wrapper for pygame components {#345}
=============================

A wrapper for two dimensional pygame components that allows to display
them on a Plane in 3D using OpenGL.

This component is a subclass of OpenGLComponent and therefore uses the
OpenGL display service.

::: {.section}
[Example Usage]{#example-usage} {#346}
-------------------------------

The following example shows a wrapped Ticker and MagnaDoodle component:

``` {.literal-block}
# override pygame display service
ogl_display = OpenGLDisplay.getDisplayService()
PygameDisplay.setDisplayService(ogl_display[0])

TICKER = Ticker(size = (150, 150)).activate()
TICKER_WRAPPER = PygameWrapper(wrap=TICKER, position=(4, 1,-10), rotation=(-20,15,3)).activate()
MAGNADOODLE = MagnaDoodle(size=(200,200)).activate()
MAGNADOODLEWRAPPER = PygameWrapper(wrap=MAGNADOODLE, position=(-2, -2,-10), rotation=(20,10,0)).activate()
READER = ConsoleReader().activate()

READER.link( (READER,"outbox"), (TICKER, "inbox") )

Axon.Scheduler.scheduler.run.runThreads()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#347}
--------------------------------------

This component is a subclass of OpenGLComponent. It overrides
\_\_init\_\_(), setup(), draw(), handleEvents() and frame().

In setup() first the needed additional mailboxes are created. These are
the \"eventrequest\" and \"wrapcallback\" inboxes and the
\"wrapped\_events\" outbox:

-   \"eventrequest\" is used for the reception of ADDLISTENEVENT and
    REMOVELISTENEVENT requests of the wrapped component.
-   \"wrapcallback\" is used to receive the response from the display
    service.
-   \"wrapped\_events\" is where the input events get sent to.

Additionally, a WRAPPERREQUEST is sent to the OpenGL display service. It
contains the objectid of the wrapped component as well as the comms for
callback and eventrequests.

In frame(), it is waited for the response on the WRAPPERREQUEST. The
response should contain the OpenGL texture name, the texture size and
the size of the wrapped component. The wanted events are stored and the
\"wrapped\_events\" outbox is linked to the wrapped components
\"events\" inbox. If the size of the wrapper is not set, it is
calculated using the wrapped component pixel size multiplied by the
pixelscaling factor.

To handle event requests by the wrapped component, the method
handleEventRequests() gets called.

In handleEvents() received mouse events get translated into the 2d space
of the wrapped component and sent to it if requested. This is done by
using ray/polygon intersection to determine the point of intersection in
3d. The 2d coordinates are then calculated by using the dot product
between the point of intersection relative to the top left corner and
the edge vectors.

In draw() a cuboid gets drawn with the texture of the pygame component
on its front plane. If the z component of the size is set to zero, only
the front plane is drawn.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[PygameWrapper](/Components/pydoc/Kamaelia.UI.OpenGL.PygameWrapper.html){.reference}.[PygameWrapper](/Components/pydoc/Kamaelia.UI.OpenGL.PygameWrapper.PygameWrapper.html){.reference}
====================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class PygameWrapper(OpenGLComponent) {#symbol-PygameWrapper}
------------------------------------

PygameWrapper(\...) -\> A new PygameWrapper component.

A wrapper for two dimensional pygame components that allows to display
them on a Plane in 3D using OpenGL.

Keyword arguments:

-   wrap \-- Pygame component to wrap
-   pixelscaling \-- Factor to convert pixels to units in 3d, ignored if
    size is specified (default=100)
-   sidecolour \-- Colour of side and back planes
    (default=(200,200,244))
-   thickness \-- Thickness of wrapper, ignored if size is specified
    (default=0.3)

::: {.section}
### [Inboxes]{#symbol-PygameWrapper.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-PygameWrapper.Outboxes}
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-PygameWrapper.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [draw(self)]{#symbol-PygameWrapper.draw}

Draw cuboid.
:::

::: {.section}
#### [frame(self)]{#symbol-PygameWrapper.frame}
:::

::: {.section}
#### [handleEventRequests(self)]{#symbol-PygameWrapper.handleEventRequests}
:::

::: {.section}
#### [handleEvents(self)]{#symbol-PygameWrapper.handleEvents}
:::

::: {.section}
#### [setup(self)]{#symbol-PygameWrapper.setup}
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
