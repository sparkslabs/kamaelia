---
pagename: MiniAxon/InterludeTwo
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[6 Interlude 2]{style="font-size:14pt;font-weight:600"}

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
