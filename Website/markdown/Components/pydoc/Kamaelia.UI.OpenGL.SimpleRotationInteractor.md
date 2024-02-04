---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.SimpleRotationInteractor
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[SimpleRotationInteractor](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleRotationInteractor.html){.reference}
=======================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [SimpleRotationInteractor](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleRotationInteractor.SimpleRotationInteractor.html){.reference}**
:::

-   [Simple Rotation Interactor](#297){.reference}
    -   [Example Usage](#298){.reference}
    -   [How does it work?](#299){.reference}
:::

::: {.section}
Simple Rotation Interactor {#297}
==========================

A simple interactor for rotating OpenGLComponents around the X,Y axes.

SimpleRotationInteractor is a subclass of Interactor.

::: {.section}
[Example Usage]{#example-usage} {#298}
-------------------------------

The following example shows four SimpleCubes which can be rotated by
dragging your mouse over them:

``` {.literal-block}
o1 = SimpleCube(position=(6, 0,-30), size=(1,1,1)).activate()
i1 = SimpleRotationInteractor(target=o1).activate()

o2 = SimpleCube(position=(0, 0,-20), size=(1,1,1)).activate()
i2 = SimpleRotationInteractor(target=o2).activate()

o3 = SimpleCube(position=(-3, 0,-10), size=(1,1,1)).activate()
i3 = SimpleRotationInteractor(target=o3).activate()

o4 = SimpleCube(position=(15, 0,-40), size=(1,1,1)).activate()
i4 = SimpleRotationInteractor(target=o4).activate()

Axon.Scheduler.scheduler.run.runThreads()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#299}
--------------------------------------

SimpleTranslationInteractor is a subclass of Interactor (for Interactor
functionality see its documentation). It overrides the \_\_init\_\_(),
setup() and handleEvents() methods.

The amount of rotation is determined using the relative 2d movement
which is included in every mouse event and multiplying it by a factor.
This factor must be specified on creation of the component.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[SimpleRotationInteractor](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleRotationInteractor.html){.reference}.[SimpleRotationInteractor](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleRotationInteractor.SimpleRotationInteractor.html){.reference}
===========================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class SimpleRotationInteractor(Interactor) {#symbol-SimpleRotationInteractor}
------------------------------------------

SimpleRotationInteractor(\...) -\> A new SimpleRotationInteractor
component.

A simple interactor for rotating OpenGLComponents around the X,Y axes.

Keyword arguments:

-   rotationfactor \-- factor to translate between 2d movment and 3d
    rotation (default=10.0)

::: {.section}
### [Inboxes]{#symbol-SimpleRotationInteractor.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-SimpleRotationInteractor.Outboxes}
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-SimpleRotationInteractor.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [handleEvents(self)]{#symbol-SimpleRotationInteractor.handleEvents}
:::

::: {.section}
#### [setup(self)]{#symbol-SimpleRotationInteractor.setup}
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
