---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[OpenGLComponent](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.html){.reference}
=====================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [OpenGLComponent](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.OpenGLComponent.html){.reference}**
:::

-   [General OpenGL component](#330){.reference}
    -   [Example Usage](#331){.reference}
    -   [How does it work?](#332){.reference}
:::

::: {.section}
General OpenGL component {#330}
========================

This components implements the interaction with the OpenGLDisplay
service that is needed to setup, draw and move an object using OpenGL.

It is recommended to use it as base class for new 3D components. It
provides methods to be overridden for adding functionality.

::: {.section}
[Example Usage]{#example-usage} {#331}
-------------------------------

One of the simplest possible reasonable component would like something
like this:

``` {.literal-block}
class Point(OpenGLComponent):
    def draw(self):
        glBegin(GL_POINTS)
        glColor(1,0,0)
        glVertex(0,0,0)
        glEnd()
```

A more complex component that changes colour in response to messages
sent to its \"colour\" inbox and reacts to mouse clicks by rotationg
slightly:

``` {.literal-block}
class ChangingColourQuad(OpenGLComponent):
    def setup(self):
        self.colour = (0.5,1.0,0.5)
        self.addInbox("colour")
        self.addListenEvents([pygame.MOUSEBUTTONDOWN])

    def draw(self):
        glBegin(GL_QUADS)
        glColor(*self.colour)
        glVertex(-1, 1, 0)
        glVertex(1, 1, 0)
        glVertex(1, -1, 0)
        glVertex(-1, -1, 0)
        glEnd()

    def handleEvents(self):
        while self.dataReady("events"):
            event = self.recv("events")
            if event.type == pygame.MOUSEBUTTONDOWN and self.identifier in event.hitobjects:
                self.rotation += Vector(0,0,10)
                self.rotation %= 360

    def frame(self):
        while self.dataReady("colour"):
            self.colour = self.recv("colour")
            self.redraw()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#332}
--------------------------------------

OpenGLComponent provides functionality to display and move objects in
OpenGL as well as to process events. The component registers at the
OpenGL display service, draws its contens to a displaylist and applies
its transformations to a Transform object. The display list id and the
Transform objects are continuosly transfered to the display service when
updated.

For movement several inboxes are provided. The messages sent to these
boxes are collected and applied automatically. The inboxes and expected
messages are:

-   position \-- position triples (x,y,z)
-   rotation \-- rotation triples (x,y,z)
-   scaling \-- scaling triples (x,y,z)
-   rel\_position \-- relative position triples (x,y,z)
-   rel\_rotation \-- relative rotation triples (x,y,z)
-   rel\_scaling \-- relative scaling triples (x,y,z)

When an OpenGLComponent gets moved, it also provides feedback about its
movement. This feedback is sent to the following outboxes:

-   position \-- position triples (x,y,z)
-   rotation \-- rotation triples (x,y,z)
-   scaling \-- scaling triples (x,y,z)

OpenGLComponent is designed to get subclassed by opengl components.
Using it as base class has the advantage not having to worry about
interaction with the OpenGl display service. To add functionality, the
following methods are provided to be overridden:

-   setup() \-- set up the component
-   draw() \-- draw content using OpenGL
-   handleEvents() \-- handle input events (\"events\" inbox)
-   frame() \-- called every frame, to add additional functionality

Stubs method are provided, so missing these out does not result in
broken code. The methods get called from the main method, the following
code shows in which order:

``` {.literal-block}
def main(self):
    # create and send display request
    ...
    # setup function from derived objects
    self.setup()
    ...
    # inital apply trasformations
    self.applyTransforms() # generates and sends a Transform object
    # initial draw to display list
    self.redraw() # calls draw and saves it to a displaylist

    ...
    while 1:
        yield 1
        self.applyTransforms()
        self.handleMovement()
        # handle events function from derived objects
        self.handleEvents()
        # frame function from derived objects
        self.frame()
```

As can be seen here, there is no invocation of draw in the main loop. It
is only called once to generate a displaylist which then gets send to
the display service. This is the normal situation with static 3D
objects. If you want to create a dynamic object, e.g. which changes e.g.
its geometry or colour (see second example above), you need to call the
redraw() method whenever changes happen.

If you need to override the \_\_init\_\_() method, e.g. to get
initialisation parameters, make sure to pass on all keyword arguments to
\_\_init\_\_(\...) of the superclass, e.g.:

``` {.literal-block}
def __init__(self, **argd):
    super(ClassName, self).__init__(**argd)
    # get an initialisation parameter
    myparam = argd.get("myparam", defaultvalue)
```

The following methods are provided to be used by inherited objects:

-   redraw() \-- Call draw() and save its actions to a displaylist. Send
    it as update request to the display service. *Don\'t call this
    method from within draw()!*
-   addListenEvents(list of events) \-- Request reception of a list of
    events
-   removeListenEvents(list of events) \-- Stop reveiving events

The are inteded to simplify component handling. For detailed description
see their documentation.

Every OpenGLComponent has its own pygame Clock object. It is used to
measure the time between frames. The value gets stored in self.frametime
in seconds and can be used by derived components to make movement time-
based rather than frame-based. For example to rotate 3 degrees per
second you would do something like:

``` {.literal-block}
self.rotation.y += 3.0*self.frametime
```

OpenGLComponent components terminate if a producerFinished or
shutdownMicroprocess message is received on their \"control\" inbox. The
received message is also forwarded to the \"signal\" outbox. Upon
termination, this component does *not* unbind itself from the
OpenGLDisplay service and does not free any requested resources.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[OpenGLComponent](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.html){.reference}.[OpenGLComponent](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.OpenGLComponent.html){.reference}
==============================================================================================================================================================================================================================================================================================================================================================================

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
