---
pagename: Cookbook/PipelinesAndGraphlines
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Cookbook : Pipelines and Graphlines
===================================

::: {.boxright}
**Discussion** Please discuss this on [the discussion
page](http://backend.kamaelia.org/Cookbook/PipelinesAndGraphlinesDiscuss)
for this page
:::

Fairly early on you\'ll want a quick an easy way to link your components
together. To actually build a useful system you need to set up linkages
to get data from one component\'s outbox to another component\'s inbox.
[**Pipelines**](/Cookbook/Pipelines) and
[**Graphlines**](/Cookbook/Graphlines) are the two simplest and most
common ways of doing this.\
\

::: {.boxright}
Find out more about using Pipelines [here](/Cookbook/Pipelines)
:::

Pipeline and Graphline are, themselves, components. Pipeline wires
components together in a long chain. For example:\

>     from Kamaelia.Chassis.Pipeline import Pipeline
>
>     from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver
>     from Kamaelia.Protocol.SimpleReliableMulticast import SRM_Sender
>     from Kamaelia.Protocol.Packetise import MaxSizePacketiser
>
>     Pipeline( RateControlledFileReader("myaudio.mp3",readmode="bytes",rate=128000/8),
>               SRM_Sender(),
>               MaxSizePacketiser(),
>               Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600),
>             ).run()

::: {.boxright}
Find out more about Graphlines [here](/Cookbook/Graphlines)
:::

Whereas a Graphline wires components together in any way you want - you
specify each individual link. For example:\

``` {style="margin-left: 40px;"}
from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.UI.Pygame.Image import Image

from Kamaelia.Util.Chooser import Chooser

from Kamaelia.Chassis.Graphline import Graphline

files = [ "slide1.gif", "slide2.gif", .... "slide99.gif" ]

Graphline(
     CHOOSER  = Chooser(files),
     IMAGE    = Image(size=(800,600), position=(8,48)),
     NEXT     = Button(caption="Next",     msg="NEXT", position=(72,8)  ),
     PREVIOUS = Button(caption="Previous", msg="PREV" ,position=(8,8)   ),
     FIRST    = Button(caption="First",    msg="FIRST",position=(256,8) ),
     LAST     = Button(caption="Last",     msg="LAST" ,position=(320,8) ),
     linkages = {
        ("NEXT",     "outbox") : ("CHOOSER", "inbox"),
        ("PREVIOUS", "outbox") : ("CHOOSER", "inbox"),
        ("FIRST",    "outbox") : ("CHOOSER", "inbox"),
        ("LAST",     "outbox") : ("CHOOSER", "inbox"),

        ("CHOOSER",  "outbox") : ("IMAGE",   "inbox"),
     }
).run()
```

\-- 17 Dec 2006 - Matt Hammond\

\
