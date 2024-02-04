---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.Movement.PathMover
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[Movement](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.html){.reference}.[PathMover](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.PathMover.html){.reference}
=============================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.html){.reference}

------------------------------------------------------------------------

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
