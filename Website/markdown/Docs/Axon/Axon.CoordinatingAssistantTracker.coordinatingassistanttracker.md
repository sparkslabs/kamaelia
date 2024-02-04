---
pagename: Docs/Axon/Axon.CoordinatingAssistantTracker.coordinatingassistanttracker
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[CoordinatingAssistantTracker](/Docs/Axon/Axon.CoordinatingAssistantTracker.html){.reference}.[coordinatingassistanttracker](/Docs/Axon/Axon.CoordinatingAssistantTracker.coordinatingassistanttracker.html){.reference}
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.CoordinatingAssistantTracker.html){.reference}

------------------------------------------------------------------------

::: {.section}
class coordinatingassistanttracker(object) {#symbol-coordinatingassistanttracker}
------------------------------------------

::: {.section}
coordinatingassistanttracker(\[parent\]) -\> new
coordinatingassistanttracker object.

Co-ordinating assistant tracker object tracks values and
(component,inboxname) services under names.

Keyword arguments:

-   parent \-- Optional. None, or a parent coordinatingassistanttracker
    object.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self\[, parent\])]{#symbol-coordinatingassistanttracker.__init__}
:::

::: {.section}
#### [deRegisterService(self, service)]{#symbol-coordinatingassistanttracker.deRegisterService}

Deregister a service that was previously registered.

Raises
[Axon.AxonExceptions.MultipleServiceDeletion](/Docs/Axon/Axon.AxonExceptions.MultipleServiceDeletion.html){.reference}
if the service is not/ no longer registered.
:::

::: {.section}
#### [informationItemsLogged(self)]{#symbol-coordinatingassistanttracker.informationItemsLogged}

Returns list of names values are being tracked under.
:::

::: {.section}
#### [main(self)]{#symbol-coordinatingassistanttracker.main}
:::

::: {.section}
#### [registerService(self, service, thecomponent, inbox)]{#symbol-coordinatingassistanttracker.registerService}

Register a named inbox on a component as willing to offer a service with
the specified name.

Keyword arguments:

-   service \-- the name for the service
-   thecomponent \-- the component offering the service
-   inbox \-- name of the inbox on the component

Exceptions that may be raised:

-   [Axon.AxonExceptions.ServiceAlreadyExists](/Docs/Axon/Axon.AxonExceptions.ServiceAlreadyExists.html){.reference}
-   [Axon.AxonExceptions.BadComponent](/Docs/Axon/Axon.AxonExceptions.BadComponent.html){.reference}
-   [Axon.AxonExceptions.BadInbox](/Docs/Axon/Axon.AxonExceptions.BadInbox.html){.reference}
:::

::: {.section}
#### [retrieveService(self, name)]{#symbol-coordinatingassistanttracker.retrieveService}

Retrieve the (component, inboxName) service with the specified name.
:::

::: {.section}
#### [retrieveValue(self, name)]{#symbol-coordinatingassistanttracker.retrieveValue}

Retrieve the value tracked (recorded) under the specified name.

Trying to retrieve a value under a name that isn\'t yet being tracked
results in an
[Axon.AxonExceptions.AccessToUndeclaredTrackedVariable](/Docs/Axon/Axon.AxonExceptions.AccessToUndeclaredTrackedVariable.html){.reference}
exception being raised.
:::

::: {.section}
#### [servicesRegistered(self)]{#symbol-coordinatingassistanttracker.servicesRegistered}

Returns list of names of registered services
:::

::: {.section}
#### [trackValue(self, name, value)]{#symbol-coordinatingassistanttracker.trackValue}

Track (record) the specified value under the specified name.

Once we start tracking a value, we have it\'s value forever (for now).
Trying to track the same named value more than once causes an
[Axon.AxonExceptions.NamespaceClash](/Docs/Axon/Axon.AxonExceptions.NamespaceClash.html){.reference}
exception. This is done to capture problems between interacting
components
:::

::: {.section}
#### [updateValue(self, name, value)]{#symbol-coordinatingassistanttracker.updateValue}

Update the value being tracked under the specified name with the new
value provided.

Trying to update a value under a name that isn\'t yet being tracked
results in an
[Axon.AxonExceptions.AccessToUndeclaredTrackedVariable](/Docs/Axon/Axon.AxonExceptions.AccessToUndeclaredTrackedVariable.html){.reference}
exception being raised.
:::

::: {.section}
#### [zap(self)]{#symbol-coordinatingassistanttracker.zap}
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
