---
pagename: Components/pydoc/Kamaelia.Util.Comparator
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Comparator](/Components/pydoc/Kamaelia.Util.Comparator.html){.reference}
==========================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Comparator](/Components/pydoc/Kamaelia.Util.Comparator.Comparator.html){.reference}**
:::

-   [Comparing two data sources](#204){.reference}
    -   [Example Usage](#205){.reference}
    -   [How does it work?](#206){.reference}
:::

::: {.section}
Comparing two data sources {#204}
==========================

The Comparator component tests two incoming streams to see if the items
they contain match (pass an equality test).

::: {.section}
[Example Usage]{#example-usage} {#205}
-------------------------------

Compares contents of two files and prints \"MISMATCH!\" whenever one is
found:

``` {.literal-block}
class DetectFalse(component):
    def main(self):
        while 1:
            yield 1
            if self.dataReady("inbox"):
                if not self.recv("inbox"):
                    print "MISMATCH!"

Graphline( file1   = RateControlledFileReader(filename="file 1", ...),
           file2   = RateControlledFileReader(filename="file 2", ...),
           compare = Comparator(),
           fdetect = DetectFalse(),
           output  = ConsoleEchoer(),
           linkages = {
               ("file1","outbox") : ("compare","inA"),
               ("file2","outbox") : ("compare","inB"),
               ("compare", "outbox") : ("fdetect", "inbox"),
               ("fdetect", "outbox") : ("output", "inbox"),
           },
         ).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#206}
--------------------------------------

The component simply waits until there is data ready on both its \"inA\"
and \"inB\" inboxes, then takes an item from each and compares them. The
result of the comparison is sent to the \"outbox\" outbox.

If data is available at neither, or only one, of the two inboxes, then
the component will wait indefinitely until data is available on both.

If a producerFinished or shutdownMicroprocess message is received on the
\"control\" inbox, then a producerFinished message is sent out of the
\"signal\" outbox and the component terminates.

The comparison is done by the combine() method. This method returns the
result of a simple equality test of the two arguments.

You could always subclass this component and reimplement the combine()
method to perform different functions (for example, an \'adder\').
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Comparator](/Components/pydoc/Kamaelia.Util.Comparator.html){.reference}.[Comparator](/Components/pydoc/Kamaelia.Util.Comparator.Comparator.html){.reference}
===============================================================================================================================================================================================================================================================================

::: {.section}
class Comparator([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Comparator}
--------------------------------------------------------------------------------------------------

Comparator() -\> new Comparator component.

Compares items received on \"inA\" inbox with items received on \"inB\"
inbox. For each pair, outputs True if items compare equal, otherwise
False.

::: {.section}
### [Inboxes]{#symbol-Comparator.Inboxes}

-   **control** : NOT USED
-   **inbox** : NOT USED
-   **inB** : Source \'B\' of items to compare
-   **inA** : Source \'A\' of items to compare
:::

::: {.section}
### [Outboxes]{#symbol-Comparator.Outboxes}

-   **outbox** : Result of comparison
-   **signal** : NOT USED
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
#### [combine(self, valA, valB)]{#symbol-Comparator.combine}

Returns result of (valA == valB)

Reimplement this method to change the type of comparison from equality
testing.
:::

::: {.section}
#### [mainBody(self)]{#symbol-Comparator.mainBody}

Main loop body.
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
