---
pagename: Components/pydoc.old/Kamaelia.vorbisDecodeComponent.AOAudioPlaybackAdaptor
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.vorbisDecodeComponent.AOAudioPlaybackAdaptor
=====================================================

class AOAudioPlaybackAdaptor(Axon.Component.component)
------------------------------------------------------

AOAudioPlaybackAdaptor() -\> new AOAudioPlaybackAdaptor

Expects to recieve data from standard inbox, and plays it using libao.
When it recieves a message on the control port: Sends a producerConsumed
to its outbox. Then shutsdown.

**Requires** libao and pyao (python bindings)

**Example**

A simple player:

``` {.literal-block}
pipeline(
    ReadFileAdaptor("somefile.ogg"),
    VorbisDecode(),
    AOAudioPlaybackAdaptor(),
).run()
```

#### Inboxes

-   control : If a message is received here, the component shutsdown
-   inbox : Any raw PCM encoded data recieved here is played through the
    default oss playback device

#### Outboxes

-   outbox : UNUSED
-   signal : When the component shutsdown, it sends a producerFinished
    message out this outbox

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### main(self)

Performs the logic described above

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
