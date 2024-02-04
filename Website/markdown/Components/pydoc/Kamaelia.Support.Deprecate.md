---
pagename: Components/pydoc/Kamaelia.Support.Deprecate
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Support](/Components/pydoc/Kamaelia.Support.html){.reference}.[Deprecate](/Components/pydoc/Kamaelia.Support.Deprecate.html){.reference}
=================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [Kamaelia Deprecation infrastructure](#36){.reference}
:::

::: {.section}
(this is stub documentation) FIXME: Documentation

::: {.section}
[Kamaelia Deprecation infrastructure]{#kamaelia-deprecation-infrastructure} {#36}
---------------------------------------------------------------------------

You can set a global environment variable -
KAMAELIA\_DEPRECATION\_WARNINGS - to control debug warnings.

Possible values of KAMAELIA\_DEPRECATION\_WARNINGS:

  -----------------------------------------------------------------------
  Value     Action
  --------- -------------------------------------------------------------
  (not set) This causes the default debug level for warnings \-- (QUIET)

  QUIET     Supresses all deprecation warnings

  WARN      Display warning only for first usage of each deprecated
            entity

  VERBOSE   Displays warning for all deprecations, including traceback
            for each

  CRASH     Raises exception causing the component (and probably the
            system) to crash - useful especially during testing
  -----------------------------------------------------------------------
:::
:::

------------------------------------------------------------------------

::: {.section}
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
