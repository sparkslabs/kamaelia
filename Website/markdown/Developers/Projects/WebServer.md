---
pagename: Developers/Projects/WebServer
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task page: Web Server
=============================

> **PLEASE NOTE THIS PAGE IS CURRENTLY (15/12/2006.** **12:01)** **being
> filled in!**\
> **PLEASE NOTE THIS PAGE IS CURRENTLY (15/12/2006. 12:01) being filled
> in!**\
> **PLEASE NOTE THIS PAGE IS CURRENTLY (15/12/2006.** **12:01)** **being
> filled in!**\

::: {.boxright}
**Status:** Running - Code has been integrated with another project
providing another usecase\
**Current Developers:** Michael Sparks\
**Current \"inflight\" dev location:**
/Code/Python/Kamaelia/Kamaelia/HTTP\
**Start Date:** Jul 2006\
**Major Milestone date:** Sept 2006 - initial release\
**Expected End Date:** n/a\
**End Date:** n/a\
**Date this page last updated:** 15 December 2006\
**Estimated effort so far:** Original dev+ 0 days\
:::

**\
**

**Description**
---------------

The aim of this task is to create a complete, pure python, webserver
that is designed from the ground up to be suitable for use in Kamaelia
systems, and also easy to use/integrate with other python projects.\
\
It should be possible to use the Kamaelia web server to expose a web
interface for a Kamaelia system. It should be possible to take an
existing python based web application and use Kamaelia as a webserver
for that application.\
\
The original development context for this server was during Google
Summer of Code. Specifically:*\
*

-   Ryan wanted to create a webserver to serve IRC logs. (the reasons
    for this are shrouded by the mists of time).
-   Ryan also needed a webserver to upload .torrent files to as part of
    his summer of code project. This provided a useful test case.\

Benefits of creating this set of components:\

-   This enables Kamaelia based systems to gain an interface that many
    users are now familiar with - specifically using a web interface.
    However since we\'re python based, this means that we also have a
    webserver that can run client side, which is useful for a number of
    future projects beyond \"just\" integration with other web
    frameworks.\

Inputs
------

*This section is largely about WHO has influenced this task to do WHAT,
and where possible WHY. It is also about WHO to contact with regard to
this task to influence what\'s going on.\
*

*Task Sponsor: (can be main developer)*

*Task Owner: (likely to be main developer)\
*

*Developers involved in the task at some point\
*

-   *There is likely to be at least one. One will be the task owner (if
    the project is not in stasis)\
    *

*Users:*

-   *Specific concrete users who have provided input*

*Interested third parties*

-   *This will be specific third parties who have provided input to the
    project*

*Requirements*

-   *Each requirement should have who the requirement came from attached
    to it*
-   *Each requirement should have an indication of MUST/SHOULD/MAY/WOULD
    LIKE attached.*

*The people listed here should be real people. Unless you have agreement
however, this this should be their initials rather than name.\
\
Relevant Influencing factors:\
*

-   *eg release of a tool doing the same sort of thing that renders this
    non-relevant*
-   *people joining/leaving project*
-   *change of sponsorship*
-   *growth in users/thirdparties*
-   *tool dependency suitablility*
-   *unexpected complications*

Outputs
-------

*This section is largely about WHAT has been produced, normally by WHO
(in order to provide a point of contact)*\

### Expected

-   *There is likely to be at least one thing expected*\

### Actual

*This can take many forms\
*

-   *Code - what does it do, where is it?\
    *
-   *Reports - where is it, who wrote it, what was it about, when?\
    *
-   *Presentation - where is it, where was it presented, what was it
    about, who presented it, when?\
    *
-   *Events - eg The Brussels open space event*
-   *Other - other actual strands of work arising.\
    *

*Note: Especially with speculative tasks,actual outputs may be
substantially different from expected.\
*

### Realistic possibilities arising as a result of activity on this task

*Generally speaking there may or may not be anything here. The reason
this is under outputs, is because this really is an output, even if it
doesn\'t look like it at first glance.\
*

Related Tasks
-------------

### Tasks that directly enable this task (dependencies) 

