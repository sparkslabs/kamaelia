---
pagename: Cookbook/HTTPClient
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Cookbook: HTTPClient
====================

The web client support in Kamaelia currently comes in two forms:

-   A single shot web client
-   A reusable web client

As well as basic examples for these two, this page also shows:\

-   How to build a basic RSS client (well, actually any feed [the
    universal feedparser](http://feedparser.org/) will parse, which is a
    lot more than just RSS)

\

The Single Shot Web Client 
--------------------------

>     from Kamaelia.Chassis.Pipeline import Pipeline
>     from Kamaelia.Protocol.HTTP.HTTPClient import *
>     from Kamaelia.Util.Console import *
>
>     Pipeline(
>         SingleShotHTTPClient("http://kamaelia.sourceforge.net/Home"),
>         ConsoleEchoer(),
>     ).run()

As you can see, this component takes a single argument, goes off,
fetches it, and spits it out of it\'s main outbox \"outbox\". If we run
this, we get the following:\

>     ~> ./test.py

As you can see this is not as simple an object as you might have
expected. Rather than just being passed the data, you are passed an
object. You\'re not really expected to use this, but it is useful to
know about.\

The Reusable Web Client
-----------------------

::: {.boxright}
**NOTE:** The URLs passed over to the SimpleHTTPClient **MUST NOT**
include a newline, or else you will be left wondering why your code
doesn\'t work. This is why this example ensures that the ConsoleReader
strips the carriage return from the end of line!
:::

\

>     from Kamaelia.Chassis.Pipeline import Pipeline
>     from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
>     from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
>
>     Pipeline(
>         ConsoleReader(eol=""),
>         SimpleHTTPClient(),
>         ConsoleEchoer(),
>     ).run()

\
As you can see, this time we have a console reader - where we\'re
expected to type URLs. These URLs are passed to the SimpleHTTPClient
which goes off, grabs the URLs and dumps them out of it\'s main outbox
\"outbox\". If we runs this, we get the following:\

>     ~> ./PipedHTTP.py
>     >>> http://kamaelia.sourceforge.net/Home
>     >>> 
>     .bodytext {
>         font-size: 10pt;
>     ...snip...
>
>     >>>

As you can see, this version of the system simple sends the body of the
HTTP response to its main outbox \"outbox\". If you want more
information (such as response headers etc), you have to use these
components differently. However as basic examples hopefully these are
sufficient :-)\
\

Feed Fetching, Parsing, Printing, Displaying
--------------------------------------------

::: {.boxright}
Note: This example can be simplified - see [Cookbook
PureTransformer](/Cookbook/PureTransformer)
:::

This is a more substantial, but relatively basic example.\

>     import feedparser
>     import pprint
>     import Axon
>     from Kamaelia.Chassis.Pipeline import Pipeline
>     from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
>     from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
>
>     class Feedparser(Axon.Component.component):
>         def main(self):
>             while 1:
>                 while self.dataReady("inbox"):
>                     data = self.recv("inbox")
>                     parseddata = feedparser.parse(data)
>                     self.send(parseddata, "outbox")
>
>                 if not self.anyReady():
>                     self.pause()
>                 yield 1
>
>     class PrettyPrinter(Axon.Component.component):
>         def main(self):
>             while 1:
>                 while self.dataReady("inbox"):
>                     data = self.recv("inbox")
>                     prettified = pprint.pformat(data)
>                     self.send(prettified, "outbox")
>
>                 if not self.anyReady():
>                     self.pause()
>                 yield 1
>
>     Pipeline(
>         ConsoleReader(eol=""),
>         SimpleHTTPClient(),
>         Feedparser(),
>         PrettyPrinter(),
>         ConsoleEchoer(),
>     ).run()

If we run this, we get the following:\

>     ~> ./PipedFeedFetcher.py
>     >>> http://kamaelia.sourceforge.net/cgi-bin/blog/feed.cgi
>     >>> {'bozo': 0,
>      'encoding': 'utf-8',
>      'entries': [{'author': u'Michael',
>                   'guidislink': False,
>                   'id': u'http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1158348609.1',
>                   'link': u'http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1158348609.1',
>     ...
>                   'title_detail': {'base': '',
>                                    'language': None,
>                                    'type': 'text/plain',
>                                    'value': u'How do I register?'},
>                   'updated': u'Fri, 29 Sep 2006 12:11:29 +0000',
>                   'updated_parsed': (2006, 9, 29, 12, 11, 29, 4, 272, 0)},
>                  {'author': u'Michael',
>                   'guidislink': False,
>                   'id': u'http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1148942995',
>                   'link': u'http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1148942995',
>     ...
>                   'updated': u'Mon, 29 May 2006 22:49:55 +0000',
>                   'updated_parsed': (2006, 5, 29, 22, 49, 55, 0, 149, 0)}],
>      'feed': {'author': u'email@example.com',
>               'author_detail': {'name': u'', 'email': u'email@example.com'},
>               'docs': u'http://blogs.law.harvard.edu/tech/rss',
>               'generator': u'Kamaelia 0.1',
>               'generator_detail': {'name': u'Kamaelia 0.1'},
>     ...
>               'updated': u'Wed, 27 Dec 2006 22:23:49 +0000',
>               'updated_parsed': (2006, 12, 27, 22, 23, 49, 2, 361, 0)},
>      'namespaces': {},
>      'version': 'rss20'}
>     >>>

It\'s probably worth noting at this point that you can pretty much use
this then in a similar way to the way [Kamaelia
Macro](/Developers/Projects/KamaeliaMacro) handles multiplexes EIT
information and uses that to trigger events (such as finishing a
transcoding session).\
\
\-- Michael, December 2006\
\
\
\
