---
pagename: Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Visualisation](/Components/pydoc/Kamaelia.Visualisation.html){.reference}.[PhysicsGraph](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.html){.reference}.[lines\_to\_tokenlists](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists.html){.reference}
=============================================================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [lines\_to\_tokenlists](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists.lines_to_tokenlists.html){.reference}**
:::

-   [Simple line-of-text tokeniser](#441){.reference}
    -   [Example Usage](#442){.reference}
    -   [How does it work?](#443){.reference}
:::

::: {.section}
Simple line-of-text tokeniser {#441}
=============================

This component takes a line of text and splits it into space character
separated tokens. Tokens can be encapsulated with single or double quote
marks, allowing spaces to appear within a token.

::: {.section}
[Example Usage]{#example-usage} {#442}
-------------------------------

A simple pieline that takes each line you type and splits it into a list
of tokens, showing you the result:

``` {.literal-block}
Pipeline( ConsoleReader(),
          lines_to_tokenlists(),
          ConsoleEchoer()
        ).run()
```

At runtime::

:   ``` {.first .last .doctest-block}
    >>> Hello world "how are you" 'john said "hi"' "i replied "hi"" "c:\windows" end
    [ 'Hello',
      'world',
      'how are you',
      'john said "hi"',
      'i replied "hi"',
      'c:\windows',
      'end' ]
    ```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#443}
--------------------------------------

lines\_to\_tokenlists receives individual lines of text on its \"inbox\"
inbox. A line is converted to a list of tokens, which is sent out of its
\"outbox\" outbox.

Space characters are treated as the token separator, however a token can
be encapsulated in single or double quotes allowing space characters to
appear within it.

If you need to use a quote mark or backslash within a token encapsulated
by quote marks, it must be escaped by prefixing it with a backslash.
Only do this if the token is encapsulated.

encapsulating quote marks are removed when the line is tokenised.
Escaped backslashes and quote marks are converted to plain backslashes
and quote marks.

If a producerFinished() or shutdownMicroprocess() message is received on
this component\'s \"control\" inbox, then it will send it on out of its
\"signal\" outbox and immediately terminate. It will not flush any whole
lines of text that may still be buffered.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Visualisation](/Components/pydoc/Kamaelia.Visualisation.html){.reference}.[PhysicsGraph](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.html){.reference}.[lines\_to\_tokenlists](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists.html){.reference}.[lines\_to\_tokenlists](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists.lines_to_tokenlists.html){.reference}
=====================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class lines\_to\_tokenlists([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-lines_to_tokenlists}
-------------------------------------------------------------------------------------------------------------

lines\_to\_tokenlists() -\> new lines\_to\_tokenlists component.

Takes individual lines of text and separates them into white space
separated tokens. Tokens can be enclosed with single or double quote
marks.

::: {.section}
### [Inboxes]{#symbol-lines_to_tokenlists.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Individual lines of text
:::

::: {.section}
### [Outboxes]{#symbol-lines_to_tokenlists.Outboxes}

-   **outbox** : list of tokens making up the line of text
-   **signal** : Shutdown signalling
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
#### [\_\_init\_\_(self)]{#symbol-lines_to_tokenlists.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [lineToTokens(self, line)]{#symbol-lines_to_tokenlists.lineToTokens}

linesToTokens(line) -\> list of tokens.

Splits a line into individual white-space separated tokens. Tokens can
be enclosed in single or double quotes to allow spaces to be used in
them.

Escape backslash and single or double quotes by prefixing them with a
backslash *only* if used within an quote encapsulated string.
:::

::: {.section}
#### [main(self)]{#symbol-lines_to_tokenlists.main}

Main loop.
:::

::: {.section}
#### [shutdown(self)]{#symbol-lines_to_tokenlists.shutdown}

Returns True if a shutdownMicroprocess or producerFinished message was
received.
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
