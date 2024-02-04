---
pagename: Projects/Soc2006/AVCodecs
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
SoC Project: Increased Audio/Video Codec Support 
================================================

There were 3 project applications in this area that are summarised here.
This page contains the depersonalised content, which can be consolidated
as necessary. The depersonalisation is for privacy reasons, credit is
here due to those who spent the time writing these descriptions.\

### Project Title: Creation of Ogg Vorbis Encoder and mp3 Encoder/Decoder component bindings for Kamaelia.

Benefits to Kamaelia:\
\
There are existing components for decoding Ogg Vorbis and Dirac
multimedia formats in Kamaelia. But there are no existing Ogg Vorbis
Encoding components and no mp3 Encoding/Decoding components. Ogg Vorbis
& mp3 support will provide the Kamaelia toolkit a lot of versatility.
Kamaelia is already an excellent Free Software project and these two AV
component bindings will make it extremely useful in a wide range of
situations.\
\
Synopsis:\
\
mp3 is the current de-facto standard any type of audio transmission. Ogg
Vorbis is also a Free and Open Source audio format which is slowly
becoming very popular. Kamaelia though being an excellent toolkit
unfortunately lacks the above two. I will write component bindings for
mp3 encoding/decoding and also the encoding part of Ogg Vorbis as the
decoding part is already present in Kamaelia.\
\
This will enable Kamaelia to create and handle mp3, Ogg Vorbis streams.
The components will be created in Python by wrapping already existing C
library functions provided by libvorbis and ffmpeg (libavcodec). I will
also take a look at wrapping the video codecs in libavcodec and
components for putting in and extracting video from a container format
if time permits so.\
\
Deliverables:\
\
The Project deliverables are \--\

-   The Ogg Vorbis encoder component
-   The mp3 encoder & decoder components
-   Test cases for the above
-   Documentation and recipies for the CookBook\

And given sufficient time \--\

-   Components for handling a video codec
-   Components for putting encoding audio and video into a container
    format (eg AVI), and components for extracting audio and video from
    that container format.