-   *example: Multicast transciever, internet subsystem*
-   *This tasks should ideally be links to the project task pages for
    these other tasks.\
    *

### Sub Tasks

-   *Example: Selector subsystem shutdown*
-   *Each subtask here should ideally be a link to a project task page
    for that project*
-   *It would be* *nice but not mandatory to note the subtask status*
-   *For small subtasks, it **IS** acceptable to merely have subtasks as
    bullet points with the sort of information you\'d put on a project
    task page, but for which it seems overkill to create a project task
    page for. (It can always become a full PTP later on)\
    *

Task Log
--------

*This is a list of time indexed day to day item. There should ideally be
an entry here every time you work on this task. Ideally the time taken
relating to each entry should be listed as well, preferably in man days,
down to 1/4 day granuarity. (ie 2 hours). Sanity is expected to prevail
when noting this down. They should be annotated by who made the entry,
when, and any status changes.*\

***When a task is running, then this is where most updates will
occur.**\
\
Please put **Output** in bold prior to any entries where an output was
produced\
Please put **Task status changed** in bold when the entry relates to a
task status change.\
Example entries:\
*

-   *Created the PTP page for the project, and brainstormed how to get
    started. Michael. November 27th 2006. Time spent 1/4 day*
-   ***Output:** Produced report (added to output list), Michael.
    November 27th 2006. Time spent 1/4 day.*
-   *Liased with sponsor (input to task). Michael, Sponsor, November
    27th 2006. Time spent 1/2 day.*
-   *Started working of frobbing the bibble, code is being worked in in
    /Sketches/MPS/Here/\...\
    **Task status changed** to running.\
    Time spent: 1/2 day\
    Michael, November 27th 2006\
    *
-   *Project blocked due to lack of access to kit, Michael, 27th
    November 2006. Time spent: n/a, **Task status changed** to blocked.*
-   *Changed sponsor to Jimbo*
-   *Added developer Matt*
-   *Removed developer Michael*
-   *Removed developer Matt*
-   ***Task status changed** to stasis*

*This is however a task log. The format of entries hasn\'t be decided on
yet. However there should ideally be an entry an minimum whenever the
state of the task changes - that is new developers, sponsors, inputs
from people, outputs from the task, whether the project is completed,
finished etc.\
The reason for including times is to assist in future time estimation
exercises.\
As a result each entry is likely to have:\
*

-   *A note of any state change (new person, new input, new output,
    status change, new work started, completed etc) This can however
    simply be a note to say what\'s been done in that amount of time
    working on the task. eg code refactoring is none of the above, but
    is work, and is suitable for the task log, as is simply \"coding,
    Michael, November 27th, 1 day\", etc*
-   *Who is making the entry*
-   *When they are making the entry*
-   *The amount of time spent in the process of effecting that entry.
    (eg 1/2 day writing a report, 1/2 writing code, etc)*

*I\'d expect much of this text to be deleted.*\
\

Discussion
----------

*This is where random comments with regard to the project can be added.
It\'s expected this section will be in thread mode rather than document
mode, but people should feel able to refactor comments. If they do,
these comments become inputs to the project, and the people who have
added comments would be added under interested third parties.*

*Anything that doesn\'t fit above fits in here.*

#### end note (delete from any actual PTP)

