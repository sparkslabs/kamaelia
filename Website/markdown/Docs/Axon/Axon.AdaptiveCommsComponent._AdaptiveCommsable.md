---
pagename: Docs/Axon/Axon.AdaptiveCommsComponent._AdaptiveCommsable
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.html){.reference}.[\_AdaptiveCommsable](/Docs/Axon/Axon.AdaptiveCommsComponent._AdaptiveCommsable.html){.reference}
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.AdaptiveCommsComponent.html){.reference}

------------------------------------------------------------------------

::: {.section}
class \_AdaptiveCommsable(object) {#symbol-_AdaptiveCommsable}
---------------------------------

::: {.section}
Mixin for making a component \'adaptable\' so that it can create and
destroy extra inboxes and outboxes at runtime.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, \*args, \*\*argd)]{#symbol-_AdaptiveCommsable.__init__}
:::

::: {.section}
#### [\_newInboxName(self\[, name\])]{#symbol-_AdaptiveCommsable._newInboxName}

Allocates a new inbox with name *based on* the name provided.

If this name is available it will be returned unchanged. Otherwise the
name will be returned with a number appended
:::

::: {.section}
#### [\_newOutboxName(self\[, name\])]{#symbol-_AdaptiveCommsable._newOutboxName}

Allocates a new outbox name *based on* the name provided.

If this name is available it will be returned unchanged. Otherwise the
name will be returned with a number appended
:::

::: {.section}
#### [addInbox(self, \*args)]{#symbol-_AdaptiveCommsable.addInbox}

Allocates a new inbox with name *based on* the name provided. If a box
with the suggested name already exists then a variant is used instead.

Returns the name of the inbox added.
:::

::: {.section}
#### [addOutbox(self, \*args)]{#symbol-_AdaptiveCommsable.addOutbox}

Allocates a new outbox with name *based on* the name provided. If a box
with the suggested name already exists then a variant is used instead.

Returns the name of the outbox added.
:::

::: {.section}
#### [ceaseTrackingResource(self, resource)]{#symbol-_AdaptiveCommsable.ceaseTrackingResource}

Stop tracking a resource and release references to it
:::

::: {.section}
#### [deleteInbox(self, name)]{#symbol-_AdaptiveCommsable.deleteInbox}

Deletes the named inbox. Any messages in it are lost.

Try to ensure any linkages to involving this outbox have been destroyed
- not just ones created by this component, but by others too! Behaviour
is undefined if this is not the case, and should be avoided.
:::

::: {.section}
#### [deleteOutbox(self, name)]{#symbol-_AdaptiveCommsable.deleteOutbox}

Deletes the named outbox.

Try to ensure any linkages to involving this outbox have been destroyed
- not just ones created by this component, but by others too! Behaviour
is undefined if this is not the case, and should be avoided.
:::

::: {.section}
#### [retrieveTrackedResource(self, inbox)]{#symbol-_AdaptiveCommsable.retrieveTrackedResource}

Retrieve the resource that has been associated with the named inbox.
:::

::: {.section}
#### [retrieveTrackedResourceInformation(self, resource)]{#symbol-_AdaptiveCommsable.retrieveTrackedResourceInformation}

Retrieve a tuple (inboxes, outboxes, otherdata) that has been stored as
the specified resource.
:::

::: {.section}
#### [trackResource(self, resource, inbox)]{#symbol-_AdaptiveCommsable.trackResource}

Associate the specified resource with the named inbox.
:::

::: {.section}
#### [trackResourceInformation(self, resource, inboxes, outboxes, information)]{#symbol-_AdaptiveCommsable.trackResourceInformation}

Store a list of inboxes, outboxes and other information as the specified
resource.

The inboxes and outboxes specified must exist.
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
