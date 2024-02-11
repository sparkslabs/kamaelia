---
pagename: Codeless Composition
last-modified-date: 
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
SoC Project: CodelessComposition
================================

There was one project application in this area that is summarised here.
This page contains the depersonalised content, which can be consolidated
as necessary. The depersonalisation is for privacy reasons, credit is
here due to those who spent the time writing these descriptions.

## Project Title: Primitives - Components for codeless composition 

### Benefits to Kamaelia:

allow users to construct a parallel system graphically. The systems way
of allowing components to be joined together is ideal for this. A user
could stitch together their program and be able to see the execution of
the code in their \"multi-threaded\" program, something which has
previously been limited to simple \"single-threaded\" programs. The
ability to visualize the programs execution paths may well mean it
becomes easier in the future to develop components, or systems of
components graphically, before compiling them down to something more
optimized python functions.

### Synopsis:

I believe the development of the primitive components themselves
(without the graphics) could be done in a matter of minutes,
particularly as Python allows the dynamic calling of methods. A general
primitive component with one outbox and any number of inboxes could be
designed to call a given method on whatever object was in the first of
its inboxes with the first item in each of its other inboxes as
arguments and putting the result in its outbox. The harder primitive
programming language elements to engineer as components would be if else
statements because their output is which of two pipes to pass a set of
elements to next.

The visual IDE aspect of the project, for stitching the components
together would take far more time. I also imagine enabling the visual
IDE to display the program\'s execution would be the last part of the
project. The IDE would work similarly to the Crocodile ICT program
(shown here: http://www.crocodile-clips.com/crocodile/ict/index.jsp).
Pipelines made by stitching components together could be wrapped by the
IDE into mega components that carry out a given task and manipulated as
one within the IDE. The most primitive components would be turned into
Python code by the IDE for better efficiency.

### Deliverables:

I\'d expect to as I mentioned above have the non-graphical components
built almost straight away. My aim after that would be to build a set of
components to stitch them and other components together graphically and
execute them. Wrapping components together for easier manipulation in
the IDE should then be straight forward and I\'d hope if I had time to
have the program be able to turn groups of primitive components into
single component classes not containing any sub-components. In any time
I\'d have left I\'d aim to add anything suggested to the IDE and to
allow the IDE to be able to display its execution.

### Project Details:

I will develop the project in Python and use the Kamaelia system. Using
the Pygame libraries for the interface.\
The benefits I hope the project provides I hope I\'ve covered above
(there\'s 6 minutes to the deadline at the moment so I won\'t write any
more here for now).

### Project Schedule:

First week: Build primitive components and become fully acquainted with
Kamaelia.
Second and third week (and possibly 4th week): Build some prototypes in
Pygame of the interface and familiarize myself with the techniques
needed.
Month two: Build and deliver version 1 of the IDE.
Month three: Work on the grouping of primitive components.

