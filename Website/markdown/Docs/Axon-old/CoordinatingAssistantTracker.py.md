---
pagename: Docs/Axon-old/CoordinatingAssistantTracker.py
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Axon.]{style="font-size:24pt"}[CoordinatingAssistantTracker.py]{style="font-size:24pt;font-weight:600"}

Version: Axon 1.0

The co-ordinating assistant tracker is designed to allow components to
register services and statistics they wish to make public to the rest of
the system. Components can also query the co-ordinating assistant
tracker to create linkages to specific services, and for specific global
statistics.

Microprocesses can also use the co-ordinating assistant tracker to
log/retrieve statistics/information. Co-ordinating assistant trackers
are designed to work in a singleton manner accessible via a local or
class interface.This singleton nature of the co-ordinatin assistant
tracker is not enforced.

[Pydoc Style Documentation]{style="font-size:14pt;font-weight:600"}

class coordinatingassistanttracker(\_\_builtin\_\_.object)

Methods defined here:

[\_\_init\_\_(self, parent=None)]{style="font-weight:600"}

[deRegisterService(self, service)]{style="font-weight:600"}

-   Services are run by components - these by definition die and need to
    be de-registered

[informationItemsLogged(self)]{style="font-weight:600"}

[main(self)]{style="font-weight:600"}

[registerService(self, service, thecomponent,
inbox)]{style="font-weight:600"}

-   [t.registerService(\'service\',component,inbox)]{style="font-family:Courier 10 Pitch"} -
    Registers that a component is willing to offer a service over a
    specific inbox

[retrieveService(self, name)]{style="font-weight:600"}

[retrieveValue(self, name)]{style="font-weight:600"}

[servicesRegistered(self)]{style="font-weight:600"}

-   Returns list of names of registered services

[trackValue(self, name, value)]{style="font-weight:600"}

-   Once we start tracking a value, we have it\'s value forever (for
    now). Adding the same named value more than once causes a
    NamespaceClash to capture problems between interacting components

[updateValue(self, name, value)]{style="font-weight:600"}

\...

[Testdoc Documentation]{style="font-size:14pt;font-weight:600"}

[\_\_init\_\_]{style="font-weight:600"}

-   Called with a single argument results in it being the parent for the
    tracker
-   Called with no arguments should succeed.
-   Trying to set a anything other than a coordinated assistant tracker
    as the parent causes a
    [BadParentTracker]{style="font-family:Courier 10 Pitch"} exception

[informationItemsLogged]{style="font-weight:600"}

-   returns the names of pieces of information logged with this tracker

[registerService]{style="font-weight:600"}

-   adding a duplicate service fails, even with same arguments
-   adding a service but not to as a component fails - raises
    [BadComponent]{style="font-family:Courier 10 Pitch"} assertion
-   adding a service but to a bad/nonexistant inbox fails - raises
    [BadInbox]{style="font-family:Courier 10 Pitch"} assertion
-   adds the named component/inbox to the list of named registered
    services

[retrieveService]{style="font-weight:600"}

-   Attempting to retrieve a non-tracked service results in
    [KeyError]{style="font-family:Courier 10 Pitch"} exception being
    thrown
-   Retrieving a tracked service should return the component/inbox pair
    we supplied under a specific name

[deRegisterService]{style="font-weight:600"}

-   allows a component to remove their service from being public
-   deleting a non-existant service raises
    [MultipleServiceDeletion]{style="font-family:Courier 10 Pitch"}
    exception

[trackValue]{style="font-weight:600"}

-   Adding a value to be tracked twice raises
    [NamespaceClash]{style="font-family:Courier 10 Pitch"}
-   Adds the name/value pair to the set of info items logged

[updateValue]{style="font-weight:600"}

-   Updating a value not declared as tracked should raise
    [AccessToUndeclaredTrackedVariable]{style="font-family:Courier 10 Pitch"}
-   Updating a value should result in the value stored being updated

[retrieveValue]{style="font-weight:600"}

-   Retrieving a tracked value should return the value we asked to be
    tracked
-   attempting to retrieve a value we\'re not tracking should raise
    [AccessToUndeclaredTrackedVariable]{style="font-family:Courier 10 Pitch"}

[Class methods defined here:]{style="font-weight:600"}

-   getcat(cls) from \_\_builtin\_\_.type

Michael, December 2004
