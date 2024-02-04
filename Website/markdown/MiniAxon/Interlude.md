---
pagename: MiniAxon/Interlude
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[3 Interlude]{style="font-size:14pt;font-weight:600"}

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

The key point we have is [active ]{style="font-style:italic"}objects
talking only to local interfaces, and not knowing how those local
interfaces are used.

So the next step is to first create this standard interface for external
communications, and then a mechanism for allowing communication between
these interface.
