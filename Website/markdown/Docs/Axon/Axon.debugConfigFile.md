---
pagename: Docs/Axon/Axon.debugConfigFile
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[debugConfigFile](/Docs/Axon/Axon.debugConfigFile.html){.reference}
------------------------------------------------------------------------------------------------------------
:::
:::

::: {.section}
Reading debugging configuration files
=====================================

::: {.container}
-   **[readConfig](/Docs/Axon/Axon.debugConfigFile.readConfig.html){.reference}**(filename)
:::

-   [Debugging configuration file format](#93){.reference}
:::

::: {.section}
The readConfig() method reads debugging configuration from the specified
file.

-   [Axon.debug.debug](/Docs/Axon/Axon.debug.debug.html){.reference}
    uses this to read configuration for itself.

Each call to output debugging information specifies what section it
belongs to and the level of detail it represents. A configuration file
specifies what sections should be expected and what maximum level of
detail should be output for each.

::: {.section}
[Debugging configuration file format]{#debugging-configuration-file-format} {#93}
---------------------------------------------------------------------------

Debugging configuration files are simple text files.

-   **Comments** are lines beginning with a hash \'\#\' character
-   **Blank lines** are permitted
-   **Configuration lines** are a space (not tab) separated triple of
    *section* name, *level* of detail, and *location*

For example:

``` {.literal-block}
# The following tags are for debugging the debug system
#

debugTestClass.even         5  default
debugTestClass.triple       10 default
debugTestClass.run          1  default
debugTestClass.__init__     5  default
debugTestClass.randomChange 10 default
```

For a given *section*, the *level* number specifies the maximum level of
detail that you want outputted. Any calls to output debugging
information for that section but with a higher level number will be
filtered out.

The final *location* field is currently not used. It is recommended to
specify \"default\" for the moment.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[debugConfigFile](/Docs/Axon/Axon.debugConfigFile.html){.reference}.[readConfig](/Docs/Axon/Axon.debugConfigFile.readConfig.html){.reference}
======================================================================================================================================================================================

::: {.section}
[readConfig(filename)]{#symbol-readConfig}
------------------------------------------

Reads debug configuration from the specified file.

Returns a dictionary mapping debugging section names to maximum levels
of detail to be output for that section.
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

*\-- Automatic documentation generator, 09 Dec 2009 at 04:00:25 UTC/GMT*
