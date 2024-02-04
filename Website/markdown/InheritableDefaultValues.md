---
pagename: InheritableDefaultValues
last-modified-date: 2008-10-19
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Inheritable Default Values
==========================

::: {align="right"}
**Making systemic specialisation more declarative**\
:::

This feature was introduced in Axon 1.6.0 (Kamaelia 0.6.0)\
\
The idea behind this is to allow a more compact, declarative way of
defining more complex Kamaelia systems. It stemmed initially from an
observation that two of us wanted to do this:\
\

>     def ReusableSocketAddrServer(port=100,
>                            protocol=EchoProtocol):
>         return ServerCore(protocol=protocol,
>                           port=port,
>                           socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1))

\
Specifically we noticed that we were creating a fair number of factory
functions which only really differed based on on value. The problem we
have here is that this is relatively fragile. Specifically, what happens
if ServerCore adds in extra arguments - do we also update
ReusableSocketAddrServer ? What if we don\'t, does someone else come
along and duplicate our code in order to support those extra arguments?
OK, well we can handle this in python if we use the \*\*argd syntax. If
we do that, we can do that this way:\

>     def ReusableSocketAddr(**argd):
>         argd_local = dict(argd)
>         argd_local["socketOptions"] = (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
>         return ServerCore(**argd_local)

Whilst that\'s maybe more reflective of what we wanted to do, it now
looks rather obscured. We then realised that there is a useful side
effect of python namespaces that we can take advantage of, which is
this:\

self.attribute first of all looks inside the object self. If this is not
found\...

self.attribute looks inside self.\_\_class\_\_ . If that\'s not found,

self.attribute looks inside the parents of self.\_\_class\_\_ all the
way up.

-   This is kinda necessary to make (self.method) work, so it can be
    relied upon.

This means that if we change the base component class to do this:\

>     def __init__(self, **argd):
>          self.__dict__.update(argd)

Then we can do this:\

>     class ReusableSocketAttrServer(ServerCore):
>         socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  

This has a number of advantages over the factory method:\

-   First and foremost it makes it very clear that this is just a
    ServerCore that happens to have different socketOptions.
-   Secondly it means that if the parent component (ServerCore) adds
    extra arguments into the initialiser, we\'ll pick those up
    automagically.
-   Thirdly, it encourages us to provide more things into the class
    namespace, which actually assists with testing, but also makes the
    system more flexible.

For example, suppose the component we\'re using creates components as a
part of it\'s operation, and we want to add tracing to these. Normally
that code would default to looking like this:\
\

>     from import Kamaelia.Internet.TCPServer import TCPServer
>
>     class ServerCore(...):
>     ...
>
>         def initialiseComponent(self):
>     ...
>                 myPLS = TCPServer(listenport=self.listenport)
>
> **Hypothetical File:** ExamplePatch.py\

\
Replacing TCPServer here with our TracedTCPServer would have to look
like this:\
\

>     from Hypothetical import TracedTCPServer
>     import ExamplePatch
>     ExamplePatch.TCPServer = TracedTCPServer
>
> **Hypothetical File:** ExamplePatchUser.py\

The downside of this as well is that this is not particularly targetted,
and leads to the situation where it would be more natural to create a
copy of the code for traced versions. This misses one of the handy
features of what inheritance gives us, which is controlled duplication
of functionality with little twists of functionality. By comparison,
with inheritable default values, we can do this instead:\
\

>     from import Kamaelia.Internet.TCPServer import TCPServer
>
>     class ServerCore(...):
>         TCPS = TCPServer
>         def initialiseComponent(self):
>     ...
>                 TCPServer = self.TCPS
>                 myPLS = TCPServer(listenport=self.listenport)
>
> **Hypothetical File:** ExamplePatch.py\

However, when someone wants to create a traced version they can be far
more to the point. Suppose they have code that looks like this:\
ServerCore(port = 1500, protocol=WhizzyProto1).run()\
\
They can change it over to use the hypothetical TracedTCPServer like
this:\

>     from Hypothetical import TracedTCPServer
>
>     ServerCore(port = 1500, protocol=WhizzyProto1, TCPS=TracedTCPServer).run()
>
> **Hypothetical File:** ExamplePatchUser.py

\
Not only that, but if they wanted to define this as a common thing they
wanted to do, they could do this:\

>     class TracedServerCore(ServerCore):
>          TCPS = TracedTCPServer

Which would then get used:\

>     TracedServerCore(port = 1500, protocol=WhizzyProto1).run()

Whilst this seems theoretical, it was bandied about as a possible idea
for nearly a year until it suddenly became extremely useful -
specifically in the [greylisting code](/KamaeliaGrey.html to allow it to use
inactivity timers on connected sockets, as well as configuration of
protocol handlers in a declarative manner:\

>     class GreylistServer(ServerCore):
>         logfile = config["greylist_log"]
>         debuglogfile = config["greylist_debuglog"]
>         socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
>         port = config["port"]
>         class TCPS(TCPServer):
>             CSA = NoActivityTimeout(ConnectedSocketAdeapter, timeout=config["inactivity_timeout"], debug=False)
>         class protocol(GreyListingPolicy):
>             servername = config["servername"]
>             serverid = config["serverid"]
>             smtp_ip = config["smtp_ip"]
>             smtp_port = config["smtp_port"]
>             allowed_senders = config["allowed_senders"]
>             allowed_sender_nets = config["allowed_sender_nets"] # Yes, only class C network style
>             allowed_domains = config["allowed_domains"]
>             whitelisted_triples = config["whitelisted_triples"]
>             whitelisted_nonstandard_triples = config["whitelisted_nonstandard_triples"]

Since then the idiom has been found to be useful in other scenarios.\
\
It\'s also worth noticing that this also means that the ServerCore code
could be repurposed to work with servers that act in a similar way to
TCPServer. For example, a hypothetical ConnectionBasedUDPListener, could
be created which operated in a similar manner to TCPServer, and then
reused as follows:\

>     class UDPServerCore(ServerCore):
>          TCPS = ConnectionBasedUDPListener

Thereby making it as simple to create connection oriented UDP servers as
it would be to create TCPServers. The only difference between the two
being lack of guarantee of ordering or delivery.\

Downsides?
----------

The clear downside of this is that the signature of your component\'s
generally initialiser becomes this:\

>     def __init__(self, **argd):
>      ...

This in turn puts a greater onus on you as a component writer to
document the arguments to your component in a clearer manner.\
\

But WHY???
----------

This is an implicit thing. **In Kamaelia when syntactic sugar gets
added** (and that\'s precisely what this is), **one of the most common
aims is to aim to move towards a declarative reusable syntax.** After
all, if you consider that the starting point was this:\

>     def ReusableSocketAddrServer(port=100,
>                            protocol=EchoProtocol):
>         return ServerCore(protocol=protocol,
>                           port=port,
>                           socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1))

You\'re actually starting off with something very fragile, especially
considering that if ServerCore changes it\'s configuration, you have to
change this factory function as well.\
\
Secondly, the next approach for dealing with changing
\_\_init\_\_ialiser arguments is to use \*\*argd, you then end up with
something which is a bit perl-ish in structure, and obfuscates what\'s
really going on:\

>     def ReusableSocketAddr(**argd):
>         argd_local = dict(argd)
>         argd_local["socketOptions"] = (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
>         return ServerCore(**argd_local)

However, by switching over to an inheritable default value approach you
gain something which is declarative, picks up new default values from
the base class cleanly and makes it much clearer that actually this
returns objects of this type, just preconfigured in a particular way:\

>     class ReusableSocketAttrServer(ServerCore):
>         socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  

So, by aiming for a syntactic sugar that\'s declarative in nature,
we\'re hopefully making the intent in the system clearer.\

Summary
-------

\
If you want to provide default values for parameters for your
components, and please do, providing them in the form of inheritable
default values will make your components more useful to others. You
don\'t have to do this, and if you find it odd, simply don\'t do this.
However if you do, it would be appreciated by the users of your code.\
\
