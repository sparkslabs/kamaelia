---
pagename: Docs/Axon-old/Postman.py
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Axon.]{style="font-size:24pt"}[Postman.py]{style="font-size:24pt;font-weight:600"}

Version: Axon 1.0

[TODO: ]{style="font-weight:600"}Until deprecation, ensure test suite
doc strings accurately detail behaviour. (deregister springs to mind as
a poor example.)

A postman is a microprocess that knows about linkages, and components,
and hence runs concurrently to your components. It can have a number of
components & linkages registered with it.

Periodically it checks the sources of the linkages it knows about for
messages. If it finds some messages it checks where to deliver them to
by looking at the sink of the linkage. Assuming it finds a destination
to deliver to, the postmans then delivers the messages to the inbox of
the assigned destination component.

The Postman microprocess handles message delivery along linkages between
inboxes and outboxes, usually contained in components. There is one
postman per component.

Since a postman is a microprocess it runs in parallel with the
components it\'s delivering messages between.

[It is highly possible this could result in a race hazard if message
queues can grow faster than the postman can deliver them. As a result
the system provides Synchronised Boxes as well which have a maximum,
enforced capacity which works to prevent this issue - at the expense of
extra logic in the client]{style="font-style:italic"}

A Postman can have a debug name - this is to help differentiate between
postmen who are delivering things versus those that aren\'t if problems
arise.

[Pydoc Style Documentation]{style="font-size:14pt;font-weight:600"}

class postman(Axon.Microprocess.microprocess)

[\_\_init\_\_(self, debugname=\'\')]{style="font-weight:600"}

Constructor. If a debug name is assigned this will be stored as a
debugname attribute. Other attributes:

-   linkages = list of linkages this postman needs to know about
-   things = dict of things this postman has to monitor outboxes on. the
    index into the dict is the name of the thing monitored, with the
    value being the thing.
-   reverse things = this provides a reverse lookup of things - the
    index being the id of the component, the value being the name of the
    component.

<div>

The super class\'s constructor is then called to make this a fully
initialised microprocess.

</div>

<div>

</div>

[\_\_str\_\_(self)]{style="font-weight:600"}

[deregister(self, name=None, component=None)]{style="font-weight:600"}

-   This deregisters a component from this postman, deleting the
    reference to the component object. If the reference isn\'t deleted,
    the reference count of the object will never reach zero and never be
    garbage collected.

[deregisterlinkage(self, thecomponent=None,
thelinkage=None)]{style="font-weight:600"}

-   De registers a linkage, based on a provided component. Does not yet
    de-register based on a user supplied linkage. Simply loops through
    the linkages, looking for the component being de-registered, and
    de-registers (deletes) any linkages with that component referenced
    inside.

[domessagedelivery(self)]{style="font-weight:600"}

-   Performs the actual message delivery activity. Loops through the
    \*linkages\*, scanning their sources, collects messages for delivery
    to the sinkwbox of the recipient.

[islinkageregistered(self, linkage)]{style="font-weight:600"}

-   Returns a true value if the linkage given is registered with the
    postman.

[main(self)]{style="font-weight:600"}

[register(self, name, component)]{style="font-weight:600"}

-   Registers a \_named\_ component with the postman. These are stored
    in forward & reverse lookup tables.

[registerlinkage(self, thelinkage)]{style="font-weight:600"}

-   Registers a linkage with the postman. It\'s likely this is actually
    more useful, looking back on this design, since we only deliver
    things along linkages. (no defaults)

[showqueuelengths(self)]{style="font-weight:600"}

-   Debugging function really. Takes the debug name of this postman, and
    appends a textual description of the queue lengths of the inboxes
    and outboxes of all the components this postman takes from/delivers
    to. Result is a string, does NOT send output to any output stream.
    (Did originally, hence \"show\", is likely to be renamed slightly.)

[Testdoc Documentation]{style="font-size:14pt;font-weight:600"}

[\_\_init\_\_]{style="font-weight:600"}

-   Called with a debugname which will be stored with \":debug \"
    appended
-   Called with no arguments. This is the normal case. \<br\>

[\_\_str\_\_]{style="font-weight:600"}

-   Checks the formatted string is of the correct format. \<br\>

[deregister]{style="font-weight:600"}

-   Deregisters a component from the postman by name
-   Deregisters a component from the postman by name
-   Deregisters a component from the postman by name
-   Deregisters a component from the postman by name
-   Deregisters a component from the postman by name
-   Deregisters a component from the postman by name
-   Deregisters a component from the postman by name and component

[deregisterlinkage]{style="font-weight:600"}

-   Tests for a deadlock when a postman deregisters a linkage whose sink
    is limited in size and full
-   Tests for a deadlock when a postman deregisters linkages of a
    component whose sink is limited in size and full

[domessagedelivery]{style="font-weight:600"}

-   Checks that linkages with data to move have moveData called. See the
    AdvancedMockLinkage classes for details.
-   Tests for stability when there are no linkages registered.

[register]{style="font-weight:600"}

-   Registers a component with the postman.

[registerlinkage]{style="font-weight:600"}

-   Registers a linkage with the Postman

\...

Michael, December 2004
