---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.Movement
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[Movement](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.html){.reference}
=======================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [PathMover](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.PathMover.html){.reference}**
-   **component
    [SimpleBuzzer](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.SimpleBuzzer.html){.reference}**
-   **component
    [SimpleMover](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.SimpleMover.html){.reference}**
-   **component
    [SimpleRotator](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.SimpleRotator.html){.reference}**
-   **component
    [WheelMover](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.WheelMover.html){.reference}**
:::

-   [A collection of movement components and classes](#324){.reference}
    -   [Example Usage](#325){.reference}
:::

::: {.section}
A collection of movement components and classes {#324}
===============================================

Contained components:

-   PathMover
-   WheelMover
-   SimpleRotator
-   SimpleBuzzer

Contained classes:

-   LinearPath

For a description of these classes have a look at their class
documentation.

::: {.section}
[Example Usage]{#example-usage} {#325}
-------------------------------

The following example show the usage of most of the components in this
file (for an example how to use the WheelMover, see the TorrentOpenGLGUI
example):

``` {.literal-block}
points = [(3,3,-20),
          (4,0,-20),
          (3,-3,-20),
          (0,-4,-20),
          (-3,-3,-20),
          (-4,0,-20),
          (-3,3,-20),
          (0,4,-20),
          (3,3,-20),
         ]
path = LinearPath(points, 1000)

cube1 = SimpleCube(size=(1,1,1)).activate()
pathmover = PathMover(path).activate()
pathmover.link((pathmover,"outbox"), (cube1,"position"))

cube2 = SimpleCube(size=(1,1,1)).activate()
simplemover = SimpleMover().activate()
simplemover.link((simplemover,"outbox"), (cube2,"position"))

cube3 = SimpleCube(size=(1,1,1), position=(-1,0,-15)).activate()
rotator = SimpleRotator().activate()
rotator.link((rotator,"outbox"), (cube3,"rel_rotation"))

cube4 = SimpleCube(size=(1,1,1), position=(1,0,-15)).activate()
buzzer = SimpleBuzzer().activate()
buzzer.link((buzzer,"outbox"), (cube4,"scaling"))

Axon.Scheduler.scheduler.run.runThreads()
```
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[Movement](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.html){.reference}.[PathMover](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.PathMover.html){.reference}
=============================================================================================================================================================================================================================================================================================================================================

::: {.section}
class PathMover([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-PathMover}
-------------------------------------------------------------------------------------------------

PathMover(\...) -\> A new PathMover object.

PathMover can be used to move a 3d object along a path.

It can be controlled by sending commands to its inbox. These commands
can be one of \"Play\", \"Stop\", \"Next\", \"Previous\", \"Rewind\",
\"Forward\" and \"Backward\".

If the pathmover reaches the beginning or the end of a path it generates
a status message which is sent to the \"status\" outbox. This message
can be \"Finish\" or \"Start\".

Keyword arguments:

-   path \-- A path object (e.g. LinearPath) or a list of points
-   repeat \-- Boolean indication if the Pathmover should repeat the
    path if it reaches an end (default=True)

::: {.section}
### [Inboxes]{#symbol-PathMover.Inboxes}

-   **control** : ignored
-   **inbox** : Commands are received here
:::

::: {.section}
### [Outboxes]{#symbol-PathMover.Outboxes}

-   **status** : Used to send status messages
-   **outbox** : Outbox for sending Control3D commands
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
#### [\_\_init\_\_(self, path\[, repeat\])]{#symbol-PathMover.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-PathMover.main}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[Movement](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.html){.reference}.[SimpleBuzzer](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.SimpleBuzzer.html){.reference}
===================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class SimpleBuzzer([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-SimpleBuzzer}
----------------------------------------------------------------------------------------------------

SimpleBuzzer(\...) -\> A new SimpleBuzzer component.

A simple buzzer component mostly for testing. Changes the scaling of
OpenGLComponents it connected to their \"scaling\" boxes.

::: {.section}
### [Inboxes]{#symbol-SimpleBuzzer.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-SimpleBuzzer.Outboxes}
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
#### [main(self)]{#symbol-SimpleBuzzer.main}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[Movement](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.html){.reference}.[SimpleMover](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.SimpleMover.html){.reference}
=================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class SimpleMover([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-SimpleMover}
---------------------------------------------------------------------------------------------------

SimpleMover(\...) -\> A new SimpleMover component.

A simple mover component mostly for testing. Moves OpenGLComponents
between the specified borders if connected to their \"position\" boxes.
The amount of movement every frame and the origin can also be specified.

Keyword arguments:

-   amount \-- amount of movement every frame sent
    (default=(0.03,0.03,0.03))
-   borders \-- borders of every dimension (default=(5,5,5))
-   origin \-- origin of movement (default=(0,0,-20))

::: {.section}
### [Inboxes]{#symbol-SimpleMover.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-SimpleMover.Outboxes}
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
#### [\_\_init\_\_(self\[, amount\]\[, borders\]\[, origin\])]{#symbol-SimpleMover.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-SimpleMover.main}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[Movement](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.html){.reference}.[SimpleRotator](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.SimpleRotator.html){.reference}
=====================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class SimpleRotator([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-SimpleRotator}
-----------------------------------------------------------------------------------------------------

SimpleRotator(\...) -\> A new SimpleRotator component.

A simple rotator component mostly for testing. Rotates OpenGLComponents
by the amount specified if connected to their \"rel\_rotation\" boxes.

Keyword arguments:

-   amount \-- amount of relative rotation sent (default=(0.1,0.1,0.1))

::: {.section}
### [Inboxes]{#symbol-SimpleRotator.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-SimpleRotator.Outboxes}
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
#### [\_\_init\_\_(self\[, amount\])]{#symbol-SimpleRotator.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-SimpleRotator.main}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[Movement](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.html){.reference}.[WheelMover](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.WheelMover.html){.reference}
===============================================================================================================================================================================================================================================================================================================================================

::: {.section}
class WheelMover([Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}) {#symbol-WheelMover}
------------------------------------------------------------------------------------------------------------------------------------------------------

WheelMover(\...) -\> A new WheelMover component.

A component to arrange several OpenGlComponents in the style of a big
wheel rotating around the X axis. Can be used to switch between
components.

Components can be added and removed during operation using the
\"notify\" inbox. Messages sent to it are expected to be a dictionary of
the following form:

``` {.literal-block}
{
    "APPEND_CONTROL" :True,
    "objectid": id(object),
    "control": (object,"position")
}
```

for adding components and:

``` {.literal-block}
{
    "REMOVE_CONTROL" :True,
    "objectid": id(object),
}
```

for removing components.

If components are added when the wheel is already full (number of slots
exhausted) they are simply ignored.

The whole wheel can be controlles by sending messages to the \"switch\"
inbox. The commands can be either \"NEXT\" or \"PREVIOUS\".

Keyword arguments:

-   steps \-- number of steps the wheel is subdivided in (default=400)
-   center \-- center of the wheel (default=(0,0,-13))
-   radius \-- radius of the wheel (default=5)
-   slots \-- number of components which can be handled (default=20)

::: {.section}
### [Inboxes]{#symbol-WheelMover.Inboxes}

-   **control** : ignored
-   **switch** : For reception of switching commands
-   **inbox** : not used
-   **notify** : For appending and removing components
:::

::: {.section}
### [Outboxes]{#symbol-WheelMover.Outboxes}

-   **outbox** : Outbox for sending position updates
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
#### [\_\_init\_\_(self\[, steps\]\[, center\]\[, radius\]\[, slots\])]{#symbol-WheelMover.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-WheelMover.main}
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
