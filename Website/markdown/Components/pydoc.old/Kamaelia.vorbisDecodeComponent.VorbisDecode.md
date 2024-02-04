---
pagename: Components/pydoc.old/Kamaelia.vorbisDecodeComponent.VorbisDecode
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.vorbisDecodeComponent.VorbisDecode
===========================================

class VorbisDecode(Axon.Component.component)
--------------------------------------------

VorbisDecode() -\> new VorbisDecoder

A Vorbis decoder accepts data on its inbox \"inbox\", as would be read
from an ogg vorbis file, decodes it and sends on the decompressed data
on out of its outbox \"outbox\". It doesn\'t provide any further
information at this stage, such as bitrate, or any other frills.

**Requires** libvorbissimple and python bindings (see kamaelia
downloads)

**Example**

A simple player:

``` {.literal-block}
pipeline(
    ReadFileAdaptor("somefile.ogg"),
    VorbisDecode(),
    AOAudioPlaybackAdaptor(),
).run()
```

This component expects to recieve OGG VORBIS data as you would get from
a .ogg file containing vorbis data. (rather than raw vorbis data)

#### Inboxes

-   control : Receiving a message here causes component shutdown
-   inbox : Ogg wrapped vorbis data

#### Outboxes

-   outbox : As data is decompresessed it is sent to this outbox
-   signal : When the component shuts down, it sends on a
    producerFinished message

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### main(self)

This contains no user serviceable parts :-)

Theory of operation is simple. It simply repeatedly asks the decoder
object for audio. That decoded audio is sent to the component\'s outbox.
If the decoder object responds with RETRY, the component retries. If the
decoder object responds with NEEDDATA, the component waits for data on
any inbox until some is available (from an inbox)

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
