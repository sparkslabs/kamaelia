---
pagename: Docs/Multimedia
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Multimedia facilities
---------------------

### Audio and Video capabilities  {#audio-and-video-capabilities align="right"}

[Kamaelia.Audio](/Components/pydoc/Kamaelia.Audio) contains components
implementing audio input and output as well as support for some codecs
such as MP3. These are provided by using the cross-platform pymedia
library (make sure you have installed it!). Some bespoke components for
audio filtering and mixing are also held here.\

[Kamaelia.Codec](/Components/pydoc/Kamaelia.Codec) contains components
for encoding and decoding Dirac video, and Speex and Ogg Vorbis audio,
as well as support for parsing raw data into video frame data
structures. There is also a libAO based audio player, which obviously
requires libAO and the pyao python bindings.

**Formats used to pass audio and video between components**\

Audio components for the most part pass around raw audio data as raw pcm
data in python strings.

Uncompressed raw video is passed around as whole frames - using a
dictionary structure containing the raw data and useful metadata such as
the width, height, pixel format and frame rate.

**Where to look:**

See [Kamaelia.Audio](/Components/pydoc/Kamaelia.Audio) for:\

-   Audio Input / Capture (pymedia)
-   Audio Output / Playback (pymedia)
-   MP3 audio Encoding (pymedia)
-   MP3 audio Decoding (pymedia)
-   Audio resampling
-   Audio filtering
-   Audio mixing

\
See [Kamaelia.Codec](/Components/pydoc/Kamaelia.Codec) for:\

-   Ogg Speex audio encoding
-   Ogg Speex audio decoding
-   Ogg Vorbis audio decoding
-   Audio output / Playback (libAO)
-   Dirac video encoding
-   Dirac video decoding
-   Raw data framing for video

\-- Matt, April 2007\
\