(10:34:02) **Lawouach:** well\
(10:34:15) **Lawouach:** the handler needs to differentiateHTTP methods\
(10:34:28) **Lawouach:** the example assumes every methods will behave
the same ay\
(10:34:29) **Lawouach:** way\
(10:34:38) **Lawouach:** which is perfectly fine for an example\
(10:34:44) **Lawouach:** but didn\'t suit my requirements\
(10:34:59) **mhrd:** indeed\
(10:35:05) **Lawouach:** in fact\
(10:35:09) **Lawouach:** when you have time\
(10:35:20) **Lawouach:** I\'ll be happy to tell you where the HTTP
protocol could be improved\
(10:35:24) **Lawouach:** for the developer\
(10:35:28) **Lawouach:** not the internal code\
(10:35:35) **Lawouach:** but the public interface\
(10:35:55) **Lawouach:** and of course having support for DELETE and PUT
will be a must have :D\
(10:36:09) **MS-:** Please chat away whilst your mind is fresh\
(10:36:11) **\*\*\*mhrd** crash courses himself in how Ryan\'s HTTP
server protocol is used :)\
(10:37:17) **Lawouach:** well\
(10:37:45) **Lawouach:** take this file\
(10:37:46) **Lawouach:**
<http://trac.defuze.org/browser/oss/amplee/amplee/examples/web/demo_wsgi.py>\
(10:37:52) **Lawouach:** based on a pure WSGI approach\
(10:38:04) **Lawouach:** using the selector WSGI middleware to do the
dispatching\
(10:38:17) **Lawouach:** you can see I associate my handlers based on
the HTTp methods\
(10:38:36) **Lawouach:** the current interface of the HTTP package
coming with K.\
(10:38:50) **Lawouach:** does not help make this an easy task\
(10:38:54) **Lawouach:** and as you\'ve seen\
(10:39:05) **Lawouach:** I had to do a if/else within the handler\
(10:39:15) **MS-:** Yep.\
(10:39:25) **Lawouach:** it\'s fine but also a bit\... hmmm\
(10:39:32) **MS-:** inelegant\
(10:39:36) **Lawouach:** yes\
(10:40:04) **Lawouach:** but I don\'t blame Ryan\'s code, I don\'t think
it was a priority :)\
(10:40:10) **Lawouach:** rightly so\
(10:40:30) **Lawouach:** moreover\
(10:40:41) **Lawouach:** the dispatching based on the path of the URI\
(10:40:44) **Lawouach:** is cumbersome\
(10:40:50) **Lawouach:** and will be prone to error\
(10:40:55) **Lawouach:** because it is way to simplistic\
(10:40:59) **Lawouach:** mind you\
(10:41:06) **Lawouach:** this is easily tweakable\
(10:41:12) **Lawouach:** via the createRequestHandler code\
(10:41:37) **Lawouach:** it\'d be nice however if K. could have better
code in built-in\
(10:41:52) **Lawouach:** something based on Routes/selector for instance
would be great\
(10:42:32) **Lawouach:** brb\
(10:42:39) **MS-:** np\
(10:44:03) **Lawouach:** back\
(10:44:26) **Lawouach:** anyway, I think Ryan\'s code s a very good stab
at HTTP/1.1\
(10:44:33) **Lawouach:** it supports many features\
(10:44:39) **Lawouach:** it\'s just a bit rough around the edges\
(10:44:57) **MS-:** Indeed, I was impressed with what he managed to get
written quickly\
(10:45:32) **MS-:** Examples of APIs you like would be useful.\
(10:45:41) **MS-:** In essence this will be an \"odd\" area\
(10:46:05) **MS-:** because in order to stay useful as a kamaelia
component, certain aspects of the API need to stay\
(10:46:14) **MS-:** However it\'s a component that sits on an edge\
(10:46:19) **MS-:** (an adapter)\
(10:46:24) **MS-:** to other sorts of libraries\
(10:46:33) **Lawouach:** yes\
(10:46:41) **MS-:** So knowing a better API would be useful\
(10:46:57) **Lawouach:** it would not need much\
(10:46:58) **MS-:** (After all providing that API would be best
implemented as a component itself)\
(10:49:32) **MS-:** OK, I think I\'ll create a PTP page for the
HTTPServer, and copy this into the discussion area.\
(10:50:35) **MS-:** I think having an adapter component that adapts the
framework to provide a WSGI interface would probably be a good step
since it then\
(10:50:45) **MS-:** makes the server more generally available\
(10:50:53) **MS-:** Not that I\'ve ever written any WSGI stuff\
(10:51:39) **Lawouach:** but as you said this component lives on the
edge, that means, I know my library does not take benefit from K. per
se, but instead I use the HTTPServer as an interface between my library
and K.\
(10:51:50) **Lawouach:** I expect more of this to happen in the future\
(10:51:58) **MS-:** Yep\
(10:52:20) **MS-:** I\'ve been considering also providing a file like
interface to components BTW\
(10:52:24) **Lawouach:** re: WSGI \<\-- yes indeed!\
\
\
