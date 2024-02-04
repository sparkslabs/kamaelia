---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.SimpleTranslationInteractor
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[SimpleTranslationInteractor](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleTranslationInteractor.html){.reference}
=============================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [SimpleTranslationInteractor](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleTranslationInteractor.SimpleTranslationInteractor.html){.reference}**
:::

-   [Simple Translation Interactor](#321){.reference}
    -   [Example Usage](#322){.reference}
    -   [How does it work?](#323){.reference}
:::

::: {.section}
Simple Translation Interactor {#321}
=============================

A simple interactor for moving OpenGLComponents along th X,Y plane.

SimpleTranslationInteractor is a subclass of Interactor.

::: {.section}
[Example Usage]{#example-usage} {#322}
-------------------------------

The following example shows four SimpleCubes which can be moved by
dragging your mouse over them:

``` {.literal-block}
o1 = SimpleCube(position=(6, 0,-30), size=(1,1,1)).activate()
i1 = SimpleTranslationInteractor(target=o1).activate()

o2 = SimpleCube(position=(0, 0,-20), size=(1,1,1)).activate()
i2 = SimpleTranslationInteractor(target=o2).activate()

o3 = SimpleCube(position=(-3, 0,-10), size=(1,1,1)).activate()
i3 = SimpleTranslationInteractor(target=o3).activate()

o4 = SimpleCube(position=(15, 0,-40), size=(1,1,1)).activate()
i4 = SimpleTranslationInteractor(target=o4).activate()

Axon.Scheduler.scheduler.run.runThreads()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#323}
--------------------------------------

SimpleTranslationInteractor is a subclass of Interactor (for Interactor
functionality see its documentation). It overrides the \_\_init\_\_(),
setup() and handleEvents() methods.

The amount of movement is determined using the relative 2d movement
which is included in every mouse event and multiplying it by a factor.
This factor must be specified on creation of the component.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[SimpleTranslationInteractor](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleTranslationInteractor.html){.reference}.[SimpleTranslationInteractor](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleTranslationInteractor.SimpleTranslationInteractor.html){.reference}
==========================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class SimpleTranslationInteractor(Interactor) {#symbol-SimpleTranslationInteractor}
---------------------------------------------

SimpleTranslationInteractor(\...) -\> A new SimpleTranslationInteractor
component.

A simple interactor for moving OpenGLComponents along th X,Y plane.

Keyword arguments:

-   translationfactor \-- factor to translate between 2d and 3d movement
    (default=10.0)

::: {.section}
### [Inboxes]{#symbol-SimpleTranslationInteractor.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-SimpleTranslationInteractor.Outboxes}
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-SimpleTranslationInteractor.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [handleEvents(self)]{#symbol-SimpleTranslationInteractor.handleEvents}
:::

::: {.section}
#### [setup(self)]{#symbol-SimpleTranslationInteractor.setup}
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
