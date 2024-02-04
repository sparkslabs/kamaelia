---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.Interactor.Interactor
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[Interactor](/Components/pydoc/Kamaelia.UI.OpenGL.Interactor.html){.reference}.[Interactor](/Components/pydoc/Kamaelia.UI.OpenGL.Interactor.Interactor.html){.reference}
=====================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.UI.OpenGL.Interactor.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Interactor([Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}) {#symbol-Interactor}
------------------------------------------------------------------------------------------------------------------------------------------------------

Interactor(\...) -\> A new Interactor object (not very useful, designed
to be subclassed)

This component implements the basic functionality of an Interactor. An
Interactor listens to events of another component and tranlates them
into movement which is applied to the target component. It provides
methods to be overridden for adding functionality.

Keyword arguments:

-   target \-- OpenGL component to interact with
-   nolink \-- if True, no linkages are made (default=False)

::: {.section}
### [Inboxes]{#symbol-Interactor.Inboxes}

-   **control** : For shutdown messages
-   **callback** : for the response after a displayrequest
-   **inbox** : not used
-   **events** : Input events
:::

::: {.section}
### [Outboxes]{#symbol-Interactor.Outboxes}

-   **outbox** : used for sending relative tranlational movement
-   **signal** : For shutdown messages
-   **display\_signal** : Outbox used for communicating to the display
    surface
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-Interactor.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [addListenEvents(self, events)]{#symbol-Interactor.addListenEvents}

Sends listening request for pygame events to the display service. The
events parameter is expected to be a list of pygame event constants.
:::

::: {.section}
#### [frame(self)]{#symbol-Interactor.frame}

Method stub

Override this method for operations you want to do every frame. It will
be called every time the component is scheduled. Do not include infinite
loops, the method has to return every time it gets called.
:::

::: {.section}
#### [handleEvents(self)]{#symbol-Interactor.handleEvents}

Method stub

Override this method to do event handling inside. Should look like this:

``` {.literal-block}
while self.dataReady("events"):
    event = self.recv("events")
    # handle event ...
```
:::

::: {.section}
#### [main(self)]{#symbol-Interactor.main}
:::

::: {.section}
#### [makeInteractorLinkages(self)]{#symbol-Interactor.makeInteractorLinkages}

Method stub
:::

::: {.section}
#### [removeListenEvents(self, events)]{#symbol-Interactor.removeListenEvents}

Sends stop listening request for pygame events to the display service.
The events parameter is expected to be a list of pygame event constants.
:::

::: {.section}
#### [setup(self)]{#symbol-Interactor.setup}

Method stub

Override this method for component setup. It will be called on the first
scheduling of the component.
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
