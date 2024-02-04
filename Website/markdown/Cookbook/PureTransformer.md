---
pagename: Cookbook/PureTransformer
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Cookbook: PureTransformer
=========================

A number of components have a common format - specifically they take
every piece of data they receive, transform it somehow, and pass the
data on. Take for example this exampe from the [HTTPClient
page](../../../Cookbook/HTTPClient):

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

In the example above, the important part of the example is highlighted
**red** the common parts of the components are highlight in *green*.
Clearly this amount of boiler plate code actually hides what\'s actually
going on here. As a result the PureTransformer component exists.\

To show how this works, we\'ll leave the important part of the above
example red, but show the shorter version here:

>     import feedparser
>     import pprint
>     import Axon
>     from Kamaelia.Chassis.Pipeline import Pipeline
>     from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
>     from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
>     from Kamaelia.Util.PureTransformer import PureTransformer
>
>     Pipeline(
>         ConsoleReader(eol=""),
>         SimpleHTTPClient(),
>         PureTransformer(feedparser.parse), # Feedparser
>         PureTransformer(pprint.pformat),   # PrettyPrinter
>         ConsoleEchoer(),
>     ).run()

The biggest downside of the PureTransformer is that you sometimes lose
the *intent* behind a component due to the reused name. As a result,
creating a prefab is sometimes a nice idea. What\'s a prefab? It\'s
simply a function !\
\

Using a Prefab to show Intent
-----------------------------

>     import feedparser
>     import pprint
>     import Axon
>     from Kamaelia.Chassis.Pipeline import Pipeline
>     from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
>     from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
>     from Kamaelia.Util.PureTransformer import PureTransformer
>
>     def Feedparser(): return PureTransformer(feedparser.parse)
>     def PrettyPrinter(): return PureTransformer(pprint.pformat)
>      
>     Pipeline(
>         ConsoleReader(eol=""),
>         SimpleHTTPClient(),
>         Feedparser(),
>         PrettyPrinter(),
>         ConsoleEchoer(),
>     ).run()

The nice thing here is we now have the best of both worlds - the code in
the pipeline shows the intent, whereas the code performing the
transforms now doesn\'t contain any repetition. The other nice thing
about doing things this way is that you gain correct shutdown handling
for free at the same time! :-)\

\-- Michael Sparks, December 2006\
\
