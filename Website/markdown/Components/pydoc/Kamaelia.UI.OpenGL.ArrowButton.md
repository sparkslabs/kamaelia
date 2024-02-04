---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.ArrowButton
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[ArrowButton](/Components/pydoc/Kamaelia.UI.OpenGL.ArrowButton.html){.reference}
=============================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [ArrowButton](/Components/pydoc/Kamaelia.UI.OpenGL.ArrowButton.ArrowButton.html){.reference}**
:::

-   [Simple Arrow Button component](#337){.reference}
    -   [Example Usage](#338){.reference}
:::

::: {.section}
Simple Arrow Button component {#337}
=============================

A simple arrow shaped button without caption. Implements responsive
button behavoir.

ArrowButton is a subclass of SimpleButton. It only overrides the draw()
method, i.e. it only changes its appearance.

::: {.section}
[Example Usage]{#example-usage} {#338}
-------------------------------

Two arrow buttons printing to the console:

``` {.literal-block}
Graphline(
    button1 = ArrowButton(size=(1,1,0.3), position=(-2,0,-10), msg="PINKY"),
    button2 = ArrowButton(size=(2,2,1), position=(5,0,-15), rotation=(0,0,90), msg="BRAIN"),
    echo = ConsoleEchoer(),
    linkages = {
        ("button1", "outbox") : ("echo", "inbox"),
        ("button2", "outbox") : ("echo", "inbox")
    }
).run()
```
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[ArrowButton](/Components/pydoc/Kamaelia.UI.OpenGL.ArrowButton.html){.reference}.[ArrowButton](/Components/pydoc/Kamaelia.UI.OpenGL.ArrowButton.ArrowButton.html){.reference}
==========================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class ArrowButton([Kamaelia.UI.OpenGL.SimpleButton.SimpleButton](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleButton.SimpleButton.html){.reference}) {#symbol-ArrowButton}
--------------------------------------------------------------------------------------------------------------------------------------------------

ArrowButton(\...) -\> A new ArrowButton component.

A simple arrow shaped button without caption. Implements responsive
button behavoir.

::: {.section}
### [Inboxes]{#symbol-ArrowButton.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-ArrowButton.Outboxes}
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
#### [draw(self)]{#symbol-ArrowButton.draw}
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from [Kamaelia.UI.OpenGL.SimpleButton.SimpleButton](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleButton.SimpleButton.html){.reference} :

-   [setup](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleButton.html#symbol-SimpleButton.setup){.reference}(self)
-   [\_\_init\_\_](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleButton.html#symbol-SimpleButton.__init__){.reference}(self,
    \*\*argd)
-   [handleEvents](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleButton.html#symbol-SimpleButton.handleEvents){.reference}(self)
:::

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
-   [frame](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.html#symbol-OpenGLComponent.frame){.reference}(self)
:::
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
