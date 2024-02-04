---
pagename: Docs/Axon-old/AdaptiveCommsComponent.py
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Axon.]{style="font-size:24pt"}[AdaptiveCommsComponent.py]{style="font-size:24pt;font-weight:600"}

Version: Axon 1.0

[Pydoc Style Documentation]{style="font-size:14pt;font-weight:600"}

class AdaptiveCommsComponent(Axon.Component.component)

Method resolution order:

-   AdaptiveCommsComponent
-   Axon.Component.component
-   Axon.Microprocess.microprocess
-   Axon.Axon.AxonObject
-   \_\_builtin\_\_.object

Data and other attributes inherited from Axon.Component.component:

-   Inboxes = \[\'inbox\', \'control\'\]
-   Outboxes = \[\'outbox\', \'signal\'\]
-   Usescomponents = \[\]

Methods defined here:

[\_\_init\_\_(self)]{style="font-weight:600"}

-   \# Public Methods

[addInbox(self, \*args)]{style="font-weight:600"}

-   Adds a custom inbox with the name requested - or the closest name
    possible. (appends an integer) Returns the name of the inbox added.

[addOutbox(self, \*args)]{style="font-weight:600"}

-   Adds a custom outbox with the name requested - or the closest name
    possible. (appends an integer) Returns the name of the outbox added.

[trackResource(self, resource, inbox)]{style="font-weight:600"}

-   Tracks a \_single\_ resource associated with the inbox

[trackResourceInformation(self, resource, inboxes, outboxes,
information)]{style="font-weight:600"}

-   Provides a lookup service associating inboxes/outboxes & user
    information with a resource. Uses GIGO principle.

[retrieveTrackedResource(self, inbox)]{style="font-weight:600"}

-   Retrieves a single resource associated with the inbox

[retrieveTrackedResourceInformation(self,
resource)]{style="font-weight:600"}

-   retrieveTrackedResourceInformation(self, resource) -\>
    informationBundle ( {inboxes, outboxes,otherdata} ) (Uses GIGO
    principle.)

[ceaseTrackingResource(self, resource)]{style="font-weight:600"}

-   Stop tracking a resource and release references to it

[deleteInbox(self, name)]{style="font-weight:600"}

-   Deletes the named inbox

[deleteOutbox(self, name)]{style="font-weight:600"}

-   Deletes the named outbox

[Testdoc Documentation]{style="font-size:14pt;font-weight:600"}

[\_\_init\_\_]{style="font-weight:600"}

-   Called with no arguments is expected, results in component
    superconstructor being called. performs no local initialisation
-   Called with with arguments causes TypeError exception

[addInbox]{style="font-weight:600"}

-   adding an inbox with a completely new name results in that inbox
    being created/added
-   adding an inbox with an existing name results in an inbox being
    created/added with a similar name - same name with a suffix

[addOutbox]{style="font-weight:600"}

-   adding an outbox with a completely new name results in that outbox
    being created/added
-   adding an outbox with an existing name results in an outbox being
    created/added with a similar name - same name with a suffix

[deleteInbox]{style="font-weight:600"}

-   Deletes the named inbox
-   KeyError exception raised if you try to delete an inbox that does
    not exist - this includes the case of an already deleted Inbox

[deleteOutbox]{style="font-weight:600"}

-   Deletes the named outbox
-   KeyError exception raised if you try to delete an outbox that does
    not exist - this includes the case of an already deleted Outbox

[trackResource,retrieveTrackedResource]{style="font-weight:600"}

-   Adds to & retrieves from the mapping of inbox -\> resource to a
    local store. This allows retrieval of the resource based on which
    inbox messages arrive on. Whilst designed for custom inboxes, it
    should work with the \'default\' inboxes for a component
-   Tracking resources using a custom dynamic inbox name should work.
-   Tracking resources using an invalid inbox name should fail.

[trackResourceInformation,
retrieveTrackedResourceInformation]{style="font-weight:600"}

-   Associates communication & user aspects related to a resource.
    Associating default in/out boxes with a resource is valid
-   Associates communication & user aspects related to a resource.
    Associating dynamically created in/out boxes with a resource is the
    default
-   Tracking invalid inboxes using a resource fails.
-   Tracking invalid outboxes using a resource fails.

Michael, December 2004