\
Project Details:\
\
The project will mainly wrap available AV codecs with Python and create
lightweight components which will be used from within Kamaelia. The best
tool for this job is
[Pyrex](http://www.cosc.canterbury.ac.nz/%7Egreg/python/Pyrex/). Pyrex
is a programming language which is used for creating C modules for
Python. With Pyrex, there is no need to write glue-code. I can import &
directly use the C library as if they were Python data-types &
functions. Pyrex code can be then compiled to create a Python module
which can then be imported and used from within Python programs.\
\
I will thus use Pyrex and wrap the functions and datatypes provided by
libvorbis and libavcodec. Then that Pyrex code will be compiled to
generate lightweight Python modules which can be used directly from
within Kamaelia.\
\
The project will be useful in showcasing how to write Python bindings
for different libraries like libavcodec. In fact, the Python modules can
be used for any Python project, for example say, a multimedia
application written in Python. Thus its usage won\'t be restricted to
only this project and will be useful for all.\
\
I already have a fair amount of Python programming experience having
written quite a few apps for my college projects. I don\'t have much
idea about Pyrex as such, but I have some experience with extending
Python by writing modules in C and also some SWIG. I will read the
[Pyrex documentation](http://ldots.org/pyrex-guide/) and I don\'t think
it will take much time for me to understand Pyrex. I also need to take a
look at [libavcodec\'s API
docs](http://www.inb.uni-luebeck.de/%7Eboehme/using_libavcodec.html) to
understand its innards better.\
\
Project Schedule:\
\
I will start with wrapping libavcodec first and then will look at
libvorbis. Together, they would take around 2 weeks to be completed with
documentation. Writing test cases and recipies will take one more week
to be completed. So in total it will take around 3 weeks to be finished.
Ironically, despite the estimates, software projects usually take Pi
times more than the estimated time \-\-- Murphy is particularly
interested in software projects it seems ;) So I will presume that it
will take at least 9-10 months for me to fully develop and test the
project. If by any chance I finish early, I will start working on video
codecs in libavcodec and also take a look at handling container formats
for video.\
\
The development will be done completely in the open and the code will be
hosted on sourceforge.net or somewhere else if available. I intend to do
one Alpha and two Beta releases before doing the stable release to
ensure better testing of the code.\
\
An estimated project timeline is as below \--\
\
May 23, 2006 \-- Start of project\
June 19, 2006 \-- First Alpha Release\
Interim period \-- Continuous testing and feedback from the community\
July 19, 2006 \-- First Beta Release\
Interim period \-- Continuous testing and feedback from the community\
August 01, 2006 \-- Second Beta Release, Documentation released\
Interim period \-- Continuous testing and feedback from the community\
August 19, 2006 \-- Stable release of code\
August 21, 2006 \-- Code submission to Google\
\

------------------------------------------------------------------------

\
\

### Additional AV codecs in Kamaelia

Additional AV codecs in Kamaelia\
\
This is a proposal to create Kamaelia components to manipulate audio and
video data. This would include support for the MP3 codec, MPEG-2 video,
and Speex.\
\
This will allow more flexibility for Kamaelia as a multimedia platform.
This will help Kamaelia\'s goal as an agent of the BBC to efficiently
deal with its massive distribution requirements.\
\
I would deliver components for encoding and decoding MP3, MPEG-2 video,
and Speex data. The components would be thoroughly tested and documented
with pydoc so that they will integrate easily into the component
reference.\
\
I plan to implement support for these data formats by wrapping existing
C libraries with Pyrex to create bindings into Python and then creating
components from that. I plan to use libmad to deal with MP3, which would
also support audio layers I and II, and MPEG-2 audio. I would use
libmpeg2 to handle MPEG-2 video,and this would incidentally also wrap
support for MPEG-1.\
\
One of the most interesting codecs that I would provide components to
deal with is Speex . Speex is a patent-unencumbered codec designed for
voice communications. With Kamaelia\'s goal of strong multimedia support
and the ease of creating server components for it, a codec designed
especially for voice is a good idea. It would be simple to make a voice
communication system built on top of Speex that would work more
efficiently than one that made use of Vorbis.\
\
If I had time, I would create components to support the FLAC lossless
audio codec. It would be nice to have support for an audio codec that is
not lossy but does employ some sort of compression.\
\
By the halfway point I expect to have fully componentized MP3 using
libmad, along with documentation and testing. After that, I think the
process will pick up speed. By the end of the Summer of Code, I plan to
have wrapped libmad, libmpeg2, and libspeex; I would of course provide
components and documentation for these. If I had time at the end, I
would work on wrapping and creating components for libflac .\

------------------------------------------------------------------------

\

### A set of components for flexible media playback. 

Benefits to Kamaelia: Since Kamaelia is a toy box, there has to be good
toys. Seeing how most media available today is either mp3, mpeg or avi
Kamaelia should also support playing with these formats (Are you
discriminating!?!). This will make Kamaelia more flexible, and more
people will find it interesting to use.\
\
Synopsis: 2 paras (maybe 3)\
A set of components that allow users to use mp3, mpeg and avi files in
their programs. The components will be based around the same class, and
should therefore be very easy change (even at runtime!!).\
\
Deliverables:\
A set of components made in Python with Pymedia that decode and encode
video and audio. There will be components for at least mp3, mpeg and
basic avi formats. The components should inherit from a basic encode and
decoder class, and be easy to interchange as one sees fit. The
components will be based on unit tests, and will have documentation
according to the standard for Kamaelia components (docstrings it seems
like). Also an example application that utilizes the components will be
delivered.\
\
If this goes as smooth as I want to I will expand the component set to
include the most used formats (xvid, divx\'s, vob?), also a real-time
filter component could be nice, but I am not sure it is doable.\
\
A neat extra would be to implement a component that handles the format
that is used for mobile streaming (or is it just mpeg/avi?). This way it
would be easy to make programs that streams stuff to the mobile phone.
Maybe a stream of the whiteboard component, so that people can follow
the whiteboard while on the buss.\
\
Project Details:\
The project will base itself on Python and Pymedia. I believe this will
suffice to make components for most formats that should be desired, but
I may be wrong since I don\'t know much about Kamaelia yet. The Pymedia
module offers a nice and easy way to get raw output from most formats
(I\'ve only tried with mpeg), and the different components should
therefore be quite simple to make.\
\
I would have to start by getting to know Kamaelia, then figure out a
good way to implement the components to fit Kamaelia. Once this is done,
unit tests should be developed. A decent class/component that the
different formats could inherit should come next, with the format
specific components following. Docstring documentation will be written
at the same time.\
\
The real-time filter could be done with a Numpy/Numeric array and the
raw frame data, but I am not sure (got my doubts) that it will be fast
enough. Alternatives could be to do it on the compressed data (?) or
make it, non real-time.. but this takes a bit of the fun out of it.\
\
Project Schedule:\
\
I will use a week or two to get to know Kamaelia and how it is
structured.\
Then I will make a class for a generic encoder / decoder and unit tests
for those. This should take no more than a week.\
The different formats should be quite simple to implement if pymedia is
as easy to use for other formats than mpeg. I would think a maximum of
two weeks to implement and document the components.\
After this a example of how the components should be made. Depending on
how intuitive the Kamaelia framework is to use, this should take a
couple of days, maybe a week depending on the complexity of the
example.\
This should leave two to four weeks to work on more format components
and a real-time filter component.\

------------------------------------------------------------------------

\
\
