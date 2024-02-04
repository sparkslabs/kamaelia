---
pagename: MiniAxon/Postman
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[5[]{#Postman} Postman - A Microprocess that performs
deliveries!]{style="font-size:11pt;font-weight:600"}

Given we have outboxes and inboxes, it makes sense to have something
that can handle deliveries between the two. For the purpose of this
exercise, we\'ll create a microprocess that can look at a single outbox
for a single component, take any messages deposited there and pass them
the an inbox of another component. In terms of the component
implementation so far we can use
[dataReady]{style="font-family:Courier;font-weight:600"} to check for
availability of messages,
[recv]{style="font-family:Courier;font-weight:600"} to collect the
message from the outbox, and
[send]{style="font-family:Courier;font-weight:600"} to deliver the
message to the recipient inbox.

[Exercise: ]{style="font-weight:600"} Write a class called
[postman]{style="font-family:Courier;font-weight:600"} that subclasses
[microprocess]{style="font-family:Courier"} with the following\...

Attributes:

-   [self.source]{style="font-family:Courier"} - this should refer to
    the source component (expected type is to be a component)
-   [self.sourcebox]{style="font-family:Courier"} - this should refer to
    the name of the source component\'s outbox to check. eg \"outbox\"
-   [self.sink]{style="font-family:Courier"} - - this should refer to
    the destination (sink) component (expected type is to be a
    component)
-   [self.sinkbox]{style="font-family:Courier"} - this should refer to
    the name of the sink component\'s inbox to check. eg \"inbox\"

Behaviour: (methods)

[\_\_init\_\_(self, source, sourcebox, sink,
sinkbox)]{style="font-family:Courier"}\
This should perform the following initialisation:

-   Call the super class initialiser ([Hint:]{style="font-weight:600"}
    keyword \"super\" in python docs, and pydoc)
-   set the attributes listed above :-)

[main(self)]{style="font-family:Courier"}\
This implements the behaviour described above:

In a loop

-   yield control back periodically (eg [yield
    1]{style="font-family:Courier"} is sufficient)
-   Check to see if [data]{style="font-family:Courier"} is
    [Ready]{style="font-family:Courier"} on the
    [source]{style="font-family:Courier"} component\'s
    [sourcebox]{style="font-family:Courier"}.
-   If there is [recv]{style="font-family:Courier"} the data from that
    box, and [send]{style="font-family:Courier"} it to the
    [sink]{style="font-family:Courier"} component\'s
    [sinkbox]{style="font-family:Courier"}.

**[Answer Hidden](/MiniAxon/Postman?template=veryplain)**

**[Show Answer](/MiniAxon/Postman?template=veryplain&pat=2)**

[Answer:]{style="font-weight:600"}

-   Select from the above tabs to show the answer!

[Discussion:]{style="font-weight:600"}

Given this, we can now start building interesting systems. We have
mechanisms for enabling concurrency in a single process (microprocess &
scheduler), a mechanism for adding communications (postboxes) to a
microprocess (component) and a mechanism for enabling deliveries between
components. Whilst we (the Kamaelia team) can see from an optimised
version that the postman can actually be optimised out of the system,
this simple mini-axon shows the core elements of Kamaelia quite nearly
in a microcosm.

One full version of this mini-axon can be found here: [Mini Axon
Full](http://kamaelia.sourceforge.net/MiniAxonFull.html), which should
now be clear what it\'s doing how and why.

A simple example we can now create is a trivial system with one
component creating some data and sending it to another one for display.

Running the above system then results in the following output:
