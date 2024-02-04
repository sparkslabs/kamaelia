---
pagename: KamaeliaMacro
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
**Jan 2024 - This site, and Kamaelia are [being
updated](https://github.com/sparkslabs/kamaelia/issues/7). There is
significant work needed, and
[PRs](https://github.com/sparkslabs/kamaelia/pulls) are welcome.**

Kamaelia Macro
==============

[Tools for timeshifting]{style="text-align: right; display: block; font-size: 18pt;"}

<iframe src="https://www.slideshare.net/slideshow/embed_code/key/701GJnadkg2bjN?startSlide=1" width="597" height="486" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="margin: auto; display: block; border:1px solid #CCC; border-width:1px; margin-bottom:5px;max-width: 100%;" allowfullscreen></iframe><div style="margin-bottom:5px"><strong><a href="https://www.slideshare.net/kamaelian/timeshift-everything-miss-nothing-mashup-your-pvr-with-kamaelia" title="Timeshift Everything, Miss Nothing - Mashup your PVR with Kamaelia" target="_blank">Timeshift Everything, Miss Nothing - Mashup your PVR with Kamaelia</a></strong> from <strong><a href="https://www.slideshare.net/kamaelian" target="_blank">kamaelian</a></strong></div>

For more context on timeshifting in Kamaelia, [please see this page](http://kamaelia.sourceforge.net/ToolsForTimeshifting.html).

What is it?
-----------

It records and transcodes what is broadcast over DTT for future viewing.
It is essentially a form of timeshifting. It is currently at a prototype
stage, and as such the contents of this page is subject to change.
Programs are captured, transcoded and then made avallable for viewing in
a variety of formats. The two primary formats are suitable for handheld
TV\'s and *relatively* small living room TVs.

The resulting data was forwarded to a simple front end for demonstration
purposes.

High Level Architecture
-----------------------

The high level architecture is as follows:

![](/images/macro_1.1.png)

This might seem too high level. However, due to Kamaelia\'s nature, this
has a direct mapping to the underlying code.

Channel Transcoding
-------------------

A channel transcoder takes the data it recieves and splits it into two.

-   Scheduling information - EIT data - is extracted, and sent to an EIT
    Handler. This looks for events - specifically programme changes.
    When there\'s a programme change it spits out the information
    regarding the programme. This \"programme change\" event is also
    used to break up the transcoding, as we shall see shortly. The EIT
    information is also stored as a MIME like object with a name that
    increments.
-   The audio/video data relating to the channel. To handle this a Unix
    Shell out component - a **Pipethrough** component is created. This
    performs the actual transcoding to a given filename. The filename
    increments and matches the EIT data. The transcoding is specifically
    done by performing a shell out to `mencoder`.

Diagrammatically, this looks like this: (only one actual transcoder
shown for simplicity)

![](/images/macro_1.2.png)

The interesting point is what happens when there\'s a programme event
change. In this circumstance, new transcoders are created, and the audio
visual data is sent to them. The original transcoders are sent shutdown
messages telling them to shutdown after completing their transcoding.
This then triggers the copying of the transcoded data & captured
metadata to a location where the (currently simple) frontend can access
it

Diagrammatically, the replumbing looks like this:

![](/images/macro_1.3.png)

Specifically, files are created of the form:

-   channelname.programmeid.bitrate.avi \# 200 Kbit/s
-   channelname.programmeid.bitrate.avi \# 512 Kbit/s
-   channelname.programmeid.bitrate.DONE \# 200 Kbit/s
-   channelname.programmeid.bitrate.DONE \# 512 Kbit/s
-   channelname.programmeid.META

### Primitive Front End

The existing front end is a simple prototype that shows how a standard
single channel can be made to look like a RSS feed like any other
\"web\" channel. This is - probably unsurprisingly - no longer visible
for lots of reasons!

A snapshot of the current view:

![](/screenshots/KamaeliaMacro.png){style=width:100%}

Future?
-------

The code & system described here is not the final version. The upcoming
release of Kamaelia & Axon (0.4.0 and 1.5.0 respectively) will include
the simple version of Macro as an example, in examples 15 specifically.
Until then in order to use this you\'ll want to grab a bundle, follow
the instructions for getting started, and then get a recent CVS
snapshot. Please contact us for help in getting started. Once again
though, bear in mind that these tools have been created for legal
timeshifting purposes only.

If you\'re interested in collaborating on building this and taking this
technology forward (or perhaps even building into a domestic PVR, or a
personal/homebrew PVR) we\'d be very interested in hearing from you!

End Notes
---------

Kamaelia tools for timeshifting are relatively nascent, but as can be
seen can be used for a variety of interesting uses already. As it should
be clear, extending these systems to do more would be relatively simple.
For example rebroadcasting the transcoded data using multicast is a
relatively simple extension.

Regarding Kamaelia, this work has been useful so far for driving a large
amount of optimisation work for the core system - Axon. This has had a
number of knockon effects, such as making collaborative whiteboarding a
realistically useful tool.

------------------------------------------------------------------------

Michael, May 2006
