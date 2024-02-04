---
pagename: Components/Kamaelia.Chassis.Carousel.Carousel
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Kamaelia.Chassis.Carousel.Carousel]{style="font-size:24pt;font-weight:600"}

[Here we go again, and again,\...]{style="font-size:16pt"}

[Descripton]{style="font-size:14pt;font-weight:600"}

::: {.boxright}
[Inboxes:]{style="font-weight:600"}

-   [inbox]{style="font-family:Courier"} - passthrough to child
-   [next]{style="font-family:Courier"} - where we receive requests to
    replace the child component
-   [control]{style="font-family:Courier"} - where we recieve shutdown
    requests from outside
-   [\_control]{style="font-family:Courier"} - Expect
    \'producerFinished\' or \'shutdownMicroprocess\' from child

[Outboxes:]{style="font-weight:600"}

-   [outbox]{style="font-family:Courier"} - passthrough from child
-   [signal]{style="font-family:Courier"} -
-   [\_signal]{style="font-family:Courier"} - For sending
    \'shutdownMicroprocess\' to child
-   [requestNext]{style="font-family:Courier"} - For requesting new
    child component
:::

This chassis component is for making a carousel of components. It gets
its name from a broadcast carousel - where a programme (or set of
programmes) is broadcast one after another, often on a loop.
Alternatively, think of public information screens which display a
looping carousel of slides of information.

If this makes no sense, suppose you want to read data from a sequence of
files - one after another. Provide a carousel with a filereader
component and a source of filenames, and it will make a new filereader
for each file in turn, outputting their data one after another. The
carousel automatically asks the filename source for a new item when its
current child signals that it has finished.

You gain reusability from things that are not directly reusable and
normally come to a halt.

[Examples]{style="font-size:14pt;font-weight:600"}

Reading from a sequence of files

1\. Write a factory function that takes a single argument and returns a
new component for the carousel:

2\. Make the carousel giving it the factory function:

3\. Make a source of instructions for the carousel: (in this case, a
source of filenames)

4\. Wire the source and carousel together:

5\. Activate:

[How does it work?]{style="font-size:14pt;font-weight:600"}

The carousel chassis creates and encapsulates (as a child) the component
you want it to, and lets it get on with it.

Anything sent to the carousel\'s \"inbox\" inbox is passed onto the
child component. Anything the child sends out appears at the carousel\'s
\"outbox\" and \"signal\" outboxes.

If the child sends an
[Axon.Ipc.shutdownMicroprocess]{style="font-family:Courier"} or
[Axon.Ipc.producerFinished]{style="font-family:Courier"} message then
the carousel gets rid of that component and sends a \"NEXT\" message to
its \"[requestNext]{style="font-family:Courier"}\" outbox.

Another component, such as a Chooser, should respond to this message by
sending the new set of arguments (for the factory function) to the
carousel\'s \"next\" inbox. The carousel then uses your factory function
to create a new child component. And so the cycle repeats.

If the argument source needs to receive a \"NEXT\" message before
sending its first set of arguments, then set the argument
make1stRequest=True when creating the carousel.

You can send new orders to the [next]{style="font-family:Courier"} inbox
at any time. The carousel will immediately unwire that child (and create
the new one) and ask the old child to shut down by sending an
[Axon.Ipc.shutdownMicroprocess]{style="font-family:Courier"} message to
its [control]{style="font-family:Courier"} inbox.

The carousel will shutdown in response to an
[Axon.Ipc.shutdownMicroprocess]{style="font-family:Courier"} or
[Axon.Ipc.producerFinished]{style="font-family:Courier"} message. It
will also terminate any child component in the same way as described
above.

