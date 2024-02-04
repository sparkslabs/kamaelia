---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.OpenGLDisplay
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[OpenGLDisplay](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLDisplay.html){.reference}
=================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [OpenGLDisplay](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLDisplay.OpenGLDisplay.html){.reference}**
:::

-   [OpenGL Display Service](#309){.reference}
    -   [Example Usage](#310){.reference}
    -   [How does it work?](#311){.reference}
        -   [OpenGL components](#312){.reference}
        -   [Pygame components](#313){.reference}
        -   [Pygame wrappers](#314){.reference}
        -   [Listening to events](#315){.reference}
        -   [Eventspies](#316){.reference}
        -   [Shutdown](#317){.reference}
:::

::: {.section}
OpenGL Display Service {#309}
======================

This component provides an OpenGL window and manages input events,
positioning and drawing of other components. It handles both OpenGL and
Pygame components.

OpenGLDisplay is a service that registers with the Coordinating
Assistant Tracker (CAT).

::: {.section}
[Example Usage]{#example-usage} {#310}
-------------------------------

If you want to change some of the default parameters, like the viewport,
you first have to create an OpenGLDisplay object and then register it.
The following would show a simple cube from a slightly changed viewer
position:

``` {.literal-block}
display = OpenGLDisplay(viewerposition=(0,-10,0), lookat=(0,0,-15)).activate()
OpenGLDisplay.setDisplayService(display)

SimpleCube(position=(0,0,-15)).activate()
```

If you want to use pygame components, you have to override the
PygameDisplay service before creating any pygame components:

``` {.literal-block}
display = OpenGLDisplay.getDisplayService()
PygameDisplay.setDisplayService(display[0])
```

For examples of how components have to interfrere with OpenGLDisplay,
please have a look at OpenGLComponent.py and Interactor.py.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#311}
--------------------------------------

OpenGLDisplay is a service. obtain it by calling the
OpenGLDisplay.getDisplayService(\...) static method. Any existing
instance will be returned, otherwise a new one is automatically created.

Alternatively, if you wish to configure OpenGLDisplay with options other
than the defaults, create your own instance, then register it as a
service by calling the PygameDisplay.setDisplayService(\...) static
method. NOTE that it is only advisable to do this at the top level of
your system, as other components may have already requested and created
a OpenGLDisplay component!

When using only OpenGL components and no special display settings have
to be made, you won\'t see OpenGLDisplay as it is registered
automatically when it is first requested (by invoking the
getDisplayService(\...) static method).

You can also use an instance of OpenGLDisplay to override the
PygameDisplay service as it implements most of the functionality of
PygameDisplay. You will want to do this when you want to use Pygame
components along with OpenGL components.

pygame only supports one display window at a time, you must not make
more than one OpenGLDisplay component.

OpenGLDisplay listens for requests arriving at its \"notify\" inbox. A
request can currently be to:

-   register an OpenGL component (OGL\_DISPLAYREQUEST)
-   register a pygame component (DISPLAYREQUEST)
-   register a pygame wrapper (WRAPPERREQUEST)
-   register an eventspy (EVENTSPYREQUEST)
-   listen or stop listening to events (ADDLISTENEVENT,
    REMOVELISTENEVENT)
-   update the displaylist of an OpenGL component (UPDATE\_DISPLAYLIST)
-   update the transform of an OpenGL component (UPDATE\_TRANSFORM)
-   invoke a redraw of a pygame surface (REDRAW)

::: {.section}
### [OpenGL components]{#opengl-components} {#312}

OpenGL components get registered by an OGL\_DISPLAYREQUEST. Such a
request is a dictionary with the following keys:

``` {.literal-block}
{
    "OGL_DISPLAYREQUEST": True,     # OpenGL Display request
    "objectid" : id(object),            # id of requesting object (for identification)
    "callback" : (component,"inboxname"),   # to send the generated event id to

    "events" : (component, "inboxname"),    # to send event notification (optional)
    "size": (x,y,z),                # size of object (not yet used)
}
```

When OpenGLDisplay received such a request it generates an identifier
and returns it to the box you specify by \"callback\". This identifier
can later be used to determine if a mouse event \"hit\" the object.

It is important to note that OpenGL don\'t draw and transform themselves
directly but only hand displaylists and Transform objects to the display
service. After an OpenGL component has been registered, it can send
displaylist- and transform-updates. These requests are dictionaries of
the following form:

``` {.literal-block}
{
    "DISPLAYLIST_UPDATE": True, # update displaylist
    "objectid": id(object),     # id of requesting object
    "displaylist": displaylist  # new displaylist
}
```

If an object is static, i.e. does not change its geometry, it only needs
to send this update one time. Dynamic objects can provide new
displaylists as often as they need to.:

``` {.literal-block}
{
    "TRANSFORM_UPDATE": True,   # update transform
    "objectid": id(self),       # id of requesting object
    "transform": self.transform # new transform
}
```

A transform update should be sent every time the object transform
changes, i.e. it is moved.

OpenGL components can also request listening to events. See \"Listening
to events\" below.

It is generally recommended to use the class OpenGLComponent as base
class for OpenGL components. It implements all the functionality
required to create, draw, move OpenGL components and to handle events
(see OpenGLComponent.py for the class and e.g. SimpleCube.py, Button.py
and other components for examples).
:::

::: {.section}
### [Pygame components]{#pygame-components} {#313}

OpenGLDisplay is designed to be compatible with PygameDisplay. After
overriding the PygameDisplay service, pygame components can be created
as usual. See the documentation of PygameDisplay
(Kamaelia/UI/PygameDisplay.py) for how to do this.

NOTE: Overlays are not supported yet.
:::

::: {.section}
### [Pygame wrappers]{#pygame-wrappers} {#314}

It is possibly, by sending a WRAPPERREQUEST, to wrap an already
registered pygame component by a OpenGL component. The surface of the
pygame component is then excluded from normal drawing and this
responsibility is handed to the requesting component by giving it the
texture name corresponding to the surface. The event processing of mouse
events is then also relinked to be done by the wrapper.

The wrapper request is a dictionary with the following keys:

``` {.literal-block}
{
    "WRAPPERREQUEST" : True,                    # wrap a pygame component
    "wrapcallback" : (object, "inboxname"),     # send response here
    "eventrequests" : (object, "inboxname"),    # to receive event requests by the wrapped component
    "wrap_objectid": id(wrapped_component)      # object id of the component to be wrapped
}
```

When a WRAPPERREQUEST is received for a component which is not
registered yet, it is stored until the component to be wrapped gets
registered.

When a wrapper request was received, the OpenGL display service returns
a dictionary to the box specified by \"wrapcallback\" containing the
following keys:

``` {.literal-block}
{
    "texname": texname,             # OpenGL texture name
    "texsize": (width, height),     # texture coordinate size
    "size": (width, height)         # size of pygame surface in pixels
}
```

See PygameWrapperPlane.py for an example implementation of a wrapper.
:::

::: {.section}
### [Listening to events]{#listening-to-events} {#315}

Once your component has been registered, it can request to be notified
of specific pygame events. The same requests are used for Pygame and
OpenGL components, only the keys are slightly different.

To request to listen to a given event, send a dictionary to the
\"notify\" inbox, containing the following:

``` {.literal-block}
{
    "ADDLISTENEVENT" : pygame_eventtype,    # example: pygame.KEYDOWN
    "surface" : your_surface,               # for pygame components
    "objectid" : id(object),                # for OpenGL components
}
```

To unsubscribe from a given event, send a dictionary containing:

``` {.literal-block}
{
    "REMOVELISTENEVENT" : pygame_eventtype,
    "surface" : your_surface,               # for pygame components
    "objectid" : id(object),                # for OpenGL components
}
```

Events will be sent to the inbox specified in the \"events\" key of the
\"DISPLAYREQUEST\" or \"OGL\_DISPLAYREQUEST\" message. They arrive as a
list of pygame event objects.

The events objects of type Bunch with the following variables:

-   type \-- Pygame event type

> For events of type pygame.KEYDOWN, pygame.KEYUP:

-   key \-- Pressed or released key

> For events of type pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP:

-   pos \-- Mouse position
-   button \-- Pressed or released mouse button number

> For events of type pygame.MOUSEMOTION:

-   rel \-- Relative mouse motion.
-   buttons \-- Buttons pressed while mousemotion

> For events of type pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP,
> pygame.MOUSEMOTION when sent to OpenGL components:

-   viewerposition \-- Position of viewer
-   dir \-- Direction vector of generated from mouse position
-   hitobjects \-- List of hit objects

NOTE: If the event is MOUSEMOTION, MOUSEBUTTONUP or MOUSEBUTTONDOWN then
you will instead receive a replacement object, with the same attributes
as the pygame event. But for pygame components, the \'pos\' attribute
adjusted so that (0,0) is the top left corner of *your* surface. For
OpenGL components the origin and direction of the intersection vector
determined using the mouse position and viewport will be added as well
as a list of identfiers of objects that has been hit.

If a component has requested reception of an event type, it gets every
event that happens of that type, regardless if it is of any concern to
the component. In the case of mouse events there is a list of hit
objects included which are determined by using OpenGL picking.
:::

::: {.section}
### [Eventspies]{#eventspies} {#316}

Eventspies are components that basically listen to events for other
components. They are registered by sending an EVENSPYREQUEST:

``` {.literal-block}
{
    "EVENTSPYREQUEST" : True,
    "objectid" : id(object),            # id of requesting object
    "target": id(target),               # id of object to be spied
    "callback" : (object,"inboxname"),  # for sending event identifier
    "events" : (object, "inboxname")    # for reception of events
}
```

In return you get the identifier of the target component that can be
used to determine if the target component has been hit. An evenspy can
request reception of event types like usual (using ADDLISTENEVENT and
REMOVELISTENEVENT). When events are spied this does not affect normal
event processing.
:::

::: {.section}
### [Shutdown]{#shutdown} {#317}

Upon reception of a pygame.QUIT event, OpenGLDisplay sends an
[Axon.Ipc.shutdownMicroprocess](/Docs/Axon/Axon.Ipc.shutdownMicroprocess.html){.reference}
object out of its signal outbox. The service itself does not terminate.
:::
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[OpenGLDisplay](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLDisplay.html){.reference}.[OpenGLDisplay](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLDisplay.OpenGLDisplay.html){.reference}
====================================================================================================================================================================================================================================================================================================================================================================

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
