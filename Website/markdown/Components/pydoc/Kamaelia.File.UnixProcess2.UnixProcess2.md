---
pagename: Components/pydoc/Kamaelia.File.UnixProcess2.UnixProcess2
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[UnixProcess2](/Components/pydoc/Kamaelia.File.UnixProcess2.html){.reference}.[UnixProcess2](/Components/pydoc/Kamaelia.File.UnixProcess2.UnixProcess2.html){.reference}
=========================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.File.UnixProcess2.html){.reference}

------------------------------------------------------------------------

::: {.section}
class UnixProcess2([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-UnixProcess2}
----------------------------------------------------------------------------------------------------

UnixProcess2(command\[,buffersize\]\[,outpipes\]\[,inpipes\]\[,boxsizes\])
-\> new UnixProcess2 component.

Starts the specified command as a separate process. Data can be sent to
stdin and received from stdout. Named pipes can also be created for
extra channels to get data to and from the process.

Keyword arguments:

``` {.literal-block}
- command     -- command line string that will invoke the subprocess
- buffersize  -- bytes size of buffers on the pipes to and from the process (default=32768)
- outpipes    -- dict mapping named-pipe-filenames to outbox names (default={})
- inpipes     -- dict mapping named-pipe-filenames to inbox names (default={})
- boxsizes    -- dict mapping inbox names to box sizes (default={})
```

::: {.section}
### [Inboxes]{#symbol-UnixProcess2.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Binary string data to go to STDIN of the process.
:::

::: {.section}
### [Outboxes]{#symbol-UnixProcess2.Outboxes}

-   **outbox** : Binary string data from STDOUT of the process
-   **signal** : Shutdown signalling
-   **\_shutdownPipes** : For shutting down any named pipes used for
    output
-   **error** : Binary string data from STDERR of the process
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
#### [\_\_init\_\_(self, command\[, buffersize\]\[, outpipes\]\[, inpipes\]\[, boxsizes\])]{#symbol-UnixProcess2.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [childrenDone(self)]{#symbol-UnixProcess2.childrenDone}

Unplugs any children that have terminated, and returns true if there are
no running child components left (ie. their microproceses have finished)
:::

::: {.section}
#### [main(self)]{#symbol-UnixProcess2.main}

main loop
:::

::: {.section}
#### [setupNamedInPipes(self, pipeshutdown)]{#symbol-UnixProcess2.setupNamedInPipes}
:::

::: {.section}
#### [setupNamedOutPipes(self, pipeshutdown)]{#symbol-UnixProcess2.setupNamedOutPipes}
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
