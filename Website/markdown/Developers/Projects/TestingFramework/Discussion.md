---
pagename: Developers/Projects/TestingFramework/Discussion
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Developers/Projects/TestingFramework/Discussion
===============================================

These are ideas gathered for the testing framework. This ideas are still
being discussed, I just write this wiki page to be able to effectively
reference them in an easy way (saying \[foo1\] instead of saying \"that
thing Foo said in the list that day\...\"). I\'ll update this page
during the discussion.\
\

Convention
----------

\
I\'m using the convention \[xxxY\] being xxx the first three letters of
the nick of somebody and Y the number of the idea of this someone.\
\
\[orp?\] -\> orphans\
\[dav?\] -\> Davbo\
\[law?\] -\> Lawouach\
\[cho?\] -\> Chong\
\[jba?\] -\> j\_baker\
\

Ideas
-----

\
So the ideas, if I understood them correctly, are:\
\
  \[orp1\] Provide a given input to a components and check the outputs
to check that the format is correct.\
  \[orp2\] Make sure that when you ask for it, it finishes.\
  \[orp3\] Check that a component has called the pause() method at some
time\
\
  \[dav1\] A random set of pygame interrupts to the display\
  \[dav2\] A logging engine that can be enable/disable certain
components so you can keep the printing of the messages in the code, but
it will just not be showed if not wanted.\
\
  \[law1\] Be able to unit test components independently.\
\
  \[cho1\] Provide inputs for the component and expect output from it.\
  \[cho2\] Check variables in runtime.\
  \[cho3\] try..except helpful to prevent program from crashing but
harmful when finding bugs. It would be nice if it could be disabled.\
  \[cho4\] Check which components are still running and which components
are not.\
\
  \[jba1\] logging engine that can be enable/disable certain components
so you can keep the printing of the messages in the code, but it will
just not be showed if not wanted.\
\

Ordering the ideas
------------------

\
Ordering them by functionality, we get:\
\

-    \[orp1\], \[orp2\], \[law1\], \[cho1\] essentially refer to a basic
    Axon-based testing framework.
-   \[orp3\] refers to a cool feature of the testing framework.
-   \[cho4\] refers to another cool feature of the testing framework.

\

-   \[dav2\] and \[jba1\] are essentially a logging engine, which may
    not be part of the testing framework (but it\'s still interesting
    since that\'s the other part of my GSOC project :-D )
-   \[cho2\] may be closer to what a debugger would offer, but since
    even local variables in a generator can be easily retrieved (see
    [here](http://pastebin.com/m7a316728)), it might be interesting to
    consider it for accessing local variables in the component. This
    would be really cool, but I will not add it to a first stage.\
-   \[cho3\] may use a method \"independent of the testing framework\"
    (in order to call something like \"self.raiseExceptions\" which
    re-raise the raised exception only if a certain variable is set),
    although later the testing framework would use that variable, I\'m
    not sure if it\'s something tied to it.\
-   \[dav1\] refers to an interesting feature that may not be integrated
    in an automated testing framework, although it may be possible
    through a virtual X server such as Xvfb. I have to give it another
    thought though.\

\
\
\
