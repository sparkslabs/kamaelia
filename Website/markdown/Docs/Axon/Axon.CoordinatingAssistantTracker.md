---
pagename: Docs/Axon/Axon.CoordinatingAssistantTracker
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[CoordinatingAssistantTracker](/Docs/Axon/Axon.CoordinatingAssistantTracker.html){.reference}
--------------------------------------------------------------------------------------------------------------------------------------
:::
:::

::: {.section}
Co-ordinating Assistant Tracker
===============================

::: {.container}
-   **class
    [coordinatingassistanttracker](/Docs/Axon/Axon.CoordinatingAssistantTracker.coordinatingassistanttracker.html){.reference}**
:::

-   [Accessing the Co-ordinating Assistant Tracker](#88){.reference}
-   [Services](#89){.reference}
-   [Tracking global statistics](#90){.reference}
-   [Hierarchy of co-ordinating assistant trackers](#91){.reference}
-   [Test documentation](#92){.reference}
:::

::: {.section}
The co-ordinating assistant tracker is designed to allow components to
register services and statistics they wish to make public to the rest of
the system. Components can also query the co-ordinating assistant
tracker to create linkages to specific services, and for specific global
statistics.

-   A co-ordinating assistant tracker is shared between several/all
    components
-   Components can register an inbox as a service with a name
-   Components can retrieve a service by its name

::: {.section}
[Accessing the Co-ordinating Assistant Tracker]{#accessing-the-co-ordinating-assistant-tracker} {#88}
-----------------------------------------------------------------------------------------------

Co-ordinating assistant trackers are designed to work in a singleton
manner; accessible via a local or class interface (though this is not
enforced).

The simplest way to obtain the global co-ordinating assistant tracker is
via the getcat() class (static) method:

``` {.literal-block}
from Axon.CoordinatingAssistantTracker import coordinatingassistanttracker

theCAT = coordinatingassistanttracker.getcat()
```

The first time this method is called, the co-ordinating assistant
tracker is created. Subsequent calls, wherever they are made from,
return that same instance.
:::

::: {.section}
[Services]{#services} {#89}
---------------------

Components can register a named inbox on a component as a named service.
This provides a way for a component to provide a service for other
components - an inbox that another component can look up and create a
linkage to.

Registering a service is simple:

``` {.literal-block}
theComponent = MyComponentProvidingServiceOnItsInbox()
theComponent.activate()

theCAT = coordinatingassistanttracker.getcat()
theCAT.registerService("MY_SERVICE", theComponent, "inbox")
```

Another component can then retrieve the service:

``` {.literal-block}
theCAT = coordinatingassistanttracker.getcat()
(comp, inboxname) = theCAT.retrieveService("MY_SERVICE")
```

Because services are run by components - these by definition die and so
also need to be de-registered:

``` {.literal-block}
theCAT = coordinatingassistanttracker.getcat()
theCAT.deRegisterService("MY_SERVICE")
```
:::

::: {.section}
[Tracking global statistics]{#tracking-global-statistics} {#90}
---------------------------------------------------------

Microprocesses can also use the co-ordinating assistant tracker to
log/retrieve statistics/information.

Use the trackValue() method to initially start tracking a value under a
given name:

``` {.literal-block}
value = ...

theCAT = coordinatingassistanttracker.getcat()
theCAT.trackValue("MY_VALUE", value)
```

This can then be easily retrieved:

``` {.literal-block}
theCAT = coordinatingassistanttracker.getcat()
value= theCAT.retrieveValue("MY_VALUE")
```

Call the updateValue() method (not the trackValue() method) to update
the value being tracked:

``` {.literal-block}
newvalue = ...

theCAT = coordinatingassistanttracker.getcat()
theCAT.updateValue("MY_VALUE", newvalue)
```
:::

::: {.section}
[Hierarchy of co-ordinating assistant trackers]{#hierarchy-of-co-ordinating-assistant-trackers} {#91}
-----------------------------------------------------------------------------------------------

Although at initialisation a parent co-ordinating assistant tracker can
be specified; this is not currently used.
:::

Test documentation {#92}
==================

Tests passed:

-   \_\_init\_\_ - Trying to set a anything other than a coordinated
    assistant tracker as the parent causes a BadParentTracker exception
-   \_\_init\_\_ - Called with no arguments should succeed.
-   \_\_init\_\_ - Called with a single argument results in it being the
    parent for the tracker
-   deRegisterService - allows a component to remove their service from
    being public
-   deRegisterService - deleting a non-existant service raises
    MultipleServiceDeletion exception
-   informationItemsLogged - returns the names of pieces of information
    logged with this tracker
-   registerService - adds the named component/inbox to the list of
    named registered services
-   registerService - adding a duplicate service fails, even with same
    arguments
-   registerService - adding a service but not to as a component fails-
    raises BadComponent assertion
-   registerService - adding a service but to a bad/nonexistant inbox
    fails - raises BadInbox assertion
-   retrieveService - Retrieving a tracked service should return the
    component/inbox pair we supplied under a specific name
-   retrieveService - Attempting to retrieve a non-tracked service
    results in KeyError exception being thrown
-   retrieveValue - Retrieving a tracked value should return the value
    we asked to be tracked
-   retrieveValue - attempting to retrieve a value we\'re not tracking
    should raise AccessToUndeclaredTrackedVariable
-   trackValue - Adding a value to be tracked twice raises
    NamespaceClash
-   trackValue - Adds the name/value pair to the set of info items
    logged
-   updateValue - Updating a value should result in the value stored
    being updated
-   updateValue - Updating a value not declared as tracked should raise
    AccessToUndeclaredTrackedVariable
:::

------------------------------------------------------------------------

::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[CoordinatingAssistantTracker](/Docs/Axon/Axon.CoordinatingAssistantTracker.html){.reference}.[coordinatingassistanttracker](/Docs/Axon/Axon.CoordinatingAssistantTracker.coordinatingassistanttracker.html){.reference}
=================================================================================================================================================================================================================================================================

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
