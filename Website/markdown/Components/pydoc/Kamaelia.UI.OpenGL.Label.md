---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.Label
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[Label](/Components/pydoc/Kamaelia.UI.OpenGL.Label.html){.reference}
=================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Label](/Components/pydoc/Kamaelia.UI.OpenGL.Label.Label.html){.reference}**
:::

-   [OpenGL Label Widget](#342){.reference}
    -   [Example Usage](#343){.reference}
    -   [How does it work?](#344){.reference}
:::

::: {.section}
OpenGL Label Widget {#342}
===================

A Label widget for the OpenGL display service.

This component is a subclass of OpenGLComponent and therefore uses the
OpenGL display service.

::: {.section}
[Example Usage]{#example-usage} {#343}
-------------------------------

4 Labels with various sizes, colours, captions and positions:

``` {.literal-block}
Graphline(
    Label1 = Label(caption="That", size=(2,2,1), sidecolour=(0,200,0), position=(-3,0,-10)),
    Label2 = Label(caption="Boy", bgcolour=(200,100,0), position=(3,0,-10)),
    Label3 = Label(caption="Needs", margin=15, position=(-1,0,-10), rotation=(30,0,10)),
    Label4 = Label(caption="Therapy!", fontsize=20, size=(0.3,0.3,1), position=(1,0,-10)),
    ECHO = ConsoleEchoer(),
    linkages = {
        ("Label1", "outbox") : ("ECHO", "inbox"),
        ("Label2", "outbox") : ("ECHO", "inbox"),
        ("Label3", "outbox") : ("ECHO", "inbox"),
        ("Label4", "outbox") : ("ECHO", "inbox"),
    }
).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#344}
--------------------------------------

This component is a subclass of OpenGLComponent. It overrides
\_\_init\_\_(), setup(), draw(), handleEvents() and frame().

In setup() only buildCaption() gets called where the set caption is
rendered on a pygame surface. This surface is then set as OpenGL
texture.

In draw() a flat cuboid is drawn (if size is not specified) with the
caption texture on both the front and the back surface.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[Label](/Components/pydoc/Kamaelia.UI.OpenGL.Label.html){.reference}.[Label](/Components/pydoc/Kamaelia.UI.OpenGL.Label.Label.html){.reference}
============================================================================================================================================================================================================================================================================================================================

::: {.section}
class Label(OpenGLComponent) {#symbol-Label}
----------------------------

Label(\...) -\> A new Label component.

A Label widget for the OpenGL display service.

Keyword arguments:

-   caption \-- Label caption (default=\"Label\")
-   bgcolour \-- Colour of surfaces behind caption
    (default=(200,200,200))
-   fgcolour \-- Colour of the caption text (default=(0,0,0)
-   sidecolour \-- Colour of side planes (default=(200,200,244))
-   margin \-- Margin size in pixels (default=8)
-   fontsize \-- Font size for caption text (default=50)
-   pixelscaling \-- Factor to convert pixels to units in 3d, ignored if
    size is specified (default=100)
-   thickness \-- Thickness of Label widget, ignored if size is
    specified (default=0.3)

::: {.section}
### [Inboxes]{#symbol-Label.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-Label.Outboxes}
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-Label.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [buildCaption(self)]{#symbol-Label.buildCaption}

Pre-render the text to go on the label.
:::

::: {.section}
#### [draw(self)]{#symbol-Label.draw}

Draw label cuboid.
:::

::: {.section}
#### [setup(self)]{#symbol-Label.setup}

Build caption.
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
