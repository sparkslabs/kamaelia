---
pagename: Developers/Projects/WebClient
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: WebClient
============================

**Description**
---------------

::: {.boxright}
**Status:** Running - Looking to add Basic Authentication\
**Current Developers:** Michael Sparks\
**Current \"inflight\" dev location:**
Kamaelia.Protocol.HTTP.HTTPClient\
**Start Date:** July 2006\
**Major Milestone date:** Met by Ryan (Google Summer of Code deadline -
August 2006)\
**Expected End Date:** na\
**End Date:** na\
**Date this page last updated:** December 27th 2006\
**Estimated effort so far:** X+1/4
:::

The components created by this task are targetted as being the basic of
web clients.\
\
A developer will be able to embed a web client into their application.
Specifically this means they will be able to request objects from HTTP
Servers for processing/handling and acting upon.\
\
The original version of this code was developed by Ryan Lothian as part
of his work on Google\'s summer of code 2006. The current context for
continuing development (hence this page) is to provide tools for
collecting RSS/Atom feeds over HTTP and then doing funky things with the
results. Specifically [I](/Michael) have a need to publish an
authenticated RSS feed of incoming requests on sourceforge, be able to
download them, and then send out registration emails from another
server. [This isn\'t hard](/Cookbook/HTTPClient) despite how it might
sound, except we need authentication adding.\
\
A key benefit of this work is that it allows Kamaelia systems to publish
data to (push) and recieve data from (pull) from the web world. A fun
example would be a \"publish picture to blog/flickr\" from the
whiteboard.\

Inputs
------

Task Sponsor: Michael Sparks

Task Owner: Michael Sparks

Developers involved in the task at some point\

-   Ryan Lothian (original developer)\
-   Michael Sparks

Users:

-   Michael Sparks

Interested third parties

-   *LLUP people ?*\

Requirements

-   Ryan Lothian - There MUST be a component that can download a given
    URL (done by Ryan)
-   Ryan Lothian - There MUST be a component that can download URLs sent
    to its inbox (done by Ryan)
-   Ryan Lothian - It should be possible to make POST based requests
    (done by Ryan I believe - needs checking)
-   Michael Sparks - It should be possible to make requests to sites
    with basic authentication **- TODO**\

**Relevant Influencing factors:**\

-   *Ryan wanted to be able to download and upload bit torrent tracker*
    files from/to a webserver\

Outputs
-------

### Expected

-   This page was created after the fact, so it details actual outputs
    rather than expected.\

### Actual

-   Code - /Code/Python/Kamaelia/Kamaelia/Protocol/HTTP/HTTPClient.py\
-   [Cookbook page](/Cookbook/HTTPClient)

### Realistic possibilities arising as a result of activity on this task

The ability to bring in data from HTTP based systems (normally websites)
into running Kamaelia systems.\

Related Tasks
-------------

### Tasks that directly enable this task (dependencies) 

-   TCP client side of Internet subsystem (inc Selector, CSA, etc)\

### Sub Tasks

-   **TODO:** Add in basic authentication (added by Michael, December
    2006)\

Task Log
--------

-   Ryan - Google Summer of Code 2006 - Created initial working versions
    of a useful web client.
-   **Output:** September 2006 - Included in Kamaelia 0.5.0 release\
-   Michael - December 27th 2006 - Created the PTP page, added links
    regarding previous work
-   **Output:** Michael - December 27th 2006 - Created the HTTPClient
    cookbook page.
-   Michael - December 27th 2006 - Added subtask (handle basic
    authentication)\

Discussion
----------

*Anything that doesn\'t fit above fits in here.*

\-- Michael Sparks, December 2006

**Basic Authentication RFC:** <http://www.faqs.org/rfcs/rfc2617.html>

Basic Authentication seems to be suprisingly trivial, and insecure.
Essentially, to create an appropriate basic authentication header, the
necessary python is:

>     >>> import base64
>     >>> "Authorization: Basic %s" % base64.encodestring("Username:password")
>     'Authorization: Basic VXNlcm5hbWU6cGFzc3dvcmQ=\n'

Figuring out the \"best\" place to put this in Ryan\'s code is less than
obvious however\... (I\'ll put it somewhere convenient first)\

Later on\...\
\
OK, added a basic initial patch to SingleShotHTTPClient - specifically
you can now pass in an \"extraheaders\" parameter which you can use to
define extra headers (shockingly) for adding to the request.\
\
This allows me to take an application like this:\

>     Pipeline(
>         ConsoleReader(eol=""),
>         SimpleHTTPClient(),
>         ConsoleEchoer(),
>     ).run()

And create an authenticated request stream as follows:\

>     def AuthenticatedRequestStream(user, passwd):
>         auth = "Basic %s" % base64.encodestring("%s:%s" % (user,passwd))[:-1]
>         def AuthRequest(line):
>             request = {"url":line,
>                        "extraheaders": {"Authorization": auth},
>                       }
>             return request
>         return AuthRequest
>
>     Pipeline(
>         ConsoleReader(eol=""),
>         PureTransformer(AuthenticatedRequestStream("Username", "password")),
>         SimpleHTTPClient(),
>         ConsoleEchoer(),
>     ).run()

There\'s a lot going on here, so let\'s step back a second.\
**\
What\'s going into SimpleHTTPClient?\
**\
Well, it\'s getting dictionaries, and they look like this:\

>     { "url": "http://some.site.com/bla",
>       "extraheaders: {
>                "Authorization" : "Basic VXNlcm5hbWU6cGFzc3dvcmQ="
>       }
>     }

However, what is going into the PureTransformer is simply a string that
looks like this:\

>     "http://some.site.com/bla"

PureTransformer takes a function, and applies it to every thing it
recieves. So,\"clearly\" that function is transforming this:\

>     "http://some.site.com/bla"

Into this:\

>     { "url": "http://some.site.com/bla",
>       "extraheaders: {
>                "Authorization" : "Basic VXNlcm5hbWU6cGFzc3dvcmQ="
>       }
>     }

Based on this, we have to surmise that this function call:\

>     AuthenticatedRequestStream("Username", "password")

Is in fact returning a ***function*** that performs this transform which
the PureTransformer can then use.\
\
In fact what it\'s doing is just that - it performs the transform that
turns the username/password into the authorization code, then returns a
function that embeds that value and the supplied value to the user. If
we look a the function definition we this is exactly what\'s happening.
At first glance that does (admittedly) look a little hairy!\
\
\
