---
pagename: Developers/Projects/WebServerConsolidation
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: Web Server Consolidation 
-------------------------------------------

::: {.boxright}
**Status:** Started\
**Current Developers:** G0SUB\
**Current \"inflight\" dev location:** /Sketches/BG/\
**Start Date:** 12th April 2007\
**Major Milestone date:** -\
**Expected End Date:** *-*\
**End Date:** *-*\
**Date this page last updated:** April 14th 2007\
**Estimated effort so far:** 1hr\
:::

**\
**

**Description**
---------------

This task will extend the web-server component in Kamaelia to make it
useful as a general purpose web-server component.\
\
It will be possible at the end of this task to use the Kamaelia Web
Server to server both static pages and run CGI scripts within the
Kamaelia webserver. This will result in a pure python webserver that
should hopefully be deployable on both servers and clients. Support of
WSGI is likely to be explored as well, given sufficient time, which
would allow tools like Django & Pylons to be run in a scalable manner on
the client side, not just in test mode.\
\
The current web-server component in Kamaelia was written as a part of
Google Summer of Code 2006 program. It is largely functional but it
still needs a few more features before it can be used as a single
threaded, general purpose web-server component. Besides that, it has a
few things hard coded into the web-server which makes it less flexible.\
\
This project will add a few new features to the web-server component
(like full HTTP/1.0 support) and will make it more flexible and
user-friendly (user configurable options, over-ridable error handling),
etc. This way, the web-server component in Kamaelia will be useful as a
stand alone web-server and could be used in a wide range of situations.\

Inputs
------

This section is largely about WHO has influenced this task to do WHAT,
and where possible WHY. It is also about WHO to contact with regard to
this task to influence what\'s going on.\

Task Sponsor: Michael

Task Owner: G0SUB

Developers involved in the task at some point\

-   G0SUB

Users:

-   Michael
-   Sylvain

Interested third parties

-   Sylvain

Requirements

-   Each requirement should have who the requirement came from attached
    to it
-   Each requirement should have an indication of MUST/SHOULD/MAY/WOULD
    LIKE attached.

***Initial project plan***\
\
I will extend the web-server component in Kamaelia to support all
HTTP/1.0 methods (like GET, PUT, POST, etc.), add configurable options,
like document root, port to listen on, additional mime-types, etc. I
will also add CGI support to the web-server. I will also make the server
extensible so that the user can override customise the behaviour of the
server in case of errors, etc.\
\
I would like to restructure the existing code a bit to make the
component easily importable and usable from other modules.\
\
There are a few other things which I intend to work on, like adding
support for requests with byte ranges, etc.\
\
I will also investigate the possibility of adding WSGI support and a
generic interface to add custom methods to the web-server given
sufficient time.\
\
*Deliverables:*\
\
The Project deliverables are \--\

-   Full HTTP/1.0 support in the web-server
-   Configurable CGI support
-   User defined error handling
-   Test cases for the above
-   Documentation and recipes for the CookBook

And given sufficient time \--\

-   WSGI support
-   Support for byte range, cache control
-   An interface to add extra methods to HTTP

*Project Details:*\
\
The web-server already uses Axon as its core infrastructure, and that is
what I will use too. The CGI part of the web-server will be implemented
using the already available UnixProcess component though it may need to
be adapted slightly to accommodate custom environment variables for the
CGI program to execute.\
\
The other implementation aspects of the project have already been
covered above.\
\
*Project Schedule:*\
\
I will start with discussing the implementation with the Kamaelia
developer community and my mentor. Then I will read the
[HTTP/1.0](http://www.faqs.org/rfcs/rfc1945.html) and
[HTTP/1.1](http://www.faqs.org/rfcs/rfc2616.html) standards and learn
more about the various aspects of the protocol. I also need to read up
the [Axon tutorial](../../../MiniAxon/) to understand more about the
workings of the core infrastructure. I will then start implementing the
missing aspects of the protocols. Once that is done, I will take up
adding CGI support to the component. Meanwhile I will also clean up the
code and add some features to make it more user friendly and
extensible.\
\
This should take around 4 weeks to be implemented but in keeping with
the various issues involved with Software Engineering, may take up to Pi
times more than estimated. After that I will write the test cases and
add documentation for the newly implemented features.\
\
If I am left with sufficient time, I will investigate implementing
[WSGI](http://wsgi.org/wsgi) support in the web-server, so that it works
across various implementations of Python web frameworks. I will also
implement byte range support and cache control given time.\
\
The development will be done completely in the open and the code will be
hosted on sourceforge.net or somewhere else if available. I intend to do
one Alpha and two Beta releases before doing the stable release to
ensure better testing of the code.\

Outputs
-------

This section is largely about WHAT has been produced, normally by WHO
(in order to provide a point of contact)\
(for help see
[template](../../../Developers/Projects/ProjectTaskPageTemplate))\

### Expected

-   A pure python webserver capable of being used as a standalone server
    relatively easily\

### Actual

(for help see
[template](../../../Developers/Projects/ProjectTaskPageTemplate))

-   Code - *what does it do, where is it?*\
-   Reports - *where is it, who wrote it, what was it about, when?*\
-   *Presentation - where is it, where was it presented, what was it
    about, who presented it, when?*\
-   Events - *eg The Brussels open space event*

Note: Especially with speculative tasks,actual outputs may be
substantially different from expected.\

### Realistic possibilities arising as a result of activity on this task

Add speculation as it becomes apparent as realistic. Can be related to
usage or future development.\

Related Tasks
-------------

### Tasks that directly enable this task (dependencies) 

-   PTP : WebServer (for help see
    [template](../../../Developers/Projects/ProjectTaskPageTemplate))

### Sub Tasks

-   If appropriate add subtask descriptions here. (for help see
    [template](../../../Developers/Projects/ProjectTaskPageTemplate))
-   Each subtask here should ideally be a link to a project task page
    for that project
-   It would be *nice* but not mandatory to note the subtask status
-   For small subtasks, it **IS** acceptable to merely have subtasks as
    bullet points with the sort of information you\'d put on a project
    task page, but for which it seems overkill to create a project task
    page for. (It can always become a full PTP later on)\

Task Log
--------

***When a task is running, then this is where most updates will
occur.*** **(for help see
[template](../../../Developers/Projects/ProjectTaskPageTemplate) for
what goes here, level of terseness and content)***\
\
*

-   Created the PTP page for the project Michael. April 14th 2007. Time
    spent 1 hour

Discussion
----------

Comments ? :-)\

\
