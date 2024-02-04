---
pagename: Developers/CodingConventionsNaming
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Developers/CodingConventionsNaming
==================================

\

::: {.boxright}
This page consolidates [the discussion on the google groups regarding
this
topic](http://groups.google.com/group/kamaelia/browse_frm/thread/dd2a717e1d137e98#).
:::

In many respects, a significant chunk of Kamaelia is actually about
conventions around ensuring documentation is possible and natural. Matt
did actually write up some documentation guidelines, which I then\
editted and things got tweaked. [These can be found
here.](/DocumentationGuidelines)  Similarly, there is some basic
guidance on naming of things and how they\'ll be used in the page
describing a possible [notation for visualising Axon/Kamaelia
systems](/Docs/NotationForVisualisingAxon).\
\
However, it may be useful to go through some basic points on conventions
that get used.\

Whitespace
----------

4 spaces.\*\*\* No tabs \*\*\*\
No mixing of tabs and indents.\
There\'s highly pragmatic reasons for this I can go into, but for now
let\'s just say tabs have no place in Kamaelia :-)\

imports
-------

First of all, divide this into 3 main sets of lines of the form:\
\* \"import Foo\"\
\* \"from Axon. import\
\* \"from Kamaelia. import\
\
Never use:\
from foo import \*\

Unless you \*know\* that all the symbols exported by foo are expected to
be used. (this is \_very\_ rare)\

Naming of things
----------------

### Naming Components

Components should use CamelCaseWording. (though single word names - like
\"Backplane\" are fine). Names of things should be clear in what they
do. Some of the complaints about names in the earlier thread are very
valid, and worth bearing in mind.\

### Naming Boxes

Components SHOULD declare that they have the following 4 boxes:\
\* inbox - We expect to generally expect the data we work on here.\
\* control - we expect shutdown style messages here.\
\
\* outbox - If your component produces output, it should go here.\
\* signal - when you want to send shutdown messages (of various kinds)
they should get sent here.\
\

If you do not include these boxnames, the component cannot be used
inside a Pipeline. The vast majority of components tend to be able to
work using these default 4 names.\
\
Additional boxnames should always be lower case.\
\
If you do not expect anyone \_outside\_ the component to connect to an
inbox or outbox the component has, then the inbox and outbox name should
start with an underscore. These sorts of boxes are usually used by a
parent component to talk to subcomponents. For a visual example, see the
\"Notation\" link above.\
\
Boxnames which are not any of the defaults should indicate what sort of
thing is sent to them and why (insofar that\'s sensible).\
\
Whilst you can declare boxes this way\...\
\
class Foo(Axon.Component.component):\
Inboxes = \[\"inbox\", \"control\", \"imageupdate\"\]\
Outboxes = \[\"outbox\", \"signal\", \"debuglog\"\]\
\
\... since actually the key thing is Inboxes and Outboxes needs to be an
iterable that returns strings, it is preferable that it be a dictionary,
so that the documentation system can pick things up - this allows
someone introspecting a component to understand what each box is for:\
\
class Foo(Axon.Component.component):\
Inboxes = {\
\"inbox\" : \"what sort of message we expect here & why\",\
\"control\" : \"what sort of message we expect here & why\",\
\"imageupdate\" : \"what sort of message we expect here & why\",\
}\
Outboxes = {\
\"outbox\" : \"what we send here and why\",\
\"signal\" : \"what we send here and why\",\
\"debuglog\" : \"what we send here and why\",\
}\
\
Note the trailing commas on the last item in each pair. This is\
deliberate.\

Use of Boxes
------------

### 

If a box is not linked, it has no default storage. This means sending to
an outbox like this:

self.send(\"debug message\", \"debug\_log\")\
\
Will not result in messages piling up - they\'ll be thrown away unless
the box is linked up.\

Initialisation Issues
---------------------

This has evolved over the course of Kamaelia. There are 3 approaches you
will see in Kamaelia\'s codebase. 1 should be completely eradicated by
now, the other 2 are in a transition period, since one is an improvement
on the other. I\'ll also note a bug.\
\
Buggy/broken/never ever do:\
\
class Foo(Axon.Component.component):\
def \_\_init\_\_(self, arg1, arg2, arg3):\
Axon.Component.component.\_\_init\_\_(self) \<\-\-\-- broken\
self.arg1 = arg1\
self.arg2 = arg2\
self.arg3 = arg3\
\
Very old, deprecated to the extent I think of it as a bug: (will be
broken in esoteric circumstances)\
\
def \_\_init\_\_(self, logfile = \"greylist.log\", debuglogfile =\
\"greylist-debug.log\"):\
self.\_\_super.\_\_init\_\_() \<\-\-\-\-\-\-\-- This is the bit
deprecated.\
self.logfile = logfile\
self.debuglogfile = debuglogfile\
self.inbox\_log = \[\]\
self.line = None\
\
Older, deprecated, but not a bug:\
\
class MailHandler(Axon.Component.component):\
def \_\_init\_\_(self, logfile = \"greylist.log\", debuglogfile =\
\"greylist-debug.log\"):\
super(MailHandler, self).\_\_init\_\_() \<\-\-\-\-\-\-\-- preferable\
self.logfile = logfile\
self.debuglogfile = debuglogfile\
self.inbox\_log = \[\]\
self.line = None\
\
Modern approach, which is much more preferable:\
\
class MailHandler(Axon.Component.component):\
logfile = \"greylist.log\"\
debuglogfile = \"greylist-debug.log\"\
def \_\_init\_\_(self,\*\*argd): \<\-\-- Note, completely offloaded\
the value\
super(MailHandler, self).\_\_init\_\_(\*\*argd) \<\-\-\-- Best\
self.inbox\_log = \[\]\
self.line = None\
\
It\'s worth noting that these last 2 mail handler definitions work the
same way. You can still do this:\
\
MailHandler(logfile = \"/var/log/mail.log\", debug = \"/tmp/
maildebug.log\")\
\
But the latter option also allows this:\
\
class MyMailHandler(MailHandler):\
logfile = \"/var/log/mail.log\"\
debuglogfile = \"/tmp/maildebug.log\"\

Naming/Use of Subcomponents
---------------------------

In the past this has been a matter of \"just use the components you want
to use as subcomponents\". However, similar to initialisation above this
has evolved.\
\
Suppose your component creates and uses a number of subcomponents, you
could do this:\
\
from Kamaelia.Frob import Frobnicator\
from Kamaelia.Wotsits import Cruncher\
from Kamaelia.Smash import Smasher\
\
def \_\_init\_\_(\...)\
\...\
self.frobber = Frobnicator(\...)\
self.smashy = Smasher(\...)\
self.muncher = Cruncher(\...)\
\# and then later on link the components up inside main() once the\
component is started.\
\
This is OK and we\'ve done this for years, but there\'s something much\
nicer you can do:\
\
import Kamaelia.Frob\
import Kamaelia.Wotsits\
import Kamaelia.Smash\
\
class MyComponent(Axon.Component.component):\
Frobnicator = Kamaelia.Frob.Frobnicator\
Cruncher = Kamaelia.Wotsits.Cruncher\
Smasher = Kamaelia.Smash.Smasher\
def \_\_init\_\_(\...)\
\...\
self.frobber = self.Frobnicator(\...)\
self.smashy = self.Smasher(\...)\
self.muncher = self.Cruncher(\...)\
\# and then later on link the components up inside main() once\
the component is started.\
\
On the surface of things, this looks like it introduces more complexity
for no benefit. In practice it introduces a huge new level of abilities,
which you can see used in the greylisting code.\
\
Snipping out the key part that benefits:\
\
class GreylistServer(MoreComplexServer):\
port = config\[\"port\"\]\
class TCPS(TCPServer):\
CSA = NoActivityTimeout(ConnectedSocketAdapter,\
timeout=config\[\"inactivity\_timeout\"\],\
\
debug=False)\
class protocol(GreyListingPolicy):\
servername = config\[\"servername\"\]\
serverid = config\[\"serverid\"\]\
smtp\_ip = config\[\"smtp\_ip\"\]\
\
What you\'ll see here is that this subclasses an existing component
called (rather unimaginatively) MoreComplexServer. However, it overrides
how the server listens for connections, by changing the what self.TCPS
would refer to. Specifically it creates a new class called TCPS, which
subclasses TCPServer in order to change how connections are handled.\
\
Quite literally it allows you to delve deep inside components in the
tree, rummage around and change the one little detail that needs
changing to support the thing you need - in this case it was to add an
inactivity timeout to connected sockets created by the TCP
server/listener component inside the server factory.\
\
In the example above, this would mean someone could do this:\
import Kamaelia.Frob\
import Kamaelia.Wotsits\
import Kamaelia.Smash\
\
class ShinyComponent(MyComponent):\
class Frobnicator(Kamaelia.Frob.Frobnicator):\
\# local overrides\
class Cruncher(Kamaelia.Wotsits.Cruncher):\
\# local overrides\
class Smasher(Kamaelia.Smash.Smasher):\
\# local overrides\
\
And whilst that might seem overkill, it can certainly be useful. It\'s
the sort of change you\'d make to code though once it was all working
and known useful.\

Names of Variables
------------------

you should not use globals. Ever. If you must, please look at the STM\
code.\
\
variables containing things you expect to be constant should be\
UPPERCASE\
\
variables should be lowercase\
attributes should be lowercase\
\
If it\'s clearer lowercase can mean\
\"lowercaseStartingPhraseLikeThisIfYouMust\".\
\
Variables should have a good clear name reflecting use. When in a list
comprehension, use x,y,z (ideally) as the loop values - eg:\
\
items = \[ (x,y) for x,y in someList if x == y \]\
\
In a loop where you\'re interested in values, do this sort of name:\

> for item in items: \# Note the plural\...\
> for person in people:\

\
If just looping over numbers:\
for i in xrange(100)\
\
If you are looping over a generator, waiting for it to finish (cf what
happens in some pygame components), you\'re not actually caring what the
value is. If that\'s the case make this explicit by using the variable
name \"\_\". eg:\

> for \_ in self.waitBox(\"control\"): yield 1\

\
There are better ways of handling this now (see the greylister for an
example of better practice), but this is the legacy approach and shows
the one context where that name is useful.\

Naming of Methods 
-----------------

Method names should follow the same rules as variables.\
\
Unlike \"normal\" python code, you should NOT need to ever do something
like this:\
def \_shutdown(self):\
\
ie you should NOT ever need to have a method name with a leading
underscore. The reason for this is because it is defined as bug for
someone to do this\...\
mycomponent = SomeComponent( \....)\
mycomponent.doSomething()\
\
\... except in \*extraordinarily\* few cases.\
\
\
Since I\'ve referenced it a few times, the greylister is here:
https://kamaelia.svn.sourceforge.net/svnroot/kamaelia/branches/private\_MPS\_Scratch/Apps/Kamaelia-Grey/App/greylisting.py\
\
\... and it shows a number of points which are best practice.\
\
I think I\'ll leave this at that for now, but what haven\'t I covered?\
\
\* I haven\'t covered *behaviour* of initialisation, running & shutdown\
\* I haven\'t covered communication\
\* I haven\'t covered that the \"three callback form\" is now completely
and utterly deprecated. It\'s turned out to be unnecessary in practice
and tends to just make code harder to work with. Therefore modern
components should NOT have the following 3 methods:\
def initialiseComponent(self):\
def mainBody(self):\
def closeDownComponent(self):\
\
And a component SHOULD have the following method:\
def main(self):\
\
And is generally recommend to have the following ones:\
def \_\_init\_\_(self, \...):\
def shutdown(self):\
def main(self):\
def stop(self): \# should handle being called repeatedly safely\
\
Regarding the points I haven\'t covered here - which largely relate to
**behaviour.**\

Other people, please do jump in with where you feel things have worked
well\...\
\

Michael, May 2008
