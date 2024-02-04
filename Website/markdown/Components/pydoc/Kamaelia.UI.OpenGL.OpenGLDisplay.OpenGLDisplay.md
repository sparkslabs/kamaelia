---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.OpenGLDisplay.OpenGLDisplay
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[OpenGLDisplay](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLDisplay.html){.reference}.[OpenGLDisplay](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLDisplay.OpenGLDisplay.html){.reference}
====================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLDisplay.html){.reference}

------------------------------------------------------------------------

::: {.section}
class OpenGLDisplay([Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}) {#symbol-OpenGLDisplay}
---------------------------------------------------------------------------------------------------------------------------------------------------------

OpenGLDisplay(\...) -\> new OpenGLDisplay component

Use OpenGLDisplay.getDisplayService(\...) in preference as it returns an
existing instance, or automatically creates a new one.

Or create your own and register it with setDisplayService(\...)

Keyword arguments (all optional):

-   title \-- caption of window
    (default=http://kamaelia.sourceforge.net)

-   width \-- pixels width (default=800)

-   height \-- pixels height (default=600)

-   background\_colour \-- (r,g,b) background colour
    (default=(255,255,255))

-   fullscreen \-- set to True to start up fullscreen, not windowed
    (default=False)

-   show\_fps \-- show frames per second in window title (default=True)

-   

    limit\_fps \-- maximum frame rate (default=60)

    :   Projection parameters

-   near \-- distance to near plane (default=1.0)

-   far \-- distance to far plane (default=100.0)

-   

    perspective \-- perspective angle (default=45.0)

    :   Viewer position and orientation

-   viewerposition \-- position of viewer (default=(0,0,0))

-   lookat \-- look at point (default= (0,0,-self.farPlaneDist))

-   

    up \-- up vector (default(0,1,0))

    :   Fog

-   fog \-- tuple of fog distances (start, end). if not set, fog is
    disabled (default)

-   fog\_colour \-- (r,g,b) fog colour (default=(255,255,255) )

-   

    fog\_density \-- fog density (default=0.35)

    :   Event processing

-   hitall \-- boolean, if false, only the nearest object under the
    cursor gets activated (default=False)

::: {.section}
### [Inboxes]{#symbol-OpenGLDisplay.Inboxes}

-   **control** : NOT USED
-   **events** : For reception of pygame events
-   **inbox** : Default inbox, not currently used
-   **notify** : For reception of requests for surfaces, overlays and
    events
:::

::: {.section}
### [Outboxes]{#symbol-OpenGLDisplay.Outboxes}

-   **outbox** : NOT USED
-   **signal** : NOT USED
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-OpenGLDisplay.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [calcPow2Size(self, size)]{#symbol-OpenGLDisplay.calcPow2Size}

Calculates the power of 2 dimensions for a given size.
:::

::: {.section}
#### [doPicking(self, pos)]{#symbol-OpenGLDisplay.doPicking}

Uses OpenGL picking to determine objects that have been hit by mouse
pointer. see e.g. OpenGL Redbook
:::

::: {.section}
#### [drawOpenGLComponents(self)]{#symbol-OpenGLDisplay.drawOpenGLComponents}

Draws all registered OpenGL components with their set transformation
matrix.
:::

::: {.section}
#### [drawPygameSurfaces(self)]{#symbol-OpenGLDisplay.drawPygameSurfaces}

Draws all surfaces of registered pygame components on top of everything
else.
:::

::: {.section}
#### [genIdentifier(self)]{#symbol-OpenGLDisplay.genIdentifier}

Returns a unique number.
:::

::: {.section}
#### [handleEvents(self)]{#symbol-OpenGLDisplay.handleEvents}

Handles pygame input events.
:::

::: {.section}
#### [handleOGLComponentEvents(self, events)]{#symbol-OpenGLDisplay.handleOGLComponentEvents}

Prepare and send input events for OpenGL components.
:::

::: {.section}
#### [handlePygameComponentEvents(self, events)]{#symbol-OpenGLDisplay.handlePygameComponentEvents}

Prepare and send input events for pygame components.
:::

::: {.section}
#### [handleRequest\_DISPLAYREQUEST(self, message)]{#symbol-OpenGLDisplay.handleRequest_DISPLAYREQUEST}
:::

::: {.section}
#### [handleRequest\_EVENTSPYREQUEST(self, message)]{#symbol-OpenGLDisplay.handleRequest_EVENTSPYREQUEST}
:::

::: {.section}
#### [handleRequest\_OGL\_DISPLAYREQUEST(self, message)]{#symbol-OpenGLDisplay.handleRequest_OGL_DISPLAYREQUEST}
:::

::: {.section}
#### [handleRequest\_WRAPPERREQUEST(self, message)]{#symbol-OpenGLDisplay.handleRequest_WRAPPERREQUEST}
:::

::: {.section}
#### [handleRequests(self)]{#symbol-OpenGLDisplay.handleRequests}

Handles service requests.
:::

::: {.section}
#### [main(self)]{#symbol-OpenGLDisplay.main}

Main loop.
:::

::: {.section}
#### [setProjection(self)]{#symbol-OpenGLDisplay.setProjection}

Sets projection matrix.
:::

::: {.section}
#### [surfacePosition(self, surface)]{#symbol-OpenGLDisplay.surfacePosition}

Returns a suggested position for a surface. No guarantees its any good!
:::

::: {.section}
#### [updateDisplay(self)]{#symbol-OpenGLDisplay.updateDisplay}

Draws all components, updates screen, clears the backbuffer and
depthbuffer .
:::

::: {.section}
#### [updatePygameTexture(self, surface, pow2surface, texname)]{#symbol-OpenGLDisplay.updatePygameTexture}

Converts the surface of a pygame component to an OpenGL texture.
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
