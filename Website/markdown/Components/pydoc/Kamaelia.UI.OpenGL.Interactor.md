---
pagename: Components/pydoc/Kamaelia.UI.OpenGL.Interactor
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[Interactor](/Components/pydoc/Kamaelia.UI.OpenGL.Interactor.html){.reference}
===========================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Interactor](/Components/pydoc/Kamaelia.UI.OpenGL.Interactor.Interactor.html){.reference}**
:::

-   [General Interactor](#291){.reference}
    -   [Example Usage](#292){.reference}
    -   [How does it work?](#293){.reference}
:::

::: {.section}
General Interactor {#291}
==================

This component implements the basic functionality of an Interactor. An
Interactor listens to events of another component and tranlates them
into movement which is applied to the target component. It provides
methods to be overridden for adding functionality.

::: {.section}
[Example Usage]{#example-usage} {#292}
-------------------------------

A very simple Interactor could look like this:

``` {.literal-block}
class VerySimpleInteractor(Interactor):
    def makeInteractorLinkages(self):
        self.link( (self,"outbox"), (self.target, "rel_rotation") )

    def setup(self):
        self.addListenEvents([pygame.MOUSEBUTTONDOWN])

    def handleEvents(self):
        while self.dataReady("events"):
            event = self.recv("events")
            if self.identifier in event.hitobjects:
                self.send((0,90,0))
```

For examples of how to create Interactors have a look at the files
XXXInteractor.py.

A MatchedInteractor and a RotationInteractor each interacting with a
SimpleCube:

``` {.literal-block}
CUBE1 = SimpleCube(size=(1,1,1), position=(1,0,0)).activate()
CUBE2 = SimpleCube(size=(1,1,1), position=(-1,0,0)).activate()
INTERACTOR1 = MatchedTranslationInteractor(target=CUBE1).activate()
INTERACTOR2 = SimpleRotationInteractor(target=CUBE2).activate()

Axon.Scheduler.scheduler.run.runThreads()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#293}
--------------------------------------

Interactor provides functionality for interaction with the OpenGL
display service and OpenGL components. It is designed to be subclassed.
The following methods are provided to be overridden:

-   makeInteractorLinkages() \-- make linkages to and from targets
    needed
-   setup() \-- set up the component
-   handleEvents() \-- handle input events (\"events\" inbox)
-   frame() \-- called every frame, to add additional functionality

Stubs method are provided, so missing these out does not result in
broken code. The methods get called from the main method, the following
code shows in which order:

``` {.literal-block}
def main(self):
    # create and send eventspy request
    ...
    # setup function from derived objects
    self.setup()
    ...
    while 1:
        yield 1
        # handle events function from derived objects
        self.handleEvents()
        # frame function from derived objects
        self.frame()
```

If you need to override the \_\_init\_\_() method, e.g. to get
initialisation parameters, make sure to pass on all keyword arguments to
\_\_init\_\_(\...) of the superclass, e.g.:

``` {.literal-block}
def __init__(self, **argd):
    super(ClassName, self).__init__(**argd)
    # get an initialisation parameter
    myparam = argd.get("myparam", defaultvalue)
```

The following methods are provided to be used by inherited objects:

-   addListenEvents(list of events) \-- Request reception of a list of
    events
-   removeListenEvents(list of events) \-- Stop reveiving events

The are inteded to simplify component handling. For their functionality
see their description.

The event identifier of the target component gets saved in
self.identifier. Use this variable in event handling to determine if the
target component has been hit.

Interactor components terminate if a producerFinished or
shutdownMicroprocess message is received on their \"control\" inbox. The
received message is also forwarded to the \"signal\" outbox. Upon
termination, this component does *not* unbind itself from the
OpenGLDisplay service and does not free any requested resources.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[UI](/Components/pydoc/Kamaelia.UI.html){.reference}.[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}.[Interactor](/Components/pydoc/Kamaelia.UI.OpenGL.Interactor.html){.reference}.[Interactor](/Components/pydoc/Kamaelia.UI.OpenGL.Interactor.Interactor.html){.reference}
=====================================================================================================================================================================================================================================================================================================================================================

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
