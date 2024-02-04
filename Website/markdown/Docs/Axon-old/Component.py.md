---
pagename: Docs/Axon-old/Component.py
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Axon.]{style="font-size:24pt"}[Component.py]{style="font-size:24pt;font-weight:600"}

Version: Axon 1.0

[TODO: ]{style="font-weight:600"}Document the fact that
[runBody]{style="font-family:Courier 10 Pitch"} is actually the
[main()]{style="font-family:Courier 10 Pitch"} function, and hence using
a standard generator where
[main()]{style="font-family:Courier 10 Pitch"} is, is fine.

[TODO: ]{style="font-weight:600"}Make a note that microthread is meant
as a term to mean \"active generator object\". (This was written during
python 2.2 days when generators were uncommon, hence convoluted over
explanation)

[TODO: ]{style="font-weight:600"}Generally chop down and rewrite better

A component is a microprocess with a microthread of control,
input/output queues (inboxes/ outboxes) connected by linkages to other
components, with postmen taking messages from output queues, passing
them along linkages to inboxes.

A microprocess is a class that supports parallel execution using
microthreads.

A microthread takes more explanation is a thread of control resulting
from a function of the following form:

<div>

[def]{style="font-family:Courier 10 Pitch;font-weight:600"}[
foo():]{style="font-family:Courier 10 Pitch"}

</div>

<div>

[yield]{style="font-family:Courier 10 Pitch;font-weight:600"}[ 1\
]{style="font-family:Courier 10 Pitch"}[while]{style="font-family:Courier 10 Pitch;font-weight:600"}[
1:]{style="font-family:Courier 10 Pitch"}

</div>

[bla = foo()]{style="font-family:Courier 10 Pitch"} results in bla
containing an intelligent function representing the thread of control
[inside]{style="font-weight:600"} the function - in this case inside the
while loop - that remembers where the program counter was when control
was yielded back to the caller. Repeated calls to
[bla.next()]{style="font-family:Courier 10 Pitch"} continue where you
left off.

First call to [bla()]{style="font-family:Courier 10 Pitch"} & you get
\"this\" printed. Next time you get \"that\" then \"this\" printed (when
you go back round the loop). The time after that, you get \"that\" then
\"this\" printed, and so on.

If you have 10 calls to [foo()]{style="font-family:Courier 10 Pitch"}
you end up with 10 function calls that remember where they were in
[foo()]{style="font-family:Courier 10 Pitch"}, which run for a bit and
then return control back to the caller. If you repeatedly call all of
these function calls, you essentially end up with
[foo()]{style="font-family:Courier 10 Pitch"} running 10 times in
parallel. It\'s these special \"position remembering\" functions that
get termed microthreads.

Clearly in order to have a microthread, you have to have a piece of code
capable of being called in this manner - ie it yields control back to
it\'s caller periodically - this is a what a microprocess in this
context. An object that has a \"special method\" that can be treated in
this manner.

A component puts a layer of wrapper on top of the microprocess, which
adds in input & output queues (inboxes/outboxes). To make life easier, a
component has some wrappers around the \"special function\" to make user
code less obfuscated. The life cycle for a component runs as follows:

[myComponent]{style="font-family:Courier 10 Pitch"} gets activated at
some point later.

When [myComponent]{style="font-family:Courier 10 Pitch"} is activated
the following logic happens for the runtime of
[myComponent]{style="font-family:Courier 10 Pitch"} :

<div>

[def]{style="font-family:Courier 10 Pitch;font-weight:600"}[
runComponent(someComponent):]{style="font-family:Courier 10 Pitch"}

</div>

<div>

[result = someComponent.initialiseComponent()\
]{style="font-family:Courier 10 Pitch"}[if]{style="font-family:Courier 10 Pitch;font-weight:600"}[
result:
]{style="font-family:Courier 10 Pitch"}[yield]{style="font-family:Courier 10 Pitch;font-weight:600"}[
result\
result = 1\
]{style="font-family:Courier 10 Pitch"}[while]{style="font-family:Courier 10 Pitch;font-weight:600"}[
result:]{style="font-family:Courier 10 Pitch"}

