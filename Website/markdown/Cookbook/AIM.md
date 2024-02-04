---
pagename: Cookbook/AIM
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Cookbook: AIMHarness
====================

Sending and receiving messages over AIM is easy. AIMHarness only deals
with four kinds of messages: outgoing IMs, incoming IMs, buddy online
notifications, and error notifications. The first kind it receives in
its inbox, and the other three are sent out through its outbox.\
\

-   To send an instant message to another user, send the command
    (\"message\", recipient, text of the message) to its \"inbox\".
-   AIMHarness will send out the following notifications through its
    \"outbox\":

```{=html}
<!-- -->
```
          NOTIFICATION                                         EVENT
                    ("buddy online", {buddy information})                A buddy comes online
                    ("message", sender, message text)                    An instant message arrives for you
                    ("error", error message)                             An error occurs during the first stage of login

\
\

A simple, one-buddy AIM client using Pygame
-------------------------------------------

>     def sendTo(recipient, text):
>         return ("message", recipient, text)
>
>     def outformat(data, buddyname):
>         if data[0] == "buddy online" and data[1]["name"] ==  buddyname:
>             return "%s is online" % buddyname
>         elif data[0] == "message" and data[1] == buddyname:
>             return "%s: %s" % (buddyname, data[2])
>         elif data[0] == "error":
>             ": ".join(data)
>
>     def SimpleAIMClient(screenname, password, buddyname):
>         Pipeline(Textbox(position=(0, 400)),
>                  PureTransformer(lambda text: sendTo(buddyname, text)),
>                  AIMHarness(screenname, password),
>                  PureTransformer(lambda tup: outformat(tup, buddyname)),
>                  TextDisplayer()
>                  ).run()
