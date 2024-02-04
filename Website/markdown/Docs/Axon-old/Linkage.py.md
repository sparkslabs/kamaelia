---
pagename: Docs/Axon-old/Linkage.py
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Axon.]{style="font-size:24pt"}[Linkage.py]{style="font-size:24pt;font-weight:600"}

Version: Axon 1.0

[TODO:]{style="font-weight:600"} test suite doesn\'t emit API docs quite
right

Components only have input & output boxes. For data to get from a
producer (eg a file reader) to a consumer (eg an encryption component)
then the output of one component, the source component, must be linked
to the input of another component, the sink component.

These need to be registered with a postman (see below) who takes
messages from the outputs and delivers them to the appropriate
destination. This is NOT the usual technique for software messaging.
Normally you create messages, addressed to something specific, and then
the message handler delivers them.

However the method of communication used here is the norm for
\_hardware\_ systems, and generally results in very pluggable components
- the aim of this system, hence this design approach rather than the
normal. This method of communication is also the norm for one form of
software system - unix shell scripting - something that has shown itself
time and again to be used in ways the inventors of programs/components
never envisioned.

[Pydoc Style Documentation]{style="font-size:14pt;font-weight:600"}

class linkage(Axon.Axon.AxonObject)

Linkage - Since components can only talk to local interfaces, this
defines the linkages between inputs and outputs of a component. At
present no argument is really optional.

Methods defined here:

[\_\_init\_\_(self, source, sink, sourcebox=\'outbox\',
sinkbox=\'inbox\', postoffice=None, passthrough=0, pipewidth=0,
synchronous=None)]{style="font-weight:600"}

-   This needs to tag the source/sink boxes as synchronous, to get
    component to go \"BANG\" if writing to a blocked

[\_\_str\_\_(self)]{style="font-weight:600"}

[dataToMove(self)]{style="font-weight:600"}

[moveData(self, force=False)]{style="font-weight:600"}

[moveDataWithCheck(self)]{style="font-weight:600"}

[setShowTransit(self, showtransit)]{style="font-weight:600"}

[setSynchronous(self, pipewidth=None)]{style="font-weight:600"}

[sinkPair(self)]{style="font-weight:600"}

[sourcePair(self)]{style="font-weight:600"}

[Testdoc Documentation]{style="font-size:14pt;font-weight:600"}

[\_\_init\_\_]{style="font-weight:600"}

-   Called with no arguments fails - raises TypeError - must supply
    source & sink components\...
-   Called with source & sink components forms a non-synchronous,
    non-passthrough linkage between the source component\'s outbox to
    the sink component\'s inbox not registered with any postman\...
-   Providing a pipewidth and synchronous flag set to false is an error.
    Raises an exception.
-   Providing a pipewidth automatically changes the source/sink boxes to
    being synchronised - with a maximum number of items in transit.
    (Clearly just stored by the object during initialisation). ttbw
-   The synchronous flag is stored to note whether the linkage limits
    deliveries based on whether the recipient (sink) box has space to
    recieve data. Source & Sink boxes are changed to be synchronous if
    they were not originally defined to be so. ttbw
-   When created with a defined postoffice/postman, the linkage
    registers itself with that postman.
-   called with both source/sink in/outboxes in addition to min-args
    forms a linkage between the specified source/sink boxes.
-   called with passthrough set to 0 results in a standard
    non-passthrough outbox to inbox linkage.
-   called with passthrough set to 1 means the source and sink boxes are
    both inboxes. This means the linkage is passthrough-inbound
    (normally from the inbox of a wrapper component to the inbox of a
    worker/sub-component).
-   called with passthrough set to 2 means the source and sink boxes are
    both outboxes. This means the linkage is passthrough-outbound
    (normally from the outbox of a worker/sub-component to the outbox of
    a wrapper component ). ttbw

[\_\_str\_\_]{style="font-weight:600"}

-   Returns a string that indicates the link source and sink components
    and boxes. Precise formatting is checked.

[dataToMove]{style="font-weight:600"}

-   Checks whether the source has any data available on it that needs
    moving to the sink.
-   Checks whether the source has any data available on it that needs
    moving to the sink. Passthrough inbox-\>inbox test.
-   Checks whether the source outbox has any data available on it. This
    works on normal linkages.

[moveData]{style="font-weight:600"}

-   .
-   .
-   Moves data from source to sink. Forces despite full pipe.
-   Moves data from source to sink. Forces move despite pipewidth.
-   Moves data from source to sink. One item is moved if there is room
    in the sink box. IndexError is thrown if source box is empty so
    check with dataToMove before calling unless you know there is an
    item available.
-   Moves data from source to sink. One item is moved if there is room
    in the sink box. IndexError is thrown if source box is empty so
    check with dataToMove before calling unless you know there is an
    item available.
-   Moves data from source to sink. One item is moved if there is room
    in the sink box. noSpaceInBox is thrown if \_deliver is called and
    source box is full.
-   Moves data from source to sink. One item is moved if there is room
    in the sink box. noSpaceInBox is thrown if source box is full.

[setSynchronous]{style="font-weight:600"}

-   Makes a linkage synchronous with its current pipewidth, will default
    to 1. Calls \_synchronised Box on each component so that the boxes
    are setup correctly.
-   Makes a linkage synchronous with its the argument as the pipewidth.

Michael, December 2004
