---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.Container
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[Container](/Components/pydoc/Kamaelia.UI.OpenGL.Container.html){.reference}
=========================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Container](/Components/pydoc/Kamaelia.UI.OpenGL.Container.Container.html){.reference}**
:::

-   [Container component](#294){.reference}
    -   [Example Usage](#295){.reference}
    -   [How does it work?](#296){.reference}
:::

::: {.section}
Container component {#294}
===================

A container to control several OpenGLComponents.

::: {.section}
[Example Usage]{#example-usage} {#295}
-------------------------------

In the following example, three components are put into a container and
get moved by a SimpleMover and rotated around the Y axis by a
SimpleRotator:

``` {.literal-block}
o1 = SimpleButton(size=(1,1,1)).activate()
o2 = SimpleCube(size=(1,1,1)).activate()
o3 = ArrowButton(size=(1,1,1)).activate()

containercontents = {
    o1: {"position":(0,1,0)},
    o2: {"position":(1,-1,0)},
    o3: {"position":(-1,-1,0)},
}

Graphline(
    OBJ1=o1,
    OBJ2=o2,
    OBJ3=o3,
    CONTAINER=Container(contents=containercontents, position=(0,0,-10)),
    MOVER=SimpleMover(amount=(0.01,0.02,0.03)),
    ROTATOR=SimpleRotator(amount=(0,0.1,0)),
    linkages = {
        ("MOVER", "outbox") : ("CONTAINER","position"),
        ("ROTATOR", "outbox") : ("CONTAINER","rel_rotation")
    }
).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#296}
--------------------------------------

The Container component provides the same inboxes for absolute and
relative movement as a OpenGLComponent. These are \"position\",
\"rotation\", \"scaling\", \"rel\_position\", \"rel\_rotation\",
\"rel\_scaling\", their names are self explanatory. When the container
receives a tuple in one of those inboxes, it does update its own
transform and uses it to translate the movement to its content
components. This is done in the method rearangeContents(). Currently
only translation and scaling is supported. This means though components
change their position with respect to the rotation of the container and
their relative position, the components rotation does not change.

The contents have to be provided as constructor keyword in form of a
nested dictionary of the following form:

``` {.literal-block}
{
    component1 : { "position":(x,y,z), "rotation":(x,y,z), "scaling":(x,y,z) },
    component2 : { "position":(x,y,z), "rotation":(x,y,z), "scaling":(x,y,z) },
    ...
}
```

Each of the \"position\", \"rotation\" and \"scaling\" arguments specify
the amount relative to the container. They are all optional. As stated
earlier, rotation is not supported yet so setting the rotation has no
effect.

Container components terminate if a producerFinished or
shutdownMicroprocess message is received on their \"control\" inbox. The
received message is also forwarded to the \"signal\" outbox. Upon
termination, this component does *not* unbind itself from the
OpenGLDisplay service and does not free any requested resources.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[Container](/Components/pydoc/Kamaelia.UI.OpenGL.Container.html){.reference}.[Container](/Components/pydoc/Kamaelia.UI.OpenGL.Container.Container.html){.reference}
================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class Container([Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}) {#symbol-Container}
-----------------------------------------------------------------------------------------------------------------------------------------------------

Container(\...) -\> A new Container component.

A container to control several OpenGLComponents.

Keyword arguments:

-   position \-- Initial container position (default=(0,0,0)).
-   rotation \-- Initial container rotation (default=(0,0,0)).
-   scaling \-- Initial container scaling (default=(1,1,1)).
-   contents \-- Nested dictionary of contained components.

::: {.section}
### [Inboxes]{#symbol-Container.Inboxes}

-   **control** : For shutdown messages
-   **scaling** : receive scaling triple (x,y,z)
-   **inbox** :
-   **position** : receive position triple (x,y,z)
-   **rotation** : receive rotation triple (x,y,z)
-   **rel\_scaling** : receive scaling triple (x,y,z)
-   **rel\_position** : receive position triple (x,y,z)
-   **rel\_rotation** : receive rotation triple (x,y,z)
:::

::: {.section}
### [Outboxes]{#symbol-Container.Outboxes}

-   **outbox** :
-   **signal** : For shutdown messages
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-Container.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [addElement(self, comp\[, position\]\[, rotation\]\[, scaling\])]{#symbol-Container.addElement}
:::

::: {.section}
#### [applyTransforms(self)]{#symbol-Container.applyTransforms}

Use the objects translation/rotation/scaling values to generate a new
transformation Matrix if changes have happened.
:::

::: {.section}
#### [handleMovement(self)]{#symbol-Container.handleMovement}

Handle movement commands received by corresponding inboxes.
:::

::: {.section}
#### [main(self)]{#symbol-Container.main}
:::

::: {.section}
#### [rearangeContents(self)]{#symbol-Container.rearangeContents}
:::

::: {.section}
#### [removeElement(self, comp)]{#symbol-Container.removeElement}
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