</div>

<div>

[someComponent.closeDownComponent\
]{style="font-family:Courier 10 Pitch"}[yield]{style="font-family:Courier 10 Pitch;font-weight:600"}[
result\
\# Component ceases running]{style="font-family:Courier 10 Pitch"}

</div>

Dummy methods for the methods listed here are provided, so missing these
out won\'t result in broken code. The upshot is a user component can
look like this:

<div>

[class]{style="font-family:Courier 10 Pitch;font-weight:600"}[
myComponent(component):]{style="font-family:Courier 10 Pitch"}

</div>

<div>

[count = 0\
]{style="font-family:Courier 10 Pitch"}[def]{style="font-family:Courier 10 Pitch;font-weight:600"}[
\_\_init\_\_(self,somearg):]{style="font-family:Courier 10 Pitch"}

</div>

<div>

[def]{style="font-family:Courier 10 Pitch;font-weight:600"}[
initialiseComponent(self):]{style="font-family:Courier 10 Pitch"}

</div>

<div>

[def]{style="font-family:Courier 10 Pitch;font-weight:600"}[
mainLoop(self):]{style="font-family:Courier 10 Pitch"}

</div>

<div>

[def
]{style="font-family:Courier 10 Pitch;font-weight:600"}[closeDownComponent(self):]{style="font-family:Courier 10 Pitch"}

</div>

This creates a component class which has the default input/output boxes
of \"inbox\" and \"outbox\".

[Pydoc Style Documentation]{style="font-size:14pt;font-weight:600"}

class component(Axon.Microprocess.microprocess)

Method resolution order:

-   component
-   Axon.Microprocess.microprocess
-   Axon.Axon.AxonObject
-   \_\_builtin\_\_.object

Data and other attributes defined here:

-   Inboxes = \[\'inbox\', \'control\'\]
-   Outboxes = \[\'outbox\', \'signal\'\]
-   Usescomponents = \[\]

Methods defined here:

[\_\_init\_\_(self)]{style="font-weight:600"}

-   You want to overide this method locally. You MUST call this
    superconstructor for things to work however.

[\_\_str\_\_(self)]{style="font-weight:600"}

-   Provides a useful string representation of the component. You
    probably want to override this, and append this description using
    something like:
    [component.\_\_str\_\_(self)]{style="font-family:Courier 10 Pitch"}

[addChildren(self, \*children)]{style="font-weight:600"}

-   [C.addChildren(list,of,components)]{style="font-family:Courier 10 Pitch"} -
    Register the components as children/subcomponents This takes a list
    of children components and adds them to the children list of this
    component. This is done by looping of the list and adding each one
    individually by calling addChild. addChild has a number of effects
    internally described above.

[childComponents(self)]{style="font-weight:600"}

-   [C.childComponents()]{style="font-family:Courier 10 Pitch"} - Simple
    accessor method, returns list of child components

[closeDownComponent(self)]{style="font-weight:600"}

-   Stub method. [This method is designed to be
    overridden.]{style="font-style:italic;font-weight:600"}

[dataReady(self, boxname=\'inbox\')]{style="font-weight:600"}

-   [C.dataReady(\"boxname\")]{style="font-family:Courier 10 Pitch"} -
    test, returns true if data is available in the requested inbox. Used
    by a component to check an inbox for ready data. You will want to
    call this method to periodically check whether you\'ve been sent any
    messages to deal with!\
    You are unlikely to want to override this method.

[initialiseComponent(self)]{style="font-weight:600"}

-   Stub method. [This method is designed to be
    overridden.]{style="font-style:italic;font-weight:600"}

[link(self, source, sink, passthrough=0, pipewidth=0,
synchronous=None)]{style="font-weight:600"}

-   [C.link(source,sink)]{style="font-family:Courier 10 Pitch"} - create
    linkage between a source and sink.\
    source is a tuple: (source\_component, source\_box)\
    sink is a tuple: (sink\_component, sink\_box)\
    passthrough, pipewidth and synchronous are defined as in the linkage
    class

[main(self)]{style="font-weight:600"}

-   [C.main()]{style="font-family:Courier 10 Pitch"} - [You may want to
    override this method instead of using callbacks\
    ]{style="font-style:italic;font-weight:600"}This is the function
    that gets called by microprocess. If you override this do so with
    care. If you don\'t do it properly, your
    [initialiseComponent]{style="font-family:Courier 10 Pitch"},
    [mainBody]{style="font-family:Courier 10 Pitch"} &
    [closeDownComponent]{style="font-family:Courier 10 Pitch"} parts
    will not be called. Ideally you should not NEED to override this
    method. You also should not call this method directly since activate
    does this for you in order to create a microthread of control.

[mainBody(self)]{style="font-weight:600"}

-   Stub method. [This method is designed to be
    overridden.]{style="font-style:italic;font-weight:600"}

[recv(self, boxname=\'inbox\')]{style="font-weight:600"}

-   [C.recv(\"boxname\")]{style="font-family:Courier 10 Pitch"} -
    returns the first piece of data in the requested inbox.\
    Used by a component to recieve a message from the outside world. All
    comms goes via a named box/input queue\
    You will want to call this method to actually recieve messages
    you\'ve been sent. You will want to check for new messages using
    [dataReady]{style="font-family:Courier 10 Pitch"} first though.\
    You are unlikely to want to override this method.

[removeChild(self, child)]{style="font-weight:600"}

-   [C.removeChild(component)]{style="font-family:Courier 10 Pitch"} -
    Deregister component as a child.\
    Removes the child component, and deregisters it as capable of
    recieving messages. You probably want to do this when you enter a
    closedown state of some kind for either your component, or the child
    component.\
    You will want to call this function when shutting down child
    components of your component.

[send(self, message, boxname=\'outbox\',
force=False)]{style="font-weight:600"}

-   [C.send(message,
    \"boxname\")]{style="font-family:Courier 10 Pitch"} - appends
    message to the requested outbox.\
    Used by a component to send a message to the outside world.A ll
    comms goes via a named box/output queue.\
    You will want to call this method to send messages. They are NOT
    sent immediately. They are placed in your outbox called \'boxname\',
    and are periodically collected & delivered by the postman. This is
    not guaranteed to stay the same. (ie immediate delivery may happen)\
    If the outbox is synchronised then noSpaceInBox will be raised if
    the box is full unless force is True which should only be used with
    great care.\
    You are unlikely to want to override this method.

[synchronisedSend(self, thingsToSend,
outbox=\'outbox\')]{style="font-weight:600"}

[C.synchronisedSend(list, of, things,to,
send)]{style="font-family:Courier 10 Pitch"} -\> generator for sending
the objects when space is available. Expected to be used as:

<div>

[for]{style="font-family:Courier 10 Pitch;font-weight:600"}[ i
]{style="font-family:Courier 10 Pitch"}[in]{style="font-family:Courier 10 Pitch;font-weight:600"}[
self.synchronisedSend(thingsToSend):]{style="font-family:Courier 10 Pitch"}

</div>

<div>

Largely has to be done that way due to not being able to wrap yield. See
test/SynchronousLinks\_SystemTest.py for an example

</div>

[Testdoc Documentation]{style="font-size:14pt;font-weight:600"}

[\_\_init\_\_]{style="font-weight:600"}

-   Class constructor is expected to be called without arguments.

[\_\_str\_\_]{style="font-weight:600"}

-   Returns a string representation of the component- consisting of
    Component,representation of inboxes, representation of outboxes.
-   Returns a string that contains the fact that it is a component
    object and the name of it.

[addChildren]{style="font-weight:600"}

-   All arguments are added as child components of the component.

[childComponents]{style="font-weight:600"}

-   Returns the list of children components of this component.

[closeDownComponent]{style="font-weight:600"}

-   stub method, returns 1, expected to be overridden by clients.

[dataReady]{style="font-weight:600"}

-   Returns true if the supplied inbox has data ready for processing.

[initialiseComponent]{style="font-weight:600"}

-   Stub method, returns 1, expected to be overridden by clients.

[link]{style="font-weight:600"}

-   Creates a link, handled by the component\'s postman, that links a
    source component to it\'s sink, honouring passthrough, pipewidth and
    synchronous attributes.

[main]{style="font-weight:600"}

-   Returns a generator that implements the documented behaviour of a
    highly simplistic approach component statemachine.
-   This ensures that the closeDownComponent method is called at the end
    of the loop. It also repeats the above test.

[mainBody]{style="font-weight:600"}

-   stub method, returns None, expected to be overridden by clients as
    the main loop.

[recv]{style="font-weight:600"}

-   Takes the first item available off the specified inbox, and returns
    it.

[removeChild]{style="font-weight:600"}

-   Removes the specified component from the set of child components and
    deregisters it from the postoffice.

[send]{style="font-weight:600"}

-   Takes the message and places it into the specified outbox, throws an
    exception if there is no space in a synchronous outbox.
-   Takes the message and places it into the specified outbox, throws an
    exception if there is no space in a synchronous outbox.

[synchronisedBox]{style="font-weight:600"}

-   Called with no arguments sets the outbox \'outbox\' to being a
    synchronised box, with a maximum depth of 1.

[synchronisedSend]{style="font-weight:600"}

-   Takes a list of things to send, and returns a generator that when
    repeatedly called tries to send data over a synchronised outbox.

[\_activityCreator]{style="font-weight:600"}

-   Always returns true. Components are microprocesses instantiated by
    users typically - thus they are creators of activity, not slaves to
    it. Internal function.

[\_closeDownMicroprocess]{style="font-weight:600"}

-   Checks the shutdownMicroprocess message for the scheduler contains a
    reference to the postoffice associated with the component.
-   Returns a shutdownMicroprocess. Internal Function.

[\_collect]{style="font-weight:600"}

-   Takes the first piece of data in an outbox and returns it. Raises
    IndexError if empty. Internal function.

[\_collectInbox]{style="font-weight:600"}

-   Tests with default args. All these deliveries should suceed.
    Internal Function.
-   Tests with default args. Should raise IndexError as the box should
    be empty in this test. Internal Function.
-   Tests with inbox arg. Should raise IndexError as the box should be
    empty in this test. Internal Function.
-   Tests with inbox arg. Tests collection. Internal Function.

[\_deliver]{style="font-weight:600"}

-   Appends the given message to the given inbox. Internal Function.
-   Checks delivery to a synchronised inbox fails when it is full using
    the force method.
-   Checks delivery to a synchronised inbox fails when it is full.
    \<br\>

[\_passThroughDeliverIn]{style="font-weight:600"}

-   Appends the given message to the given inbox. Internal Function.
-   Should throw noSpaceInBox if a synchronised box is full.
-   When force is passed as true the box can be overfilled.

[\_passThroughDeliverOut]{style="font-weight:600"}

-   Appends the given message to the given outbox. Internal Function.
-   Checks delivery is limited to the pipewidth.
-   Checks delivery is limited to the pipewidth.

[\_passThroughDeliverOut\_Sync]{style="font-weight:600"}

-   Appends messages to given outbox. Should throw noSpaceInBox when
    full.

[\_safeCollect]{style="font-weight:600"}

-   Wrapper around \_collect - returns None where an IndexError would
    normally be thrown. Internal Function.

[\_\_addChild]{style="font-weight:600"}

-   Registers the component as a child of the component. Internal
    function. ttbw

Michael, December 2004
