---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.Container.Container
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[Container](/Components/pydoc/Kamaelia.UI.OpenGL.Container.html){.reference}.[Container](/Components/pydoc/Kamaelia.UI.OpenGL.Container.Container.html){.reference}
================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.UI.OpenGL.Container.html){.reference}

------------------------------------------------------------------------

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
