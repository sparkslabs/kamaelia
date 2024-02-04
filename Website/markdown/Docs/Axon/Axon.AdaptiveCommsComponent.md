---
pagename: Docs/Axon/Axon.AdaptiveCommsComponent
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.html){.reference}
--------------------------------------------------------------------------------------------------------------------------
:::
:::

::: {.section}
\"Adaptive Comms Components\" - can add and remove inboxes and outboxes
=======================================================================

::: {.container}
-   **class
    [AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}**
-   **class
    [\_AdaptiveCommsable](/Docs/Axon/Axon.AdaptiveCommsComponent._AdaptiveCommsable.html){.reference}**
:::

-   [Adding and removing inboxes and outboxes](#61){.reference}
-   [Tracking resources](#62){.reference}
-   [Implementation](#63){.reference}
-   [Test documentation](#64){.reference}
:::

::: {.section}
An AdaptiveCommsComponent is just like an ordinary component but with
the ability to create and destroy extra inboxes and outboxes whilst it
is running.

-   An AdaptiveCommsComponent is based on an
    [Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}

There are other variants on the basic component:

-   [Axon.ThreadedComponent.threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference}
-   [Axon.ThreadedComponent.threadedadaptivecommscomponent](/Docs/Axon/Axon.ThreadedComponent.threadedadaptivecommscomponent.html){.reference}

If your component needs to block - eg. wait on a system call; then make
it a \'threaded\' component. If it needs to change what inboxes or
outboxes it has at runtime, then make it an \'adaptive\' component.
Otherwise, simply make it an ordinary component!

::: {.section}
[Adding and removing inboxes and outboxes]{#adding-and-removing-inboxes-and-outboxes} {#61}
-------------------------------------------------------------------------------------

To add a new inbox or outbox call self.addInbox() or self.addOutbox()
specifying a base name for the inbox/outbox. The created inbox or outbox
is immediately ready to be used.:

``` {.literal-block}
actualInboxName = self.addInbox("inputData")
actualOutboxName = self.addOutbox("outputData")
```

You specify a name you would ideally like the inbox or outbox to be
given. If that name is already taken then a variant of it will be
generated. Calls to addInbox() and addOutbox() therefore return the
actual name the inbox or outbox was given. You should always use this
returned name. It is unwise to assume your ideal choice of name has been
allocated!

To remove a box, call self.deleteInbox() or self.deleteOutbox()
specifying the name of the box to be deleted:

``` {.literal-block}
self.deleteInbox(actualInboxName)
self.deleteOutbox(actualOutboxName)
```

When deleting an inbox or outbox, try to make sure that any linkages
involving that inbox/outbox have been destroyed. This includes not only
linkages created by your component, but any created by other components
too.
:::

::: {.section}
[Tracking resources]{#tracking-resources} {#62}
-----------------------------------------

adaptivecommscomponent also includes an ability to track associations
between resources and inboxes, outboxes and other information.

For example, you might want to associate another component (that your
component is interacting with) with the set of inboxes, outboxes and any
other info that are being used to communicate with it.

You can also associate particular inboxes or outboxes with those
resources. This therefore allows you to map both ways: \"which resource
relates to this inbox?\" and \"which inboxes relate to this resource?\"

For example, suppose a request leads to your component creating an inbox
and outbox to deal with another component. You might store these as a
tracked resource, along with other information, such as the \'other\'
component and any state or linkages that were created; and associate
this resource with the inbox from which data might arrive:

``` {.literal-block}
def wireUpToOtherComponent(self, theComponent):
    newIn  = self.addInbox("commsIn")
    newOut = self.addOutbox("commsOut")

    newState = "WAITING"
    inLinkage  = self.link((theComponent,itsOutbox),(self,newIn))
    outLinkage = self.link((theComponent,itsInbox), (self,newOut))

    resource = theComponent

    inboxes = [newIn]
    outboxes = [newOut]
    info = (newState, inLinkage, outLinkage)
    self.trackResourceInformation(resource, inboxes, outboxes, info)

    self.trackResource(resource, newIn)
```

If a message then arrives at that inbox, we can easily look up all the
information we might need know where it came from and how to handle it:

``` {.literal-block}
def handleMessageArrived(self, inboxName):
    msg = self.recv(inboxName)

    resource = self.retrieveResource(inboxName)
    inboxes, outboxes, info = self.retrieveResourceInformation(resource)
    theComponent=resource

    ...
```

When you are finished with a resource and its associated information you
can clean it up with the ceaseTrackingResource() method which removes
the association between the resource and information. For example when
you get rid of a set of linkages and inboxes or outboxes associated with
another component you might want to clean up the resource you were using
to track this too:

``` {.literal-block}
def doneWithComponent(self, theComponent):
    resource=theComponent
    inboxes, outboxes, info = self.retrieveResourceInformation(resource)

    for name in inboxes:
        self.deleteInbox(name)
    for name in outboxes:
        self.deleteOutbox(name)

    state,linkages = info[0], info[1:]
    for linkage in linkages:
        self.unlink(thelinkage=linkage)

    self.ceaseTrackingResource(resource)
```
:::

::: {.section}
[Implementation]{#implementation} {#63}
---------------------------------

AdaptiveCommsComponent\'s functionality above and beyond the ordinary
[Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}
is implemented in a separate mixin class \_AdaptiveCommsable. This
enables it to be reused for other variants on the basic component that
need to inherit this functionality - such as the
threadedadaptivecommscomponent.

When adding new inboxes or outboxes, name clashes are resolved by
permuting the box name with a suffixed unique ID number until there is
no longer any clash.
:::

Test documentation {#64}
==================

Tests passed:

-   -Acceptance Test - Check Addition and Deletion of Inboxes
-   -Acceptance Test - Check Addition and Deletion of Outboxes
-   \_\_init\_\_ - Called with with arguments does not cause problems
-   \_\_init\_\_ - Called with no arguments is expected, results in
    component superconstructor being called. performs no local
    initialisation
-   addInbox - adding an inbox with an existing name results in an inbox
    being created/added with a similar name - same name with a suffix
-   addInbox - adding an inbox with a completely new name results in
    that inbox being created/added
-   addOutbox - adding an outbox with an existing name results in an
    outbox being created/added with a similar name - same name with a
    suffix
-   addOutbox - adding an outbox with a completely new name results in
    that outbox being created/added
-   deleteInbox - KeyError exception raised if you try to delete an
    inbox that does not exist - this includes the case of an already
    deleted Inbox
-   deleteInbox - Deletes the named inbox
-   deleteOutbox - KeyError exception raised if you try to delete an
    outbox that does not exist - this includes the case of an already
    deleted Outbox
-   deleteOutbox - Deletes the named outbox
-   trackResourceInformation, retrieveTrackedResourceInformation -
    Tracking invalid inboxes using a resource fails.
-   trackResourceInformation, retrieveTrackedResourceInformation -
    Tracking invalid outboxes using a resource fails.
-   trackResourceInformation, retrieveTrackedResourceInformation -
    Associates communication & user aspects related to a resource.
    Associating default in/out boxes with a resource is valid
-   trackResourceInformation, retrieveTrackedResourceInformation -
    Associates communication & user aspects related to a resource.
    Associating dynamically created in/out boxes with a resource is the
    default
-   trackResource,retrieveTrackedResource - Tracking resources using an
    invalid inbox name should fail.
-   trackResource,retrieveTrackedResource - Adds to & retrieves from the
    mapping of inbox -\> resource to a local store. This allows
    retrieval of the resource based on which inbox messages arrive on.
    Whilst designed for custom inboxes, it should work with the
    \'default\' inboxes for a component
-   trackResource,retrieveTrackedResource - Tracking resources using a
    custom dynamic inbox name should work.
:::

------------------------------------------------------------------------

::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.html){.reference}.[AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}
===================================================================================================================================================================================================================================

::: {.section}
class AdaptiveCommsComponent([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}, \_AdaptiveCommsable) {#symbol-AdaptiveCommsComponent}
-----------------------------------------------------------------------------------------------------------------------------------

::: {.section}
Base class for a component that works just like an ordinary component
but can also \'adapt\' its comms by adding or removing inboxes and
outboxes whilst it is running.

Subclass to make your own.

See
[Axon.AdaptiveCommsComponent.\_AdaptiveCommsable](/Docs/Axon/Axon.AdaptiveCommsComponent._AdaptiveCommsable.html){.reference}
for the extra methods that this subclass of component has.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, \*args, \*\*argd)]{#symbol-AdaptiveCommsComponent.__init__}
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference} :

-   [mainBody](/Docs/Axon/Axon.Component.html#symbol-component.mainBody){.reference}(self)
-   [\_\_str\_\_](/Docs/Axon/Axon.Component.html#symbol-component.__str__){.reference}(self)
-   [childComponents](/Docs/Axon/Axon.Component.html#symbol-component.childComponents){.reference}(self)
-   [setInboxSize](/Docs/Axon/Axon.Component.html#symbol-component.setInboxSize){.reference}(self,
    boxname, size)
-   [send](/Docs/Axon/Axon.Component.html#symbol-component.send){.reference}(self,
    message\[, boxname\])
-   [main](/Docs/Axon/Axon.Component.html#symbol-component.main){.reference}(self)
-   [dataReady](/Docs/Axon/Axon.Component.html#symbol-component.dataReady){.reference}(self\[,
    boxname\])
-   [initialiseComponent](/Docs/Axon/Axon.Component.html#symbol-component.initialiseComponent){.reference}(self)
-   [anyReady](/Docs/Axon/Axon.Component.html#symbol-component.anyReady){.reference}(self)
-   [\_\_addChild](/Docs/Axon/Axon.Component.html#symbol-component.__addChild){.reference}(self,
    child)
-   [closeDownComponent](/Docs/Axon/Axon.Component.html#symbol-component.closeDownComponent){.reference}(self)
-   [\_closeDownMicroprocess](/Docs/Axon/Axon.Component.html#symbol-component._closeDownMicroprocess){.reference}(self)
-   [link](/Docs/Axon/Axon.Component.html#symbol-component.link){.reference}(self,
    source, sink, \*optionalargs, \*\*kwoptionalargs)
-   [unlink](/Docs/Axon/Axon.Component.html#symbol-component.unlink){.reference}(self\[,
    thecomponent\]\[, thelinkage\])
-   [recv](/Docs/Axon/Axon.Component.html#symbol-component.recv){.reference}(self\[,
    boxname\])
-   [\_deliver](/Docs/Axon/Axon.Component.html#symbol-component._deliver){.reference}(self,
    message\[, boxname\])
-   [removeChild](/Docs/Axon/Axon.Component.html#symbol-component.removeChild){.reference}(self,
    child)
-   [Inbox](/Docs/Axon/Axon.Component.html#symbol-component.Inbox){.reference}(self\[,
    boxname\])
-   [addChildren](/Docs/Axon/Axon.Component.html#symbol-component.addChildren){.reference}(self,
    \*children)
:::

::: {.section}
#### Methods inherited from [Axon.Microprocess.microprocess](/Docs/Axon/Axon.Microprocess.microprocess.html){.reference} :

-   [pause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.pause){.reference}(self)
-   [\_unpause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._unpause){.reference}(self)
-   [\_microprocessGenerator](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._microprocessGenerator){.reference}(self,
    someobject\[, mainmethod\])
-   [\_isStopped](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._isStopped){.reference}(self)
-   [stop](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.stop){.reference}(self)
-   [next](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.next){.reference}(self)
-   [activate](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.activate){.reference}(self\[,
    Scheduler\]\[, Tracker\]\[, mainmethod\])
-   [unpause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.unpause){.reference}(self)
-   [run](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.run){.reference}(self)
-   [\_isRunnable](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._isRunnable){.reference}(self)
:::

::: {.section}
#### Methods inherited from [Axon.AdaptiveCommsComponent.\_AdaptiveCommsable](/Docs/Axon/Axon.AdaptiveCommsComponent._AdaptiveCommsable.html){.reference} :

-   [retrieveTrackedResource](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.retrieveTrackedResource){.reference}(self,
    inbox)
-   [deleteOutbox](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.deleteOutbox){.reference}(self,
    name)
-   [\_newOutboxName](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable._newOutboxName){.reference}(self\[,
    name\])
-   [ceaseTrackingResource](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.ceaseTrackingResource){.reference}(self,
    resource)
-   [addInbox](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.addInbox){.reference}(self,
    \*args)
-   [trackResource](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.trackResource){.reference}(self,
    resource, inbox)
-   [retrieveTrackedResourceInformation](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.retrieveTrackedResourceInformation){.reference}(self,
    resource)
-   [deleteInbox](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.deleteInbox){.reference}(self,
    name)
-   [\_newInboxName](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable._newInboxName){.reference}(self\[,
    name\])
-   [trackResourceInformation](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.trackResourceInformation){.reference}(self,
    resource, inboxes, outboxes, information)
-   [addOutbox](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.addOutbox){.reference}(self,
    \*args)
:::
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.html){.reference}.[\_AdaptiveCommsable](/Docs/Axon/Axon.AdaptiveCommsComponent._AdaptiveCommsable.html){.reference}
============================================================================================================================================================================================================================

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
