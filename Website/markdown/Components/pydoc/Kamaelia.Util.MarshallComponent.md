---
pagename: Components/pydoc/Kamaelia.Util.MarshallComponent
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[MarshallComponent](/Components/pydoc/Kamaelia.Util.MarshallComponent.html){.reference}
========================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **prefab
    [BasicMarshallComponent](/Components/pydoc/Kamaelia.Util.MarshallComponent.BasicMarshallComponent.html){.reference}**
:::

-   [Legacy stub for BasicMarshallComponent](#201){.reference}
    -   [Example Usage](#202){.reference}
    -   [How does it work?](#203){.reference}
:::

::: {.section}
Legacy stub for BasicMarshallComponent {#201}
======================================

The functionality of this component has been superceeded by the
Marshaller and DeMarshaller components in
[Kamaelia.Util.Marshalling](/Components/pydoc/Kamaelia.Util.Marshalling.html){.reference}.
Please use these in preference.

This component contains both marshalling and demarshalling facilities.
It is a thin wrapper combining a Marshalling and DeMarshalling
component.

::: {.section}
[Example Usage]{#example-usage} {#202}
-------------------------------

None at present.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#203}
--------------------------------------

Behaviour is consistent with that of
[Kamaelia.Util.Marshalling](/Components/pydoc/Kamaelia.Util.Marshalling.html){.reference},
except that the \"inbox\" inbox and \"outbox\" outbox are not used.

Marshall data by sending it to the \"marshall\" inbox. The marshalled
data is sent to the \"marshalled\" outbox.

Demarshall data by sending it to the \"demarshall\" inbox. The
marshalled data is sent to the \"demarshalled\" outbox.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[MarshallComponent](/Components/pydoc/Kamaelia.Util.MarshallComponent.html){.reference}.[BasicMarshallComponent](/Components/pydoc/Kamaelia.Util.MarshallComponent.BasicMarshallComponent.html){.reference}
============================================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: BasicMarshallComponent {#symbol-BasicMarshallComponent}
------------------------------
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
