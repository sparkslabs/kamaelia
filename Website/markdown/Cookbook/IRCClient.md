---
pagename: Cookbook/IRCClient
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Cookbook: IRCClient 
===================

The Interface
-------------

The IRCClient module provides an inbox/outbox interface to IRC. Call
SimpleIRCClientPrefab to obtain a connection to an IRC server.\
\

Sending messages
----------------

Send tuples in the form \*(cmd, \[arg1\] \[,arg2\] \[,arg3\...\])\* to
SimpleIRCClientPrefab\'s \"inbox\". \*cmd\* should be an IRC command
specified in RFC 1459 or RFC 2812. The first parameter specified by the
RFCs should be \*arg1\*, the second should be \*arg2\*, and so on.
Example messages to \"inbox\"::\
\

-   (\'NICK\', \'Zorknpals\')
-   (\'USER\', \'jlei\', \'nohost\', \'noserver\', \'Kamaelia IRC
    Client\')
-   (\'JOIN\', \'\#kamaelia\')
-   (\'PRIVMSG\', \'\#kamtest\', \'hey, how\'s it going?\')
-   (\'TOPIC\', \'\#cheese\', \"Mozzerella vs. Parmesan\")
-   (\'QUIT\')
-   (\'QUIT\', \"Konversation terminated!\")
-   (\'BERSERKER\', \"Lvl. 10\")

\
Note that \"BERSERKER\" is not a recognized IRC command. IRC\_Client
will not\
complain about this, as it treats commands uniformly, but you might get\
an error 421, \"ERR\_UNKNOWNCOMMAND\" back from the server.\
\
\

### Sending CTCP commands

IRC\_Client also handles a few CTCP commands:\
\
:ACTION:\
(\"ME\", channel-or-user, the-action-that-you-do).\
:MSG:\
If you use the outformat function defined here, \'MSG\' commands are\
treated as \'PRIVMSGs\'.\
\
No other CTCP commands are implemented.\
\
\

A simple client that logs in
----------------------------

\...and spams the channel \#kamtest with 10 \"Hello world\" messages.
(It\'s okay because no one else is ever on this channel)\
\

>     class Spammer(component):
>         def main(self):
>             """spams channel #kamtest"""
>             self.send(("NICK", "TheKamaeliaBot"))
>             self.send(("USER", "KamaeliaIRC", "stuff", "stuff", "Kamaelia IRC tester"))
>             self.send(("JOIN", "#kamtest"))
>         for _ in range(10):
>             self.send(("PRIVMSG", "#kamtest", "Hello world"))
>             yield 1
>
>     Pipeline(Spammer(), SimpleIRCClientPrefab()).run()

\
Now you will want to receive messages too, so your client isn\'t doomed
to be a spammer. Lucky for you, SimpleIRCClientPrefab transmits IRC
messages it receives in the form (cmd, sender, receiver, anything else).
Simply link your component up to its \"outbox\" to receive these
messages.\
\
\
\

Logger
------

Logs in to a channel and writes all IRC traffic it hears to a text
file.\

    from Kamaelia.File.Writing import SimpleFileWriter
    from Kamaelia.Chassis.Graphline import Graphline
    from Axon.Component import component
    import IRCClient

    class BasicLogger(component):

        Outboxes = {"irc" : "to IRC, for user responses and login",
                    "outbox" : "What we're interested in, the traffic over the channel",
                    "signal" : "Shutdown handling in the future",
                    }

        def __init__(self, channel, name, formatter=IRCClient.outformat):
            super(BasicLogger, self).__init__()
            self.channel = channel
            self.format = formatter 
            self.name = name
            
        def login(self):
            """registers with the IRC server"""
            self.send(("NICK", self.name), "irc")
            self.send(("USER", self.name, self.name, self.name, self.name), "irc")
            self.send(("JOIN", self.channel), "irc")
            
        def main(self):
            "Main loop"
            self.login()
            while True:
                yield 1 
                while self.dataReady("inbox"):
                    data = self.recv("inbox")
                    formatted_data = self.format(data)
                    if formatted_data:
                        self.send(formatted_data, "outbox")
                        self.respondToPings(data) 

        def respondToPings(self, msg):
            if msg[0] == 'PING':
                self.send(('PONG', msg[1]), 'irc')
                self.send("Sent PONG to %s \n" % msg[1], "outbox")


    #now define a prefab to wire everything up

    def Logger(channel, name, server='irc.freenode.net'):
        return Graphline(irc = IRCClient.SimpleIRCClientPrefab(server),
                         logger = BasicLogger(channel, name),
                         log = SimpleFileWriter("%s_log.txt" % channel.lstrip('#')),
                         linkages = {("logger", "irc") : ("irc", "inbox"),
                                     ("irc", "outbox") : ("logger", "inbox"),
                                     ("logger", "outbox") : ("log", "inbox"),
                                     }

                         )

    Logger('#test', 'coolLoggerDude').run() #we're assuming that no other user has this nickname! There's no error checking otherwise. 

\
That\'s all there is! Have fun using the IRC components!\
\
