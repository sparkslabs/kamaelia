---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.Movement.WheelMover
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[Movement](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.html){.reference}.[WheelMover](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.WheelMover.html){.reference}
===============================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.html){.reference}

------------------------------------------------------------------------

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
