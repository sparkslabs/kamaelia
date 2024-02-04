---
pagename: Docs/Axon/Axon.Postoffice.postoffice
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Postoffice](/Docs/Axon/Axon.Postoffice.html){.reference}.[postoffice](/Docs/Axon/Axon.Postoffice.postoffice.html){.reference}
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.Postoffice.html){.reference}

------------------------------------------------------------------------

::: {.section}
class postoffice(object) {#symbol-postoffice}
------------------------

::: {.section}
The post office looks after linkages between postboxes, thereby ensuring
deliveries along linkages occur as intended.

There is one post office per component.

A Postoffice can have a debug name - this is to help differentiate
between postoffices if problems arise.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self\[, debugname\])]{#symbol-postoffice.__init__}

Constructor. If a debug name is assigned this will be stored as a
debugname attribute.
:::

::: {.section}
#### [\_\_str\_\_(self)]{#symbol-postoffice.__str__}

Provides a string representation of a postoffice, designed for debugging
:::

::: {.section}
#### [deregisterlinkage(self\[, thecomponent\]\[, thelinkage\])]{#symbol-postoffice.deregisterlinkage}

Stub for legacy
:::

::: {.section}
#### [islinkageregistered(self, linkage)]{#symbol-postoffice.islinkageregistered}

Returns a true value if the linkage given is registered with the
postoffie.
:::

::: {.section}
#### [link(self, source, sink, \*optionalargs, \*\*kwoptionalargs)]{#symbol-postoffice.link}

link((component,boxname),(component,boxname),\*\*otherargs) -\> new
linkage

Creates a linkage from a named box on one component to a named box on
another. See linkage class for meanings of other arguments. A linkage
object is returned as a handle representing the linkage created.

The linkage is registered with this postoffice.

Throws
[Axon.AxonExceptions.BoxAlreadyLinkedToDestination](/Docs/Axon/Axon.AxonExceptions.BoxAlreadyLinkedToDestination.html){.reference}
if the source is already linked to somewhere else (Axon does not permit
one-to-many).
:::

::: {.section}
#### [unlink(self\[, thecomponent\]\[, thelinkage\])]{#symbol-postoffice.unlink}

unlink(\[thecomponent\]\[,thelinkage\] -\> destroys linkage(s).

Destroys the specified linkage, or linkages for the specified component.

Note, it only destroys linkages registered in this postoffice.
:::

::: {.section}
#### [unlinkAll(self)]{#symbol-postoffice.unlinkAll}

Destroys all linkages made with this postoffice.
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

*\-- Automatic documentation generator, 09 Dec 2009 at 04:00:25 UTC/GMT*
