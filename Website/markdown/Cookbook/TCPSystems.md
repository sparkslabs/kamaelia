---
pagename: Cookbook/TCPSystems
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Cookbook: Creating TCP Systems
==============================

::: {.boxright}
There are a number of lower down cookbook recipes for TCP systems in
Kamaelia. This cookbook page walks through a small number of techniques
which are useful in creating TCPSystems.\
**Discussion** Please discuss this on [the discussion
page](http://backend.kamaelia.org/Cookbook/TCPSystemsDiscuss) for this
page
:::

One of the earliest systems that Kamaelia was designed for was to build
network systems, specifically scaleable TCP based network servers.\

**An Echo Server**
------------------

One of the more trivial examples of TCP server is the traditional echo
server. On the surface of things echo servers tend to look useless, but
are often extremely useful for simply testing the question \"is this
thing on?\". As a result that\'s why even Skype has something similar!
An echo server takes whatever message it recieves and sends it back to
you.\
\
In Kamaelia building this protocol is relatively easy to do:\

> ::: {align="left"}
>     import Axon
>     from Kamaelia.Chassis.ConnectedServer import SimpleServer
>
>     class Echo(Axon.Component.component):
>         def main(self):
>             while 1:
>                 while self.dataReady("inbox"):
>                     data = self.recv("inbox")
>                     self.send(data, "outbox")
>                 yield 1
>
>     SimpleServer(protocol=Echo, port=1500).run()
> :::
>
> **Example 1:** Basic echo server\

We can then run this and connect back to our server: (locally typed
chars in italics)\

>     # telnet 127.0.0.1 1500
>     Trying 127.0.0.1...
>     Connected to 127.0.0.1.
>     Escape character is '^]'.
>     Hello
>     Hello
>     This
>     This
>     is
>     is
>     a
>     a
>     test
>     test

As you can see this works pretty much you\'d hope - you provide
something that can create protocol handlers to the simple server. When a
connection occurs, the simple server creates an instance, and that
instance recieves data from the socket on its inbox \"inbox\", and any
data it sends to its outbox \"outbox\" is sent to the socket.\

**Shutting Down the Connection inside the Protocol Handler**
------------------------------------------------------------

OK, so that\'s a trivial server, how about something a little more
complex? How about a protocol that when a client connects it runs, sends
a message to the user and then breaks the connection? This is very
similar to a \"message of the day service\" or a finger service.\
\
Well, to do this, we don\'t actually care about looping or waiting for
data, or anything similar and interesting, we can just send messages and
shutdown. Specifically to shutdown, we send a
Axon.Ipc.shutdownMicroprocess message out of our \"signal\" outbox, so a
simple \"message of the day\" server could look like this:\

> ::: {align="left"}
>     import Axon
>     from Kamaelia.Chassis.ConnectedServer import SimpleServer
>
>     message = """\
>     Hello, this is the message of the day
>
>     Bye Bye!
>     """
>
>     class MOTD(Axon.Component.component):
>         def main(self):
>             self.send(message, "outbox")
>             self.send(Axon.Ipc.shutdownMicroprocess(), "signal")
>             print "Shutting down"
>             yield 1
>
>     SimpleServer(protocol=MOTD, port=1501).run()
>
> **Example 2:** Basic server with a message of the day protocol that
> shuts down immediately\
> :::

**Handling a shutdown message from the socket**
-----------------------------------------------

When a client breaks their connection, the protocol handler recieves a
*Kamaelia.IPC.socketShutdown* IPC mesage on it\'s control inbox, which
you can test for in order to determine whether to shutdown or not!
Taking the original echo protocol above and extending it to handle this,
looks like this:\

::: {align="left"}
>     import Axon
>     import Kamaelia.IPC 
>     from Kamaelia.Chassis.ConnectedServer import SimpleServer
>
>     class Echo(Axon.Component.component):
>         def main(self):
>             protocolRunning = True
>             while protocolRunning:
>                 while self.dataReady("inbox"):
>                     data = self.recv("inbox")
>                     self.send(data, "outbox")
>                 while self.dataReady("control"):
>                     data = self.recv("control")
>                     if isinstance(data, Kamaelia.IPC.socketShutdown):
>                         protocolRunning = False
>                 yield 1
>             print "Protocol finished!"
>
>     SimpleServer(protocol=Echo, port=1500).run()
>
> **Example 3:** Server with a protocol that shuts down when it recieves
> notification the socket has shutdown\
:::

OK, so that\'s a relatively simple component - what about a simple
component that sits, waits for a message, and when it gets one, sends
one message in response and also shuts down? Well, this is kinda a
combination of examples 1& 2. In realworld terms, this is very similar
conceptually to the \"finger\" protocol (though not quite :), and has
basic similarities to HTTP as well.\

> ::: {align="left"}
>     import Axon
>     import Kamaelia.IPC 
>     from Kamaelia.Chassis.ConnectedServer import SimpleServer
>
>     class Echo(Axon.Component.component):
>         def main(self):
>             while not self.dataReady():
>                 yield 1
>
>             message = self.recv("inbox")
>             self.send("You sent the message:" + message, "outbox")
>             self.send(Axon.Ipc.shutdownMicroprocess(), "signal")
>             print "Protocol finished!"
>             yield 1
>
>     SimpleServer(protocol=Echo, port=1500).run()
>
> **Example 4:** Server with a protocol that sends a message and shuts
> down when it recieves any message from the connection\
> :::

There\'s a couple of further examples worth looking at here. One is a
protocol that runs and when it recieves a special message - in this case
the word \"shutdown\" - it causes the connection to be shutdown, but
also one that also handles a client disconnection:\

> ::: {align="left"}
>     import Axon
>     import Kamaelia.IPC 
>     from Kamaelia.Chassis.ConnectedServer import SimpleServer
>
>     class Echo(Axon.Component.component):
>         def main(self):
>             protocolRunning = True
>             while protocolRunning:
>                 while self.dataReady("inbox"):
>                     data = self.recv("inbox")
>                     if "shutdown" in data:
>                         protocolRunning = False
>                         self.send(Axon.Ipc.shutdownMicroprocess(), "signal")
>                     else:
>                         self.send("munch"+data, "outbox")
>
>                 while self.dataReady("control"):
>                     data = self.recv("control")
>                     if isinstance(data, Kamaelia.IPC.socketShutdown):
>                         protocolRunning = False
>                 yield 1
>             print "Protocol finished!"
>
>     SimpleServer(protocol=Echo, port=1500).run()
> :::
>
> **Example 5:** Server with a protocol where the client can forcibly
> break the connection or request disconnection\

A final basic example is how to create a server that when a client
connects the server will send a message and shutdown. For this the
client needs to send a serverShutdown message to a serversignal outbox
as well as a shutdownMicroprocess to the signal.\

::: {align="left"}
>     import Axon
>     from Kamaelia.Chassis.ConnectedServer import SimpleServer
>     from Kamaelia.IPC import serverShutdown
>
>     message = """Hello, this is the message of the day
>     Bye Bye!"""
>
>     class MOTD(Axon.Component.component):
>         Outboxes = ["outbox", "signal", "serversignal"]
>         def main(self):
>             self.send(message, "outbox")
>             self.send(serverShutdown(), "serversignal")
>             print "Shutting down"
>             yield 1
>
>     SimpleServer(protocol=MOTD, port=1501).run()
>
> **Example 6:** Server where the server shuts down as soon as the first
> client connects.\
:::

Shared Markov Chain Protocol
----------------------------

For a more fun example, let\'s create a simple server that accepts
connections from users, and is expected to chat to the people who
connect. For extra bonus points, what it will do is take anything
that\'s typed to it, and use this to build up a simple markov chain.
This markov chain will be shared between all connections, and as a
result its dialogue will grow as the number of connections to it grows.\
\
Whilst this sounds complex, the code is relatively simple, and focusses
almost entirely around the markov chain aspects rather than the network
system aspects.\
\
I wrote this as an example of a relatively simple, but non-trivial
network protocol. It creates a server that sits there waiting for
connections. Anything that you type at it updates the markov chain for
anyone/everyone connected. The protocol handler itself could be bolted
into an IRC bot instead so you could have a deranged bot sitting on a
channel which talks vaguely on-topic (but relatively - not totally -
incoherently) most of the time. I thought I\'d blog about it because it
makes quite a nice fun/simple introduction to Kamaelia in it\'s own
special way. The markov chain used is based on the one here. (courtesy
of a google search)\

::: {align="left"}
>     import Axon, random
>     nlnl = '\n', '\n'
>     key = nlnl
>
>     def new_key(key, word):
>        if word == '\n': return nlnl
>        else: return (key[1], word)
>
>     class Chatty(Axon.Component.component):
>        data = {}
>        def updateChain(self, message):
>            key = nlnl
>            for word in message.split():
>                self.__class__.data.setdefault(key, []).append(word)
>                key = new_key(key, word)
>
>        def response(self):
>            key, result, word = nlnl, [], None
>            while word != "\n":
>                word = random.choice(self.__class__.data.get(key, nlnl))
>                key = new_key(key, word)
>                result.append(word)
>            return " ".join(result)
>
>        def main(self):
>            while 1:
>                if self.dataReady("inbox"):
>                    message = self.recv("inbox")
>                    self.updateChain(message)
>                    self.send(self.response(), "outbox")
>                yield 1
>
>     if __name__ == "__main__":
>         from Kamaelia.Chassis.ConnectedServer import SimpleServer
>         SimpleServer(protocol=Chatty, port=1500).run()
>
> **Example 7:** Markov Chain Chat server.\
:::

\
And that\'s pretty much all there is to it. As you\'d imagine (I hope),
a Chatty component is created to handle any accepted connection on port
1500, and anything the user types is received on the inbox \"inbox\",
used to update the class\'s markov chain DB, and then generates a
response to send to the outbox \"outbox\" (meaning it gets sent to the
socket). The upshot is the more people who connect, the more the
database gets updated.\
\
The nice thing about this is that the bulk of the code here focusses on
the logic that\'s desired, not on any networking details. OK, this
example isn\'t ideal because it misses some important things like
shutdown and what happens if the connection disappears, but it also is
interesting because you can test the component in isolation as well:\

>     Pipeline(
>             ConsoleReader(),
>             Chatty(),
>             ConsoleEchoer(),
>     ).run()

Which is a nice thing to be able to do! If you wanted to train the
markov chain server you could also do that as follows:\

>     Pipeline(
>             ReadFileAdaptor("SomeTrainingMaterial"),
>             TCPClient("127.0.0.1", 1500), # assuming localhost
>             ConsoleEchoer(), # May as well see the deranged output :)
>     ).run()

The fun thing about this trainer is that you can see the output from the
markov chain during testing as well :-)\
\
\-- Michael, January 2007\
