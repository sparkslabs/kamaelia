---
pagename: Components/pydoc/Kamaelia.Chassis.Carousel
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}.[Carousel](/Components/pydoc/Kamaelia.Chassis.Carousel.html){.reference}
===============================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Carousel](/Components/pydoc/Kamaelia.Chassis.Carousel.Carousel.html){.reference}**
:::

-   [Component Carousel Chassis](#278){.reference}
    -   [Example Usage](#279){.reference}
    -   [Why is this useful?](#280){.reference}
    -   [How does it work?](#281){.reference}
-   [Test documentation](#282){.reference}
:::

::: {.section}
Component Carousel Chassis {#278}
==========================

This component lets you create and wire up another component. You can
then swap it for a new one by sending it a message. The message contents
is used by a factory function to create the new replacement component.

The component that is created is a child contained within Carousel. Wire
up to Carousel\'s \"inbox\" inbox and \"outbox\" outbox to send and
receive messages from the child.

::: {.section}
[Example Usage]{#example-usage} {#279}
-------------------------------

A reusable file reader:

``` {.literal-block}
def makeFileReader(filename):
    return ReadFileAdapter(filename = filename, ...other args... )

reusableFileReader = Carousel(componentFactory = makeFileReader)
```

Whenever you send a filename to the \"next\" inbox of the
reusableFileReader component, it will read that file. You can do this as
many times as you wish. The data read from the file comes out of the
carousel\'s outbox.

Putting this re-usable file reader to use: the following simple example
lets the user enter the names of files to read:

``` {.literal-block}
Graphline(
   FILENAME_INPUT = ConsoleReader(prompt="enter a filename>"),
   FILE_READER = Carousel(componentFactory = makeFileReader),
   OUTPUT = ConsoleEchoer(),
   linkages = {
       ("FILENAME_INPUT", "outbox") : ("FILE_READER", "next"),
       ("FILE_READER", "outbox") : ("OUTPUT", "inbox"),
   }).run()
```

The user input causes the Carousel to replace the current file reader
component (if it has not already terminated) with a new one. The output
from this file reader is sent straight back to the console.
:::

::: {.section}
[Why is this useful?]{#why-is-this-useful} {#280}
------------------------------------------

This chassis component is for making a carousel of components. It gets
its name from a broadcast carousel - where a programme (or set of
programmes) is broadcast one after another, often on a loop.
Alternatively, think of public information screens which display a
looping carousel of slides of information.

You gain reusability from things that are not directly reusable and
normally come to a halt. For example, make a carousel of file reader
components, and you can read from more than one file, one after another.
The carousel will make a new file reader component every time you make
new request.

The Carousel automatically sends a \"NEXT\" message when a component
finishes, to prompt you make a new request.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#281}
--------------------------------------

The carousel chassis creates and encapsulates (as a child) the component
you want it to, and lets it get on with it.

Anything sent to the carousel\'s \"inbox\" inbox is passed onto the
child component. Anything the child sends out appears at the carousel\'s
\"outbox\" outbox.

If the child terminates, then the carousel unwires it and sends a
\"NEXT\" message out of its \"requestNext\" outbox (unless of course it
has been told to shutdown).

Another component, such as a Chooser, can respond to this message by
sending the new set of arguments (for the factory function) to the
carousel\'s \"next\" inbox. The carousel then uses your factory function
to create a new child component. This way, a sequence of operations can
be automatically chained together.

If the argument source needs to receive a \"NEXT\" message before
sending its first set of arguments, then set the argument
make1stRequest=True when creating the carousel.

You can actually send new orders to the \"next\" inbox at any time, not
just in response to requests from the Carousel. The carousel will
immediately ask that child to terminate; then as soon as it has done so,
it will create the new one and wire it in in its place.

If Carousel receives an
[Axon.Ipc.producerFinished](/Docs/Axon/Axon.Ipc.producerFinished.html){.reference}
message on its \"control\" inbox then it will finish handling any
pending messages on its \"next\" inbox (in the way described above) then
when there are none left, it will ask the child component to shut down
by sending on the producerFinished message to the child. As soon as the
child has terminated, the Carousel will terminate and send on the
producerFinished message out of its own \"signal\" outbox.

If Carousel receives an
[Axon.Ipc.shutdownMicroprocess](/Docs/Axon/Axon.Ipc.shutdownMicroprocess.html){.reference}
message on its \"control\" inbox then it will immediately send it on to
its child component to ask it to terminate. As soon as the child has
termianted, the Carousel will terminate and send on the
shutdownMicroprocess message out of its own \"signal\" outbox.

Of course, if the Carousel has no child at the time either shutdown
request is received, it will immediately terminate and send on the
message out of its \"signal\" outbox.
:::

Test documentation {#282}
==================

Tests passed:

-   A shutdownMicroprocess or producerFinished message sent to the
    \"control\" inbox of the Carousel gets passed onto the \"control\"
    inbox of the child.
-   Carousel initialises. By default it does nothing.
-   If the make1stRequest argument is set to True at initialisation,
    Carousel sends a \"NEXT\" message out of its \"requestNext\" outbox
    after it has started up.
-   Carousel doesn\'t terminate (in response to producerFinished or
    shutdownMicroprocess) until the child has terminated.
-   If the child sends out a producerFinished or shutdownMicroprocess
    message out of its \"signal\" outbox; the Carousel does not send out
    a message from its \"requestNext\" outbox in response.
-   Messages coming out of the child\'s \"signal\" outbox are ignored.
    They do not emerge from the \"signal\" outbox of the Carousel.
-   When a child terminates; the Carousel sends a \"NEXT\" message out
    of its \"requestNext\" outbox.
-   Any mesasges sent out of the \"outbox\" outbox of a child emerges
    from the \"outbox\" outbox of the Carousel.
-   Any messages sent to the \"inbox\" inbox of the Carousel gets sent
    on tot the \"inbox\" inbox of the child component.
-   When a message is sent to the \"next\" inbox, the supplied factory
    function is run with that argument.
-   Messages sent to the \"next\" inbox trigger the factory function,
    leading to the creation and activation of a child component.
-   A message sent to the \"next\" inbox starts a new child; but only
    once the current child has terminated.
-   If a shutdownMicroprocess() is received, any messages queued on the
    \'next\' inbox are discarded; and Carousel shuts down as soon as any
    current child has terminated.
-   If a producerFinished() is received, but there are still messages
    queued on the \'next\' inbox, those messages are processed (and
    children created) first. \*Then\* the Carousel terminates.
-   When idle, with no child; a shutdownMicroprocess or producerFinished
    message will cause Carousel to terminate.
-   If a producerFinshed or shutdownMicroprocess is sent to a
    Carousel\'s \"control\" inbox, it is passed onto the child\'s
    \"control\" inbox.
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}.[Carousel](/Components/pydoc/Kamaelia.Chassis.Carousel.html){.reference}.[Carousel](/Components/pydoc/Kamaelia.Chassis.Carousel.Carousel.html){.reference}
=================================================================================================================================================================================================================================================================================

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
