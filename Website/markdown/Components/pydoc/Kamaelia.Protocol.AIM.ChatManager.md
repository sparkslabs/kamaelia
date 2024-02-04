---
pagename: Components/pydoc/Kamaelia.Protocol.AIM.ChatManager
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[AIM](/Components/pydoc/Kamaelia.Protocol.AIM.html){.reference}.[ChatManager](/Components/pydoc/Kamaelia.Protocol.AIM.ChatManager.html){.reference}
============================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [ChatManager](/Components/pydoc/Kamaelia.Protocol.AIM.ChatManager.ChatManager.html){.reference}**
:::

-   [AIM Client](#617){.reference}
    -   [How it works:](#618){.reference}
    -   [Example Usage](#619){.reference}
:::

::: {.section}
AIM Client {#617}
==========

Deals with post-login messages from the AIM server, mostly by parsing
them and sending them out to its \"heard\" outbox in a slightly more
useable form. Also sends messages to the server based on commands coming
through its \"talk\" inbox.

::: {.section}
[How it works:]{#how-it-works} {#618}
------------------------------

ChatManager expects to receive FLAPs containing SNACs through its
\"inbox\". It recognizes certain types of SNACs. For these SNACS,
ChatManager parses them, and sends the relevant data out to its
\"heard\" outbox in tuple format. The following lists the SNACs
ChatManager understands and the tuples that it consequently sends out:

  -----------------------------------------------------------------------
  SNAC       DESCRIPTION        TUPLE SENT TO \"heard\"
  ---------- ------------------ -----------------------------------------
  (03, 0b)   Buddy is online    (\"buddy online\", {name: buddy name})

  (04, 07)   Incoming message   (\"message\", sender, message text)
  -----------------------------------------------------------------------

The \"buddy online\" message contains a dictionary instead of just a
text field for the buddy name because this will make it easier to add
more buddy data to a \"buddy online\" message, such as online time or
alias. The server sends this data, but right now ChatManager just
discards it.

ChatManager also understands tuple-based commands sent to its \"talk\"
inbox. The following lists the commands it understands, and the
corresponding actions it takes.

  -----------------------------------------------------------------------
  COMMAND                                         ACTION
  ----------------------------------------------- -----------------------
  (\"message\", recipient\'s screenname, message  Sends instant message
  text)                                           to server (SNAC (04,
                                                  07))

  -----------------------------------------------------------------------
:::

::: {.section}
[Example Usage]{#example-usage} {#619}
-------------------------------

Simple client with a truly horrible interface:

``` {.literal-block}
class AIMHarness(component):
    def main(self):
        self.loginer = LoginHandler('sitar63112', 'sitar63112').activate()
        self.link((self.loginer, "signal"), (self, "internal inbox"))
        self.addChildren(self.loginer)
        while not self.dataReady("internal inbox"): yield 1
        self.oscar = self.recv("internal inbox")
        queued = self.recv("internal inbox")
        self.unlink(self.oscar)

        self.chatter = ChatManager().activate()
        self.link((self.chatter, "heard"), (self, "outbox"), passthrough=2)
        self.link((self, "inbox"), (self.chatter, "talk"), passthrough=1)
        self.link((self.chatter, "outbox"), (self.oscar, "inbox"))
        self.link((self.oscar, "outbox"), (self.chatter, "inbox"))
        self.link((self, "internal outbox"), (self.chatter, "inbox"))
        while len(queued):
            self.send(queued[0], "internal outbox")
            del(queued[0])
        while True:
            yield 1

def tuplefy(data):
    data = data.split()
    if len(data) > 1:
        data = ("message", data[0], " ".join(data[1:]))
        return data

Pipeline(ConsoleReader(),
         PureTransformer(tuplefy),
         AIMHarness(),
         ConsoleEchoer()
        ).run()
```
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[AIM](/Components/pydoc/Kamaelia.Protocol.AIM.html){.reference}.[ChatManager](/Components/pydoc/Kamaelia.Protocol.AIM.ChatManager.html){.reference}.[ChatManager](/Components/pydoc/Kamaelia.Protocol.AIM.ChatManager.ChatManager.html){.reference}
============================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class ChatManager(SNACExchanger) {#symbol-ChatManager}
--------------------------------

ChatManager() -\> new ChatManager component.

::: {.section}
### [Inboxes]{#symbol-ChatManager.Inboxes}

-   **control** : NOT USED
-   **errors** : error messages
-   **inbox** : incoming FLAPs on channel 2
-   **talk** : outgoing messages
:::

::: {.section}
### [Outboxes]{#symbol-ChatManager.Outboxes}

-   **outbox** : outgoing FLAPs
-   **signal** : NOT USED
-   **heard** : echoes peer messages to this box.
:::

::: {.section}
### Methods defined here

::: {.container}
::: {.boxright}
**Warning!**

You should be using the inbox/outbox interface, not these methods
(except construction). This documentation is designed as a roadmap as to
their functionalilty for maintainers and new component developers.
:::
:::

::: {.section}
#### [\_\_init\_\_(self)]{#symbol-ChatManager.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [cleanMessage(self, message)]{#symbol-ChatManager.cleanMessage}

strips HTML tags off messages
:::

::: {.section}
#### [main(self)]{#symbol-ChatManager.main}

Main loop.
:::

::: {.section}
#### [receiveMessage(self, body)]{#symbol-ChatManager.receiveMessage}

Extracts the sender and message text from SNAC body, and sends the tuple
(\"message\", sender, message) to \"heard\".
:::

::: {.section}
#### [sendMessage(self, buddyname, text)]{#symbol-ChatManager.sendMessage}

constructs SNAC (04, 06), the \"send message\" SNAC and sends it to
\"outbox\"
:::
:::

::: {.section}
:::
:::
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
