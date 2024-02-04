---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.Button.Button
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[Button](/Components/pydoc/Kamaelia.UI.OpenGL.Button.html){.reference}.[Button](/Components/pydoc/Kamaelia.UI.OpenGL.Button.Button.html){.reference}
=================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.UI.OpenGL.Button.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Button([Kamaelia.UI.OpenGL.OpenGLComponent.OpenGLComponent](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.OpenGLComponent.html){.reference}) {#symbol-Button}
---------------------------------------------------------------------------------------------------------------------------------------------------------

Button(\...) -\> A new Button component.

A button widget for the OpenGL display service. Sends a message when
clicked or an assigned key is pressed.

Keyword arguments:

-   caption \-- Button caption (default=\"Button\")
-   bgcolour \-- Colour of surfaces behind caption
    (default=(244,244,244))
-   fgcolour \-- Colour of the caption text (default=(0,0,0)
-   sidecolour \-- Colour of side planes (default=(200,200,244))
-   margin \-- Margin size in pixels (default=8)
-   key \-- Key to activate button (default=None)
-   fontsize \-- Font size for caption text (default=50)
-   pixelscaling \-- Factor to convert pixels to units in 3d, ignored if
    size is specified (default=100)
-   thickness \-- Thickness of button widget, ignored if size is
    specified (default=0.3)
-   msg \-- Message which gets sent when button is activated
    (default=\"CLICK\")

::: {.section}
### [Inboxes]{#symbol-Button.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-Button.Outboxes}
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-Button.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [activationMovement(self)]{#symbol-Button.activationMovement}

Rotate button stepwise by 360 degrees when it has been activated.
:::

::: {.section}
#### [buildCaption(self)]{#symbol-Button.buildCaption}

Pre-render the text to go on the label.
:::

::: {.section}
#### [draw(self)]{#symbol-Button.draw}

Draw button cuboid.
:::

::: {.section}
#### [frame(self)]{#symbol-Button.frame}

Rotate button if it has been activated.
:::

::: {.section}
#### [handleEvents(self)]{#symbol-Button.handleEvents}

Handle events.
:::

::: {.section}
#### [setup(self)]{#symbol-Button.setup}

Build caption and request reception of events.
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
