---
pagename: MiniAxon
last-modified-date: 2008-10-13
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Mini-Axon]{style="font-size: 24pt; font-weight: 600;"}

[Build your own Kamaelia Core]{style="font-size: 16pt;"}

It\'s interesting to note that there are two kinds of rich people in the
world: those who made the money they have, and those who inherited it.
Those who make it for themselves have often been noted to be greater
risk takers than those who simply inherit. This is for the very simple
reason - they\'ve done it once, so they believe they can do it again.

Likewise when using any system, library, or framework, you\'re likely to
have a better understanding of the system and how to better use it if
you really understand how it works. That is you\'ve written the system
rather than someone else. Our preferred approach to date so far for
teaching a novice how to use to Kamaelia has been to get them to write a
version of the core concurrency system. This is framed as a series of
exercises. After having built it, they realise that the system is really
just a simple skein over simple programs.

Furthermore, this set of exercises has normally been done within less
than 2 weeks of the novice learning python. If you\'re a new programmer,
and you\'ve learnt a certain core of python, you should be able to do
and follow these exercises. It might look daunting, but it should be
fine. If you get stuck, please feel free to come chat on IRC or on the
mailing lists!

[Python pre-requisitives:]{style="font-weight: 600;"}

-   classes, methods, functions, if/elif/else, while, try..except,
    for..in.., generators (yield), lists, dictionaries, tuples.

