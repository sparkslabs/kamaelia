---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.LiftTranslationInteractor
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[LiftTranslationInteractor](/Components/pydoc/Kamaelia.UI.OpenGL.LiftTranslationInteractor.html){.reference}
=========================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [LiftTranslationInteractor](/Components/pydoc/Kamaelia.UI.OpenGL.LiftTranslationInteractor.LiftTranslationInteractor.html){.reference}**
:::

-   [Lift Translation Interactor](#300){.reference}
    -   [Example Usage](#301){.reference}
    -   [How does it work?](#302){.reference}
:::

::: {.section}
Lift Translation Interactor {#300}
===========================

An interactor for moving OpenGLComponents corresponding to mouse
movement along the X,Y plane. When \"grabbing\" an object it is lifted
by a specified amount.

LiftTranslationInteractor is a subclass of Interactor.

::: {.section}
[Example Usage]{#example-usage} {#301}
-------------------------------

The following example shows four SimpleCubes which can be moved by
dragging your mouse:

``` {.literal-block}
o1 = SimpleCube(position=(6, 0,-30), size=(1,1,1), name="center").activate()
i1 = LiftTranslationInteractor(target=o1).activate()

o2 = SimpleCube(position=(0, 0,-30), size=(1,1,1), name="center").activate()
i2 = LiftTranslationInteractor(target=o2).activate()

o3 = SimpleCube(position=(-3, 0,-30), size=(1,1,1), name="center").activate()
i3 = LiftTranslationInteractor(target=o3).activate()

o4 = SimpleCube(position=(15, 0,-30), size=(1,1,1), name="center").activate()
i4 = LiftTranslationInteractor(target=o4).activate()

Axon.Scheduler.scheduler.run.runThreads()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#302}
--------------------------------------

LiftTranslationInteractor is a subclass of Interactor. It overrides the
\_\_ini\_\_(), setup(), handleEvents() and frame() methods.

The matched movement works by using the position of the controlled
object and determine its X,Y-aligned plane. The amount of mouse movement
is then calculated as if it was on this plane. This is done by
intersecting the direction vector which is included in the mouse event
with the plane to get the point of intersection. Then the distance
between the newly generated point and the last point is calculated. The
result is the actual amount of movement along the X and the Y axis.

The interactor makes all the linkages it needs during initialisation.
Because the interactor needs the actual position of the controlled
component to be accurate all the time, it uses the components
\"position\" outbox by default. If you don\'t want the interactor to
make the linkages, you can set nolink=True as constructor argument. The
following linkages are needed for the interactor to work (from the
interactors point of view):

``` {.literal-block}
self.link( (self, "outbox"), (self.target, "rel_position") )
self.link( (self.target, "position"), (self, "inbox") )
```
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[LiftTranslationInteractor](/Components/pydoc/Kamaelia.UI.OpenGL.LiftTranslationInteractor.html){.reference}.[LiftTranslationInteractor](/Components/pydoc/Kamaelia.UI.OpenGL.LiftTranslationInteractor.LiftTranslationInteractor.html){.reference}
================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class LiftTranslationInteractor(Interactor) {#symbol-LiftTranslationInteractor}
-------------------------------------------

LiftTranslationInteractor(\...) -\> A new LiftTranslationInteractor
component.

An interactor for moving OpenGLComponents corresponding to mouse
movement along the X,Y plane. When \"grabbing\" an object it is lifted
by a specified amount.

Keyword arguments:

-   liftheight \-- height by which the controlled object is lifted
    (default=2)

::: {.section}
### [Inboxes]{#symbol-LiftTranslationInteractor.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-LiftTranslationInteractor.Outboxes}
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-LiftTranslationInteractor.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [frame(self)]{#symbol-LiftTranslationInteractor.frame}
:::

::: {.section}
#### [handleEvents(self)]{#symbol-LiftTranslationInteractor.handleEvents}
:::

::: {.section}
#### [setup(self)]{#symbol-LiftTranslationInteractor.setup}
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
