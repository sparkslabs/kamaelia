---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.OpenGLComponent
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[OpenGLComponent](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.html){.reference}.[OpenGLComponent](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.OpenGLComponent.html){.reference}
==============================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.html){.reference}

------------------------------------------------------------------------

::: {.section}
class OpenGLComponent([Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}) {#symbol-OpenGLComponent}
-----------------------------------------------------------------------------------------------------------------------------------------------------------

OpenGLComponent(\...) -\> create a new OpenGL component (not very useful
though; it is rather designed to inherit from).

This components implements the interaction with the OpenGLDisplay
service that is needed to setup, draw and move an object using OpenGL.

Keyword arguments:

-   size \-- three dimensional size of component (default=(0,0,0))
-   rotation \-- rotation of component around (x,y,z) axis
    (defaul=(0,0,0))
-   scaling \-- scaling along the (x,y,z) axis (default=(1,1,1))
-   position \-- three dimensional position (default=(0,0,0))
-   name \-- name of component (mostly for debugging,
    default=\"nameless\")

::: {.section}
### [Inboxes]{#symbol-OpenGLComponent.Inboxes}

-   **control** : For shutdown messages
-   **rel\_position** : receive position triple (x,y,z)
-   **scaling** : receive scaling triple (x,y,z)
-   **callback** : for the response after a displayrequest
-   **inbox** : not used
-   **position** : receive position triple (x,y,z)
-   **rotation** : receive rotation triple (x,y,z)
-   **rel\_scaling** : receive scaling triple (x,y,z)
-   **events** : Input events
-   **rel\_rotation** : receive rotation triple (x,y,z)
:::

::: {.section}
### [Outboxes]{#symbol-OpenGLComponent.Outboxes}

-   **signal** : For shutdown messages
-   **display\_signal** : Outbox used for communicating to the display
    surface
-   **scaling** : send scaling status when updated
-   **position** : send position status when updated
-   **outbox** : not used
-   **rotation** : send rotation status when updated
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-OpenGLComponent.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [addListenEvents(self, events)]{#symbol-OpenGLComponent.addListenEvents}

Sends listening request for pygame events to the display service. The
events parameter is expected to be a list of pygame event constants.
:::

::: {.section}
#### [applyTransforms(self)]{#symbol-OpenGLComponent.applyTransforms}

Use the objects translation/rotation/scaling values to generate a new
transformation Matrix if changes have happened.
:::

::: {.section}
#### [draw(self)]{#symbol-OpenGLComponent.draw}

Method stub

Override this method for drawing. Only use commands which are needed for
drawing. Will not draw directly but be saved to a displaylist.
Therefore, make sure not to use any commands which cannot be stored in
displaylists (unlikely anyway).
:::

::: {.section}
#### [frame(self)]{#symbol-OpenGLComponent.frame}

Method stub

Override this method for operations you want to do every frame. It will
be called every time the component is scheduled. Do not include infinite
loops, the method has to return every time it gets called.
:::

::: {.section}
#### [handleEvents(self)]{#symbol-OpenGLComponent.handleEvents}

Method stub

Override this method to do event handling inside. Should look like this:

``` {.literal-block}
while self.dataReady("events"):
    event = self.recv("events")
    # handle event ...
```
:::

::: {.section}
#### [handleMovement(self)]{#symbol-OpenGLComponent.handleMovement}

Handle movement commands received by corresponding inboxes.
:::

::: {.section}
#### [main(self)]{#symbol-OpenGLComponent.main}
:::

::: {.section}
#### [redraw(self)]{#symbol-OpenGLComponent.redraw}

Invoke draw() and save its commands to a newly generated displaylist.

The displaylist name is then sent to the display service via a
\"DISPLAYLIST\_UPDATE\" request.
:::

::: {.section}
#### [removeListenEvents(self, events)]{#symbol-OpenGLComponent.removeListenEvents}

Sends stop listening request for pygame events to the display service.
The events parameter is expected to be a list of pygame event constants.
:::

::: {.section}
#### [setup(self)]{#symbol-OpenGLComponent.setup}

Method stub

Override this method for component setup. It will be called on the first
scheduling of the component.
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
