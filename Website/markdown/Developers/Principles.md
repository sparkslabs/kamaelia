---
pagename: Developers/Principles
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Developers/Principles
=====================

Don\'t take this too seriously, except for the bit in bold.\

Spend time on making your metaphors and interfaces clear.\
\

Descriptions of things optimised for the 80% of programmers are
preferable to those with only the top 20% will understand. If this seems
\"dumbing down\", consider that it is often harder to describe something
complex simply, than to describe something simple in a complex fashion.\
\

Try to make decisions that *can* work in other languages. Kamaelia is
only implemented right now in python, but the principles ***must*** be
portable.\
\

***Remember that a key aim is to make life easier for the bulk of
programmers, with a recognition that its worth optimising for
maintenance.***\
\

Fun descriptions, ideas and code tend to win arguments :-)\
\

You\'re going to get it wrong. Whether you like it or not, something you
do will go wrong and be very wrong. We\'d like to aim for a very high
hit rate of \"good\" decisions, but often the only way to find out what
the \"right\" answer is to actually try something and find out. Please
don\'t be afraid of pointing out the emperor has new clothes. We might
be embarrassed (possibly even upset) for a while, but we\'d rather be
told and know when we\'ve got something wrong. We\'re human too after
all :-) For a good discourse on why it\'s worth taking this risk, read
Paul Arden\'s excellent (and brief!) read \"Whatever you think, think
opposite\".\

-   A corrollary of this is that it might make sense occasionally to do
    sketches and branches of ideas that you think are really bad ideas
    and see how they pan out!\
    \

Implementations change, but interfaces stay the same. If the interfaces
change, you\'ve written something new. ie you may add new inboxes and
outboxes to components, but if you change behaviours of existing
in-/out-boxes you should consider whether you\'re actually writing
something new. If in doubt, talk to the team.\
\

Quick, simple, clear, justified decisions (But not hasty).\
\

All rules have exceptions.\
\

[import this]{style="font-family: Courier; font-weight: 600;"} :-) (and
**that** and **theother**)\
\
