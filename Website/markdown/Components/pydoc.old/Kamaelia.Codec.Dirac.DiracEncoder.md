---
pagename: Components/pydoc.old/Kamaelia.Codec.Dirac.DiracEncoder
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Codec.Dirac.DiracEncoder
=================================

class DiracEncoder(Axon.Component.component)
--------------------------------------------

DiracEncoder(\[preset\]\[,verbose\]\[,encParams\]\[,seqParams\]) -\> new
Dirac encoder component

Creates a component to encode video using the Dirac codec. Configuration
based on optional preset, optionally overriden by individual encoder and
sequence parameters.

Keyword arguments: preset \-- \"CIF\" or \"SD576\" or \"HD720\" or
\"HD1080\" (presets for common video formats) verbose \-- NOT YET
IMPLEMENTED (IGNORED) encParams \-- dict of encoder setup parameters
seqParams \-- dict of video sequence info parameters

#### Inboxes

-   control : Secondary inbox often used for signals. The closest
    analogy is unix signals
-   inbox : Default inbox for bulk data. Used in a pipeline much like
    stdin

#### Outboxes

-   outbox : Default data out outbox, used in a pipeline much like
    stdout
-   signal : The default signal based outbox - kinda like stderr, but
    more for sending singal type signals

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, preset, verbose, encParams, seqParams)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### main(self)

Main loop

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
