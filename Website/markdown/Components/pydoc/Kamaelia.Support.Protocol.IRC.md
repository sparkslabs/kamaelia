---
pagename: Components/pydoc/Kamaelia.Support.Protocol.IRC
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Support](/Components/pydoc/Kamaelia.Support.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Support.Protocol.html){.reference}.[IRC](/Components/pydoc/Kamaelia.Support.Protocol.IRC.html){.reference}
=======================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [Kamaelia IRC Support Code](#16){.reference}
    -   [Core functions](#17){.reference}
        -   [informat(text,defaultChannel=\'\#kamtest\')](#18){.reference}
        -   [outformat(data,
            defaultChannel=\'\#kamtest\')](#19){.reference}
    -   [Utility functions](#20){.reference}
        -   [channelOutformat(channel)](#21){.reference}
        -   [channelInformat(channel)](#22){.reference}
    -   [Open Issues](#23){.reference}
:::

::: {.section}
Kamaelia IRC Support Code {#16}
=========================

This provides support for
[Kamaelia.Protocol.IRC](/Components/pydoc/Kamaelia.Protocol.IRC.html){.reference}.\*

Specifically it provides 2 core functions and 2 utility methods.

::: {.section}
[Core functions]{#core-functions} {#17}
---------------------------------

::: {.section}
### [informat(text,defaultChannel=\'\#kamtest\')]{#informat-text-defaultchannel-kamtest} {#18}

Summary - Puts a string input into tuple format for IRC\_Client.
Understands irc commands preceded by a slash (\"/\"). All other text is
formatted such that sending it would send the message to the default
channel.

Detail - If the text starts with a \"/\" it is treated as a command.
Informat understands some specific commands which it helps you format
for sending to the IRCClient. The commands it understands are:

``` {.literal-block}
QUIT
PRIVMSG
MSG
NOTICE
KILL
TOPIC
SQUERY
KICK
USER
ME
```

For commands it doesn\'t recognise, it makes a guess at how to forward
it.

If you send it text which does NOT start with \"/\", it is assumed to be
badly formatted text, intended to be sent to the current default
channel. It is then formatted appropriately for sending on to an
IRC\_Client component.

For an example of usage, see Examples/TCP\_Systems/IRC/BasicDemo.py
:::

::: {.section}
### [outformat(data, defaultChannel=\'\#kamtest\')]{#outformat-data-defaultchannel-kamtest} {#19}

Takes tuple output from IRC\_Client and formats for easier reading If a
plaintext is received, outformat treats it as a privmsg intended for
defaultChannel (default \"\#kamtest\").

Specific commands it understands and will make a an attempt to format
appropriately are:

``` {.literal-block}
PRIVMSG
JOIN
PART
NICK
ACTION
TOPIC
QUIT
MODE
```

It will also identify certain types of errors.

For an example of usage, see Examples/TCP\_Systems/IRC/BasicDemo.py
:::
:::

::: {.section}
[Utility functions]{#utility-functions} {#20}
---------------------------------------

::: {.section}
### [channelOutformat(channel)]{#channeloutformat-channel} {#21}

Creates a customised outformat function with defaultChannel predefined
to channel. (ie Returns a lambda)
:::

::: {.section}
### [channelInformat(channel)]{#channelinformat-channel} {#22}

Creates a customised informat function with defaultChannel predefined to
channel. (ie Returns a lambda)
:::
:::

::: {.section}
[Open Issues]{#open-issues} {#23}
---------------------------

Should these really be components rather than helper functions?
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
