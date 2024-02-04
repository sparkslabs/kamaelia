---
pagename: MiniAxon/Microprocess
last-modified-date: 2008-10-28
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
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

**[Answer Hidden](/MiniAxon/Microprocess?template=veryplain)**

**[Show Answer](/MiniAxon/Microprocess?template=veryplain&mat=2)**

[Answer:]{style="font-weight:600"}

-   Select from the above tabs to show the answer!

[Discussion:]{style="font-weight: 600;"}

Clearly we can create a handful of these now:

Calling their main method results in us being given a generator:

We can then run these generators in the usual way (though these are
fairly boring microprocesses):

OK, so we have a mechanism for adding context to generators, and we\'ve
called that a microprocess. Let\'s make it simple to set lots of these
running.
