---
pagename: Components/pydoc/Kamaelia.Protocol.IRC.IRCClient
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[IRC](/Components/pydoc/Kamaelia.Protocol.IRC.html){.reference}.[IRCClient](/Components/pydoc/Kamaelia.Protocol.IRC.IRCClient.html){.reference}
========================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [Kamaelia IRC Interface](#644){.reference}
    -   [Example Usage](#645){.reference}
    -   [How does it work?](#646){.reference}
        -   [Sending messages over IRC](#647){.reference}
        -   [Sending CTCP commands](#648){.reference}
        -   [Receiving messages](#649){.reference}
    -   [Known Issues](#650){.reference}
:::

::: {.section}
Kamaelia IRC Interface {#644}
======================

IRC\_Client provides an IRC interface for Kamaelia components.

SimpleIRCClientPrefab is a handy prefab that links IRC\_Client and
TCPClient to each other and IRC\_Client\'s \"talk\" and \"heard\" boxes
to the prefab\'s \"inbox\" and \"outbox\" boxes, respectively.
SimpleIRCClientPrefab does not terminate.

The functions informat, outformat, channelInformat, and channelOutformat
can be used to format incoming and outgoing messages.

::: {.section}
[Example Usage]{#example-usage} {#645}
-------------------------------

To link IRC\_Client to the web with console input and output:

``` {.literal-block}
client = Graphline(irc = IRC_Client(),
              tcp = TCPClient(host, port),
              linkages = {("self", "inbox") : ("irc" , "talk"),
                          ("irc", "outbox") : ("tcp" , "inbox"),
                          ("tcp", "outbox") : ("irc", "inbox"),
                          ("irc", "heard") : ("self", "outbox"),
                          })
Pipeline(ConsoleReader(),
         PureTransformer(channelInformat("#kamtest")),
         client,
         PureTransformer(channelOutformat("#kamtest")),
         ConsoleEchoer(),
).run()
```

Note: The user needs to enter:

``` {.literal-block}
/nick aNickName
/user uname server host realname
```

into the console before doing anything else in the above example. Be
quick before the connection times out.

Then try IRC commands preceded by a slash. Messages to the channel need
not be preceded by anything:

``` {.literal-block}
>>> /join #kamtest
>>> /msg nickserv identify secretpassword
>>> /topic #kamtest Testing IRC client
>>> Hello everyone.
>>> /part #kamtest
>>> /quit
```

This example sends all plaintext to \#kamtest by default. To send to
another channel by default, change the arguments of channelInformat and
channelOutformat to the name of a different channel. (E.g. \"\#python\")

For a more comprehensive example, see Logger.py in Tools.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#646}
--------------------------------------

::: {.section}
### [Sending messages over IRC]{#sending-messages-over-irc} {#647}

IRC\_Client accepts commands arriving at its \"talk\" inbox. A command
is a list/tuple and is in the form (\'cmd\', \[arg1\] \[,arg2\]
\[,arg3\...\]). IRC\_Client retransmits these as full-fledged IRC
commands to its \"outbox\". Arguments following the command are per RFC
1459 and RFC 2812.

For example,

-   (\'NICK\', \'Zorknpals\')
-   (\'USER\', \'jlei\', \'nohost\', \'noserver\', \'Kamaelia IRC
    Client\')
-   (\'JOIN\', \'\#kamaelia\')
-   (\'PRIVMSG\', \'\#kamtest\', \'hey, how\'s it going?\')
-   (\'TOPIC\', \'\#cheese\', \"Mozzerella vs. Parmesan\")
-   (\'QUIT\')
-   (\'QUIT\', \"Konversation terminated!\")
-   (\'BERSERKER\', \"Lvl. 10\")

Note that \"BERSERKER\" is not a recognized IRC command. IRC\_Client
will not complain about this, as it treats commands uniformly, but you
might get an error 421, \"ERR\_UNKNOWNCOMMAND\" back from the server.
:::

::: {.section}
### [Sending CTCP commands]{#sending-ctcp-commands} {#648}

IRC\_Client also handles a few CTCP commands:

  --------- -----------------------------------------------------------------------------------------------
  ACTION:   (\"ME\", channel-or-user, the-action-that-you-do).
  MSG:      If you use the outformat function defined here, \'MSG\' commands are treated as \'PRIVMSGs\'.
  --------- -----------------------------------------------------------------------------------------------

No other CTCP commands are implemented.
:::

::: {.section}
### [Receiving messages]{#receiving-messages} {#649}

IRC\_Client\'s \"inbox\" takes messages from an IRC server and
retransmits them to its \"heard\" outbox in tuple format. Currently each
tuple has fields (command, sender, receiver, rest). This method has
worked well so far.

Example output:

::: {.line-block}
::: {.line}
(\'001\', \'heinlein.freenode.net\', \'jinnaslogbot\', \' Welcome to the
freenode IRC Network jinnaslogbot\')
:::

::: {.line}
(\'NOTICE\', \'\', \'jinnaslogbot\', \'\*\*\*Checking ident\')
:::

::: {.line}
(\'PRIVMSG\', \'jlei\', \'\#kamtest\', \'stuff\')
:::

::: {.line}
(\'PART\', \'kambot\', \'\#kamtest\', \'see you later)
:::

::: {.line}
(\'ACTION\', \'jinnaslogbot\', \'\#kamtest\', \'does the macarena\')
:::
:::

To stop IRC\_Client, send a shutdownMicroprocess or a producerFinished
to its \"control\" box. The higher-level client must send a login itself
and respond to pings. IRC\_Client will not do this automatically.
:::
:::

::: {.section}
[Known Issues]{#known-issues} {#650}
-----------------------------

The prefab does not terminate. (?) Sometimes messages from the server
are split up. IRC\_Client does not recognize these messages and flags
them as errors.
:::
:::

------------------------------------------------------------------------

::: {.section}
:::
:::

::: {.section}
Feedback
========

Got a problem with the documentation? Something unclear that could be
clearer? Want to help improve it? Constructive criticism is very welcome
- especially if you can suggest a better rewording!

Please leave you feedback
[here](../../../cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1142023701){.reference}
in reply to the documentation thread in the Kamaelia blog.
:::

*\-- Automatic documentation generator, 05 Jun 2009 at 03:01:38 UTC/GMT*
