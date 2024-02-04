---
pagename: Components/pydoc/Kamaelia.Util.Chooser
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Chooser](/Components/pydoc/Kamaelia.Util.Chooser.html){.reference}
====================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Chooser](/Components/pydoc/Kamaelia.Util.Chooser.Chooser.html){.reference}**
-   **component
    [ForwardIteratingChooser](/Components/pydoc/Kamaelia.Util.Chooser.ForwardIteratingChooser.html){.reference}**
:::

-   [Iterating Over A Predefined List](#156){.reference}
    -   [Example Usage](#157){.reference}
    -   [How does it work?](#158){.reference}
:::

::: {.section}
Iterating Over A Predefined List {#156}
================================

The Chooser component iterates (steps) forwards and backwards through a
list of items. Request the next or previous item and Chooser will return
it.

The ForwardIteratingChooser component only steps forwards, but can
therefore handle more than just lists - for example: infinite sequences.

::: {.section}
[Example Usage]{#example-usage} {#157}
-------------------------------

A simple slideshow:

``` {.literal-block}
items=[ "image1.png", "image2.png", "image3.png", ... ]

Graphline( CHOOSER  = Chooser(items=imagefiles),
           FORWARD  = Button(position=(300,16), msg="NEXT", caption="Next"),
           BACKWARD = Button(position=(16,16),  msg="PREV", caption="Previous"),
           DISPLAY  = Image(position=(16,64), size=(640,480)),
           linkages = { ("FORWARD" ,"outbox") : ("CHOOSER","inbox"),
                        ("BACKWARD","outbox") : ("CHOOSER","inbox"),
                        ("CHOOSER" ,"outbox") : ("DISPLAY","inbox"),
                      }
         ).run()
```

The chooser is driven by the \'next\' and \'previous\' Button
components. Chooser then sends filenames to an Image component to
display them.

Another example: a forever looping carousel of files, read at 1MBit/s:

``` {.literal-block}
def filenames():
    while 1:
        yield "file 1"
        yield "file 2"
        yield "file 3"

JoinChooserToCarousel( chooser = InfiniteChooser(items=filenames),
                       carousel = FixedRateControlledReusableFilereader("byte",rate=131072,chunksize=1024),
                     )
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#158}
--------------------------------------

When creating it, pass the component a set of items for it to iterate
over.

Chooser will only accept finite length datasets. InfiniteChooser will
accept any interable sequence, even one that never ends from a
generator.

Once activated, the component will emit the first item from the list
from its \"outbox\" outbox.

If the list/sequence is empty, then nothing is emitted, even in response
to messages sent to the \"inbox\" inbox described now.

Send commands to the \"inbox\" inbox to move onto another item of data
and cause it to be emitted. This behaviour is very much like a database
cursor or file pointer - you are issuing commands to step through a
dataset.

Send \"SAME\" and the component will emit the same item of data that was
last emitted last time. Both Chooser and InfiniteChooser respond to this
request.

Send \"NEXT\" and the component will emit the next item from the list or
sequence. If there is no \'next\' item (becuase we are already at the
end of the list/sequence) then nothing is emitted. Both Chooser and
InfiniteChooser respond to this request.

With InfiniteChooser, if there is not \'next\' item then, additionally,
a producerFinished message will be sent out of its \"signal\" outbox to
signal that the end of the sequence has been reached. The component will
then terminate.

All requests described from now are only supported by the Chooser
component. InfiniteChooser will ignore them.

Send \"PREV\" and the previous item from the list or sequence will be
emitted. If there is no previous item (because we are already at the
front of the list/sequence) then nothing is emitted.

Send \"FIRST\" or \"LAST\" and the first or last item from the list or
sequence will be emitted, respectively. The item will be emitted even if
we are already at the first/last item.

If Chooser or InfiniteChooser receive a shutdownMicroprocess message on
the \"control\" inbox, they will pass it on out of the \"signal\"
outbox. The component will then terminate.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Chooser](/Components/pydoc/Kamaelia.Util.Chooser.html){.reference}.[Chooser](/Components/pydoc/Kamaelia.Util.Chooser.Chooser.html){.reference}
================================================================================================================================================================================================================================================================

::: {.section}
class Chooser([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Chooser}
-----------------------------------------------------------------------------------------------

Chooser(\[items\]) -\> new Chooser component.

Iterates through a finite list of items. Step by sending \"NEXT\",
\"PREV\", \"FIRST\" or \"LAST\" messages to its \"inbox\" inbox.

Keyword arguments:

-   items \-- list of items to be chosen from, must be type \'list\'
    (default=\[\])

::: {.section}
### [Inboxes]{#symbol-Chooser.Inboxes}

-   **control** : shutdown messages
-   **inbox** : receive commands
:::

::: {.section}
### [Outboxes]{#symbol-Chooser.Outboxes}

-   **outbox** : emits chosen items
-   **signal** : shutdown messages
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
#### [\_\_init\_\_(self\[, items\])]{#symbol-Chooser.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [getCurrentChoice(self)]{#symbol-Chooser.getCurrentChoice}

Return the current choice to the outbox
:::

::: {.section}
#### [gotoFirst(self)]{#symbol-Chooser.gotoFirst}

Goto the first item in the set. Returns True.
:::

::: {.section}
#### [gotoLast(self)]{#symbol-Chooser.gotoLast}

Goto the last item in the set. Returns True.
:::

::: {.section}
#### [gotoNext(self)]{#symbol-Chooser.gotoNext}

Advance the choice forwards one.

Returns True if successful or False if unable to (eg. already at end).
:::

::: {.section}
#### [gotoPrev(self)]{#symbol-Chooser.gotoPrev}

Backstep the choice backwards one.

Returns True if successful or False if unable to (eg. already at start).
:::

::: {.section}
#### [main(self)]{#symbol-Chooser.main}

Main loop.
:::

::: {.section}
#### [shutdown(self)]{#symbol-Chooser.shutdown}

Returns True if a shutdownMicroprocess message was received.
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Chooser](/Components/pydoc/Kamaelia.Util.Chooser.html){.reference}.[ForwardIteratingChooser](/Components/pydoc/Kamaelia.Util.Chooser.ForwardIteratingChooser.html){.reference}
================================================================================================================================================================================================================================================================================================

::: {.section}
class ForwardIteratingChooser([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-ForwardIteratingChooser}
---------------------------------------------------------------------------------------------------------------

Chooser(\[items\]) -\> new Chooser component.

Iterates through an iterable set of items. Step by sending \"NEXT\"
messages to its \"inbox\" inbox.

Keyword arguments: - items \-- iterable source of items to be chosen
from (default=\[\])

::: {.section}
### [Inboxes]{#symbol-ForwardIteratingChooser.Inboxes}

-   **control** : shutdown messages
-   **inbox** : receive commands
:::

::: {.section}
### [Outboxes]{#symbol-ForwardIteratingChooser.Outboxes}

-   **outbox** : emits chosen items
-   **signal** : shutdown messages
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
#### [\_\_init\_\_(self\[, items\])]{#symbol-ForwardIteratingChooser.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [getCurrentChoice(self)]{#symbol-ForwardIteratingChooser.getCurrentChoice}

Return the current choice
:::

::: {.section}
#### [gotoNext(self)]{#symbol-ForwardIteratingChooser.gotoNext}

Advance the choice forwards one.

Returns True if successful or False if unable to (eg. already at end).
:::

::: {.section}
#### [main(self)]{#symbol-ForwardIteratingChooser.main}

Main loop.
:::

::: {.section}
#### [shutdown(self)]{#symbol-ForwardIteratingChooser.shutdown}

Returns True if a shutdownMicroprocess message was received.
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
