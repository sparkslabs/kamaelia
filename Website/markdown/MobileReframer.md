---
pagename: MobileReframer
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
MobileReframer
==============

::: {.boxright}
For development/status information, see the [project task
page](/Developers/Projects/MobileReframer%20)
:::

\
[This is a command line tool that decodes a video clip; applies edit
decisisions (cutting, cropping and scaling); and
re]{style="background-color: rgb(255, 255, 255);"}-encodes it. The idea
is to cut and crop video to make it suitable for playback on a small
screen mobile device by zooming in onto just the important bit - such as
the face of the interviewee.\
\
You supply a set of edit decisions in an XML file, and the
MobileReframer will apply those to the source video file you provide,
creating a new output video file with the resolution you specify\
\

Getting Started
---------------

You can find the Mobile Reframer itself in ` /Sketches/MH/MobileReframe`
in the trunk of the subversion repository.\

### Pre-requisites

1.  You must install Axon from the ` private_MH_outboxwakeups ` branch
    in the subversion repository. Mobile Reframer requires the new
    features in this branch to enable it to self rate limit without
    exploding memory usage!\
    \
    Install it the usual way using the command line:\
    ` python setup.py install`\
    \
2.  You must have an installed copy of the command line ffmpeg tool,
    which can be obtained from [here.](http://ffmpeg.mplayerhq.hu/) Make
    sure you have all the codecs you need of course!\

### Running MobileReframer.py 

Run MobileReframer.py from the command line and you\'ll get usage
information:\

``` {style="margin-left: 40px;"}
> ./MobileReframer.py

Usage:
    MobileReframer.py <infile> <edlfile> <outfile> width height <tmpdir>

* width and height are even numbered pixel dimensions for output video
```

So, for example, if you run it with the following command line:\
\

``` {style="margin-left: 40px;"}
./MobileReframer.py myVideo.avi myEditDecisions.xml theResult.avi 240 160 /tmp/mobile_reframer_scratch
```

This will apply the edit decisions in the xml file to the input video
file and produce a result that is 240x160 pixels.\
\
Note that you need to specify a temporary working directory for mobile
reframer to use, since it needs somewhere to decompress video frames
into. This temporary directory should not be being used by any other
programs, including other instances of MobileReframer, and there should
be enough free disk space to hold, in the worst case, the whole input
video file when decompressed to raw frames and audio.\
\

Writing the edit decision XML file
----------------------------------

\
Write your edit decisions in an XML file, like this:\

>     <?xml version="1.0" encoding="ISO-8859-1"?>
>     <EDL xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="MobileReframe.xsd">
>
>         <FileID>File identifier</FileID>
>
>         <Edit>
>             <Start frame="0"  />
>             <End   frame="24" />
>             <Crop  x1="0" y1="0" x2="400" y2="100" />
>         </Edit>
>         <Edit>
>              frame="25" />
>                frame="49" />
>               x1="80" y1="40" x2="480" y2="140" />
>         </Edit>
>
>     </EDL>
>       

[The above edit decision list, or a similar one, shoudl be in the file
` TestEDL.xml ` in the MobileReframer\'s directory.\
\
]{style="font-family: verdana,arial,helvetica,sans-serif;"}The format is
pretty simple: simply specify a set of \'edits\', in the order you want
them to appear in the resulting video.\
\
Each edit is a chunk of the input video specified by a start and end
frame number, and then the bit of the video you want it cropped down to.
Frames are numbered from zero, and coordinates are specified in pixels
where (0,0) is the top left corner.\
\
For example perhaps, for frames 25 to 49 inclusive (a 2 second chunk
that starts 4 seconds into the video, assuming 25fps video) we want the
video to be cropped to a region in the lower left of the image:\
\
\

  ----------------------- ----------------------- -----------------------
  (0,0)\                      Throw this bit away \

  \                                     (100,150) \

  \                              Crop to this bit \

  \                                     (400,250) \

  \                                             \ (719,575)
  ----------------------- ----------------------- -----------------------

\
Then to achieve this we would write, as part of our edit decisions:\

        <Edit>
            <Start frame="25" />
            <End   frame="49" />
            <Crop  x1="100" y1="150" x2="400" y2="250" />
        </Edit>

You can write your edit decisions in any order - you don\'t have to
preserve the chronological order of the original video. For example,
perhaps the video you are editing has 10 seconds of titles 30 seconds in
from the start. Your edit decisions could specify that the output video
should start with a few seconds of those titles, then return to
something closer to the beginning.

You don\'t have to use the whole video - you can use your edit decisions
to cut a video down into a shorter one.

\
****\
****