[What\'s in this tutorial?]{style="font-weight: 600;"}

1.  Write a basic
    [[Microprocess]{style="font-weight: 600;"}](/MiniAxon.html#Microprocess)
2.  Build a simple
    [[Scheduler]{style="font-weight: 600;"}](/MiniAxon.html#Scheduler)[
    ]{style="font-weight: 600;"}to run the Microprocesses
3.  Interlude, discussing progress so far and what you can do with
    microprocesses and schedulers, putting the next two exercises in
    context
4.  Turn a microprocess into a Simple
    [[Component]{style="font-weight: 600;"}](/MiniAxon.html#Component)
5.  Create a
    [[Postman]{style="font-weight: 600;"}](/MiniAxon.html#Postman)[
    ]{style="font-weight: 600;"}to deliver data between microprocesses
6.  A second interlude where you see how to use your framework to build
    a simple multicast server that can serve a file over multicast. The
    resulting components can be used with the main Axon system as they
    can with your mini-axon system.
7.  Summary

At the end of this tutorial you will have your own mini-axon core,
compatible with the absolute core of Kamaelia\'s Axon.

[]{#Microprocess}[1. Microprocesses - A Generator with
Context]{style="font-size: 14pt; font-weight: 600;"}

Axon is built on top of generators with some added context. Whilst the
most common version of this a user actually uses is called a component,
this is a specialisation of the general concept - a generator with
context.

[Exercise:]{style="font-weight: 600;"} Write a class called
[microprocess]{style="font-family: Courier; font-weight: 600;"} (make
sure you subclass \"object\" !) with the following methods:

[\_\_init\_\_(self)]{style="font-family: Courier;"}

-   Takes no arguments. (aside from self)
-   into this put any initialisation you might need

[main(self)]{style="font-family: Courier;"}

-   Takes no arguments. (aside from self)
-   This should be a generator that simply yields 1 value - specifically
    a 1

[Answer:]{style="font-weight: 600;"}

[Discussion:]{style="font-weight: 600;"}

Clearly we can create 5 of these now:

Calling their main method results in us being given a generator:

We can then run these generators in the usual way (though these are
fairly boring microprocesses):

OK, so we have a mechanism for adding context to generators, and we\'ve
called that a microprocess. Let\'s make it simple to set lots of these
running.

[]{#Scheduler}[2. Scheduler - A means of running lots of
microprocesses]{style="font-size: 14pt; font-weight: 600;"}

[Exercise: ]{style="font-weight: 600;"}Write a class called
[scheduler]{style="font-family: Courier; font-weight: 600;"} with the
following characteristics.

-   It should subclass microprocess.

Objects created shold have the following attributes:

-   [self.active]{style="font-family: Courier;"} - this is a list.
    (initially empty)
-   [self.newqueue]{style="font-family: Courier;"} - this is also a
    list. (initially empty)\
    [Hint: ]{style="font-weight: 600;"}Initialise these in the
    \_\_init\_\_ method!

Objects created should have the following methods:

[\_\_init\_\_(self)]{style="font-family: Courier;"} - Perform any
initialisation you need here (see above)\
[Remember: ]{style="font-weight: 600;"}Don\'t forget to called your
super class\'s \_\_init\_\_ method!

[main(self) ]{style="font-family: Courier;"}- Takes no arguments\
This should be a generator with the following logic: (Looped 100 times)

Loop through all the objects in self.active using any mechanism you
choose.

-   IMMEDIATELY YIELD CONTROL HERE WITH a \"non -1 value\"
-   Suppose you call the current object (from self.active) current
-   Call current.next()
-   If a StopIteration exception is thrown, just catch and skip on to
    the next iteration. (eg continue)
-   If the result from current.next() was NOT -1, then append current
    onto self.newqueue

Having looped through all the objects, REPLACE self.active with
self.newqueue, and replace the value of self.newqueue with a new empty
list

[activateMicroprocess(self, someprocess)]{style="font-family: Courier;"}

-   someprocess is a microprocess object (or anything that conforms to
    the same interface/behaviour seen by the scheduler).
-   This method should call the object\'s main method and append the
    result to self.newqueue

[Answer:]{style="font-weight: 600;"}

[Discussion:]{style="font-weight: 600;"}

This class provides us with a rudimentary way of activating generators
embedded inside a class, adding them to a runqueue and then letting
something run them. So let\'s try it. The default microprocess is
relatively boring, so let\'s create some microprocesses that are little
more than an age old program that repeatedly displays a messae. To do
that we declare a class subclassing microprocess and provide a generator
called main. We\'ll also capture a provided argument:

Note that this generator doesn\'t ever exit. We can then create a couple
of these printers:

Next we can create a scheduler:

We can then ask this scheduler to activate the two microprocesses - X &
Y :

We can then run our scheduler by iterating through its main method:

If we run this we get the following output (middle of output snipped):

As you can see, the scheduler hits the 100th iteration and then halts.

[3 Interlude]{style="font-size: 14pt; font-weight: 600;"}

So far we\'ve created a mechanism for giving a generator some implicit
context by embedding it inside a microprocess class. We\'ve also created
a simple microprocess that repeatedly displays the same message over and
over again. We\'ve also created a simple mechanism for setting lots of
microprocesses running and watching them just go.

This is all well and good and core aspects of Axon. However another core
aspect is enabling these generators to talk to each other. Doing this
means we can divide responsibility for a task between file reading, and
display. The metaphor we choose to use in Axon is a very old one - that
of a worker at a desk with a number of inboxes and a number of outboxes.
The worker receives messages on his/her inboxes. He/She does some work,
and send results on his/her outboxes. We can then have something that
takes messages from an outbox (called saying \"finance\") and delivers
them to the inbox of somewhere else (say the inbox \"in\" on the finance
desk/component).

An alternate analogy we don\'t take here is one of computer chips with
pins and wires. Signals would get sent to pins transmitted along the
wires (links) to other pins on other chips. A more software oriented
alternative is unix pipelines and standard file descriptors. A unix
command line program always\* has access to stdin, which it reads but
has no idea of the source; stdout it can write to, but has no idea of
destination (and stderr). Obviously however unix command line programs
don\'t know if they\'re in a pipeline, or standalone.

The key point we have is [active ]{style="font-style: italic;"}objects
talking only to local interfaces, and not knowing how those local
interfaces are used.

So the next step is to first create this standard interface for external
communications, and then a mechanism for allowing communication between
these interface.

[4[]{#Component} Simple Component - Microprocesses with standard
external interfaces]{style="font-size: 14pt; font-weight: 600;"}

[Exercise: ]{style="font-weight: 600;"} Write a class called
[component]{style="font-family: Courier; font-weight: 600;"} that
subclasses [microprocess]{style="font-family: Courier;"} with the
following\...

Attributes:

[self.boxes]{style="font-family: Courier;"} - this should be a
dictionary of the following form:

<div>

Clearly this allows for more inboxes and outboxes, but at this stage
we\'ll keep things simple.

</div>

Behaviour: (methods)

As before an [\_\_init\_\_]{style="font-family: Courier;"} for anything
you need (eg attributes above :)\

[send(self, value, boxname)]{style="font-family: Courier;"}

This method takes the value and appends it to the end of the list
associated with the boxname.

That is if I do:

::: {dir="ltr"}
Then given the suggested implementation of boxes above the following
should be true afterwards:
:::

::: {dir="ltr"}
ie the last value in the list associated with the boxname is the value
we sent to that outbox. More explicitly, if the value of self.boxes was
this beforehand:
:::

::: {dir="ltr"}
And the following call had been made:
:::

::: {dir="ltr"}
The self.boxes would look like this afterwards:
:::

[recv(self, boxname)]{style="font-family: Courier;"}

This is the logical opposite of sending. Rather than appending a value
at the end of the send queue, we take the first value in the queue.

Behaviourally, given a starting value of self.boxes:

::: {dir="ltr"}
Then I would expect the following behaviour code\....
:::

::: {dir="ltr"}
\... to display the following sort of behaviour:
:::

::: {dir="ltr"}
The value of self.boxes should also change as follows after each call:
:::

[dataReady(self, boxname)]{style="font-family: Courier;"}

This should return the length of the list associated with the boxname.\
\
For example, given:

<div>

The following behaviour is expected:

</div>

[Answer:]{style="font-weight: 600;"}

[Discussion:]{style="font-weight: 600;"}

Ok that\'s a fairly long description, but a fairly simple
implementation. So what\'s this done? It\'s enabled us to send data to a
running generator and recieve data back. We\'re not worried what the
generator is doing at any point in time, and so the communications
between us and the generator (or between generators) is asynchronous.

An extension to the suggested \_\_init\_\_ is to do the following:

This small extension means that classes subclassing
[component]{style="font-family: Courier;"} can have a different set of
inboxes and outboxes. For example:

That said, components by themselves are relatively boring. Unless we
have some way of moving the data between generators we haven\'t gained
anything (really) beyond the printer example above. So we need
someone/something that can move data/messages from outboxes and deliver
to inboxes\...

[5[]{#Postman} Postman - A Microprocess that performs
deliveries!]{style="font-size: 14pt; font-weight: 600;"}

Given we have outboxes and inboxes, it makes sense to have something
that can handle deliveries between the two. For the purpose of this
exercise, we\'ll create a microprocess that can look at a single outbox
for a single component, take any messages deposited there and pass them
the an inbox of another component. In terms of the component
implementation so far we can use
[dataReady]{style="font-family: Courier; font-weight: 600;"} to check
for availability of messages,
[recv]{style="font-family: Courier; font-weight: 600;"} to collect the
message from the outbox, and
[send]{style="font-family: Courier; font-weight: 600;"} to deliver the
message to the recipient inbox.

[Exercise: ]{style="font-weight: 600;"} Write a class called
[postman]{style="font-family: Courier; font-weight: 600;"} that
subclasses [microprocess]{style="font-family: Courier;"} with the
following\...

Attributes:

-   [self.source]{style="font-family: Courier;"} - this should refer to
    the source component (expected type is to be a component)
-   [self.sourcebox]{style="font-family: Courier;"} - this should refer
    to the name of the source component\'s outbox to check. eg
    \"outbox\"
-   [self.sink]{style="font-family: Courier;"} - - this should refer to
    the destination (sink) component (expected type is to be a
    component)
-   [self.sinkbox]{style="font-family: Courier;"} - this should refer to
    the name of the sink component\'s inbox to check. eg \"inbox\"

Behaviour: (methods)

[\_\_init\_\_(self, source, sourcebox, sink,
sinkbox)]{style="font-family: Courier;"}\
This should perform the following initialisation:

-   Call the super class initialiser ([Hint:]{style="font-weight: 600;"}
    keyword \"super\" in python docs, and pydoc)
-   set the attributes listed above :-)

[main(self)]{style="font-family: Courier;"}\
This implements the behaviour described above:

In a loop

-   yield control back periodically (eg [yield
    1]{style="font-family: Courier;"} is sufficient)
-   Check to see if [data]{style="font-family: Courier;"} is
    [Ready]{style="font-family: Courier;"} on the
    [source]{style="font-family: Courier;"} component\'s
    [sourcebox]{style="font-family: Courier;"}.
-   If there is [recv]{style="font-family: Courier;"} the data from that
    box, and [send]{style="font-family: Courier;"} it to the
    [sink]{style="font-family: Courier;"} component\'s
    [sinkbox]{style="font-family: Courier;"}.

[Answer:]{style="font-weight: 600;"}

[Discussion:]{style="font-weight: 600;"}

Given this, we can now start building interesting systems. We have
mechanisms for enabling concurrency in a single process (microprocess &
scheduler), a mechanism for adding communications (postboxes) to a
microprocess (component) and a mechanism for enabling deliveries between
components. Whilst we (the Kamaelia team) can see from an optimised
version that the postman can actually be optimised out of the system,
this simple mini-axon shows the core elements of Kamaelia quite nearly
in a microcosm.

One full version of this mini-axon can be found here: [Mini Axon
Full](/MiniAxonFull.html), which should now
be clear what it\'s doing how and why.

A simple example we can now create is a trivial system with one
component creating some data and sending it to another one for display.

Running the above system then results in the following output:

[6 Interlude 2]{style="font-size: 14pt; font-weight: 600;"}

If you\'ve come this far, you may be wondering the worth of what you\'ve
acheived. Essentially you\'ve managed to implement the core of a working
Axon system, specifically on the most used aspects of the system. Sure,
there is some syntactic sugar relating to creation and managing of
links, but that\'s what it is - sugar.

One of the longer examples on the Kamaelia website, specifically in the
blog area, is how to build new components. That\'s probably the next
logical place to start looking. However, taking one of the components on
that page, we find that the core implementation of them matches the same
core API as the component system you\'ve implemented.

For example, let\'s take a look at the multicast sender.

This has an initialiser for grabbing some initial values, and ensuring
the super class\'s initialiser is called:

The main function/generator then is relatively simple - set up the
socket, wait for data and send it out:

From this, it should be clear that this will work inside the mini-axon
system you\'ve created.

Similarly, we can create a simple file reading component thus:

This can then also be used using the component system you\'ve just
created to build a simplistic system for sending data to a multicast
group:

That can then be activated and run in the usual way:

[7 Summary]{style="font-size: 14pt; font-weight: 600;"}

This page has hopefully helped you build a core component system based
on Kamaelia\'s Axon. It should be clear as well from this that the core
of Kamaelia is actually quite small. We\'ve found a number of aspects
which we can optimise, add in syntactic sugar, and we\'re discovering
that certain facilities are needed, and can be useful. However the raw
core is simple - it\'s about generators communicating with inboxes and
outboxes, and then building interesting systems on top of that.

The next step we\'d normally recommend at this point is to build some
interesting systems. Some exercises which will hopefully be helpful will
appear as time progresses.

The next step we\'d normally recommend at this point is to build some
interesting systems. Some exercises which will hopefully be helpful will
appear as time progresses.