[Pydoc Style Docs]{style="font-size:14pt;font-weight:600"}

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}.[Carousel](/Components/pydoc/Kamaelia.Chassis.Carousel.html){.reference}.[Carousel](/Components/pydoc/Kamaelia.Chassis.Carousel.Carousel.html){.reference}
=================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Chassis.Carousel.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Carousel([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Carousel}
------------------------------------------------------------------------------------------------

Carousel(componentFactory,\[make1stRequest\]) -\> new Carousel component

Create a Carousel component that makes child components one at a time
(in carousel fashion) using the supplied factory function.

Keyword arguments:

-   componentFactory \-- function that takes a single argument and
    returns a component
-   make1stRequest \-- if True, Carousel will send an initial \"NEXT\"
    request. (default=False)

::: {.section}
### [Inboxes]{#symbol-Carousel.Inboxes}

-   **control** :
-   **inbox** : child\'s inbox
-   **next** : requests to replace child
:::

::: {.section}
### [Outboxes]{#symbol-Carousel.Outboxes}

-   **outbox** : child\'s outbox
-   **signal** :
-   **\_signal** : internal use: for sending \'shutdownMicroprocess\' to
    child
-   **requestNext** : for requesting new child component
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
#### [\_\_init\_\_(self, componentFactory\[, make1stRequest\])]{#symbol-Carousel.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [checkControl(self)]{#symbol-Carousel.checkControl}
:::

::: {.section}
#### [handleChildTerminations(self)]{#symbol-Carousel.handleChildTerminations}

Unplugs any children that have terminated
:::

::: {.section}
#### [instantiateNewChild(self, args)]{#symbol-Carousel.instantiateNewChild}
:::

::: {.section}
#### [main(self)]{#symbol-Carousel.main}
:::

::: {.section}
#### [requestNext(self)]{#symbol-Carousel.requestNext}

Sends \'next\' out the \'requestNext\' outbox
:::

::: {.section}
#### [shutdownChild(self, shutdownMsg)]{#symbol-Carousel.shutdownChild}
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

class Carousel(Axon.Component.component)

A carousel component that makes child components one at a time and lets
them do their stuff. Replacing them when they terminate or if requested
to do so.

[Inboxes:]{style="font-weight:600"}

-   inbox - passthrough to child\'s inbox \"inbox\"
-   next - where we recieve requests to replace the child component
-   control - where we recieve shutdown requests from outside
-   \_control - internal use : to recieve \'producerFinished\' or
    \'shutdownMicroprocess\' from child

[Outboxes:]{style="font-weight:600"}

-   outbox - passthrough from child\'s outbox \"outbox\"
-   signal -
-   \_signal - internal use: for sending \'shutdownMicroprocess\' to
    child

requestNext - for requesting new child component

[All methods, except \_\_init\_\_ are private implementation details of
the component]{style="font-weight:600"}

[\_\_init\_\_(self, componentFactory,
make1stRequest=False)]{style="font-weight:600"}

-   \_\_init\_\_(componentFactory)
-   \_\_init\_\_(componentFactory,make1stRequest=True)
-   componentFactory(argument) -\> new component\
    factory function for creating a new child according to specified
    arguments
-   make1stRequest = True\
    Carousel will, immediately after activation, send a \"NEXT\" message
    to its \"requestNext\" outbox. Otherwise the carousel just waits.

[handleFinishedChild(self)]{style="font-weight:600"}

Unplugs the child if a shutdownMicroprocess or producerFinished message
is received from it. Also sends a \"NEXT\" request if one has not
already been sent.

[handleNewChild(self)]{style="font-weight:600"}

If data received on \"next\" inbox, removes any existing child and
creates and wires in a new one.

Received data is passed as an argument to the factory function (supplied
at initialisation) that creates the new child.

[main(self)]{style="font-weight:600"}

Main loop

[requestNext(self)]{style="font-weight:600"}

Sends \'next\' out the \'requestNext\' outbox

[shutdown(self)]{style="font-weight:600"}

Returns True if a shutdownMicroprocess or producerFinished message was
received.

[unplugChildren(self)]{style="font-weight:600"}

Sends \'shutdownMicroprocess\' to children and unwires and disowns them.
