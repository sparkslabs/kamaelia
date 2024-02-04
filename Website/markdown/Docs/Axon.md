---
pagename: Docs/Axon
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Axon]{style="font-size: 24pt; font-weight: 600;"}
==================================================

[Axon is the core subsystem in Kamaelia]{style="font-style: italic; font-size: 18pt;"} {#axon-is-the-core-subsystem-in-kamaelia align="right"}
--------------------------------------------------------------------------------------

-   **[the mini-axon tutorial](/MiniAxon/)**
-   **[a document about a notation](NotationForVisualisingAxon)**
-   **[reference documentation](/Docs/Axon/Axon)**

Introduction & Visual Notation 
------------------------------

Axon forms the core of Kamaelia. There are two possible introductions
you may wish to follow:

-   One is **[the mini-axon tutorial](/MiniAxon/)** - a series of
    exercises which encourage you to build your own Axon Core.\
-   The other is really **[a document about a
    notation](NotationForVisualisingAxon)** for visualising Axon
    systems. However this does also mean it needs to introduce the
    essential elements as well. By way of an example, it shows you how
    the SimpleServer component works inside when the system starts up.
    This is a lightly revamped version of an internal document - about 6
    months into the project.\

It is highly recommend to ***do*** the former, and to *read* the latter
:-). If you are pushed for time, reading the latter is recommended.\

Reference Documentation 
-----------------------

There is comprehensive **[reference documentation](/Docs/Axon/Axon)**
for Axon. This includes detailed explanations and simple examples and is
useful both if you are writing components and also if you want to gain a
deeper understanding of Axon.

This documentation is regularly automatically rebuilt from our latest
code in the repository.\

Installation and other ways to find documentation
-------------------------------------------------

The following text is adapted from the README bundle that accompanies
Axon\'s separate download\...

Axon is the core of Kamaelia. The contents of this directory must be
installed before the rest of Kamaelia can be used. It can also be used
independently of Kamaelia.

The install procedure is python\'s usual dance:

-   python setup.py install

Documentation is held in two places: (until this section is complete)

-   The usual \'pydoc name\' - probably worth starting with:\
    pydoc Axon.Component
-   The test suite is designed to allow you to get low level API
    behaviour information - \"should X,Y, Z work? If so, what
    happens?\". It\'s a partly retrofitted test suite, but some is TDD.
    (TDD took over late in the project) As a result, for example,
    passing a -v flag result in the docstring for each test to be dumped
    in a form that allows collation, and summarisation. (For an example
    of what we expect to automate from the test suite, see the end of
    this README file)

Sample producer/consumber & wrapper component system:

The testComponent creates 2 subcomponents, creates the links in place,
and takes the output from the consumer and links it to its own
private/internal \_input inbox. When it recieves a value from the
consumer, it reports this fact and ceases operation.

-   Producer sends values to its result outbox
-   Consumer takes values from its source, does some work and sends
    results to its outbox

(It\'s probably worth noting that an introspection system would be
possible to write/nice to see that would be able to derive the above
diagram from the running system)

Example code:

::: {.boxright}
**NOTE:** You are recommended where possible to use Pipeline or it\'s
friend Graphline where-ever possible these days since it is a) efficient
b) shows your intention clearer. It also saves with messing around with
scheduler.run.runThreads! :-)
:::

Kamaelia provides a pipeline component that provides syntactic sugar for
testHarness above. The above shows how you would use Axon by itself
without any other components to build a simple producer consumer. We can
replace the testComponent (and everything below!) with the following:

Michael, Matt, Lightly updated October 2005, December 2006, April 2007\
\
