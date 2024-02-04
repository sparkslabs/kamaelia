---
pagename: VideoCutDetector
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Video Cut Detector
==================

::: {.boxright}
For development/status information, see the [project task page](/Developers/Projects/VideoCutDetector.html)
:::

This is a simple command line tool to analyse a video file and output a
list of (probable) locations of cuts (shot-changes) in the video.\
\
This can serve as useful input data to user controlled video
manipulation/editing applications where it is useful to be able to
precisely identify where shot changes take place.

Getting Started
---------------

You can find the cut detector itself in
` /Sketches/MH/Video/CutDetector` in the trunk of the subversion
repository.\

### Pre-requisites

1.  You must install Axon from the ` private_MH_outboxwakeups ` branch
    in the subversion repository. The cut detector requires the new
    features in this branch to enable it to self rate limit without
    exploding memory usage!\
    \
    Install it the usual way using the command line:\
    ` python setup.py install`\
    \
2.  You must have an installed copy of the command line ffmpeg tool,
    which can be obtained from [here.](http://ffmpeg.mplayerhq.hu/) Make
    sure you have all the codecs you need of course!\
    \
3.  You must run ` make` in the Cut Detector\'s directory to build the c
    support library used to perform the image processing needed. This
    requires pyrex ( [get it here](http://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/) ).\

### Running CutDetector.py

Run ShotChangeDetector.py from the command line and you\'ll get usage
information:\

>     > ./ShotChangeDetector.py
>
>     Usage:
>
>         ./ShotChangeDetector.py [--show] [threshold] videofile
>
>     * threshold is a floating point value greater than zero (default=0.9)

So for example, if you run it with the following command line:

``` {style="margin-left: 40px;"}
> ./ShotChangeDetector.py myvideofile.avi
```

Then as the cut detector runs, XML listing the frame numbers of where
probably cuts (shot changes) have been detected will be sent to standard
output, for example:\

>     <?xml version="1.0" encoding="ISO-8859-1"?>
>
>     <detected_cuts xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
>                       xsi:noNamespaceSchemaLocation="DetectedCuts.xsd">
>         <cut frame="39" confidence="0.9469" />
>         <cut frame="49" confidence="0.9820" />
>         <cut frame="76" confidence="0.9009" />
>         <cut frame="78" confidence="1.0142" />
>         <cut frame="103" confidence="1.0033" />
>         <cut frame="110" confidence="0.9777" />
>         <cut frame="135" confidence="0.9613" />
>         <cut frame="147" confidence="0.9953" />
>
> > > *\.... cut down for succinctness! \...*
>
>         <cut frame="45167" confidence="0.9209" />
>         <cut frame="45168" confidence="0.9209" />
>         <cut frame="45169" confidence="0.9209" />
>         <cut frame="45170" confidence="0.9210" />
>         <cut frame="45171" confidence="1.0389" />
>     </detected_cuts>

The cuts are listed by frame number, starting from zero for the first
frame.\

The \'confidence\' value is the confidence the algorithm has that what
was detected actually is a shot change. It is basically a measure of how
much the picture suddenly changed. The higher the value, the more likely
it is to be a cut.\

Options
=======

Sensitivity Threshold
---------------------

You can specify the threshold value used for shot change detection. The
default is 0.9, meaning that any possible cuts with a confidence value
of less than 0.9 are not output. Sensible values are probably about 0.75
or greater. The cut detector will not accept values less than or equal
to zero.\
\
Specify the threshold as a floating point value immediately before the
video filename, for example:\

``` {style="margin-left: 40px;"}
> ./ShotChangeDetector.py 0.85 myvideofile.avi
```

The best choice of threshold value will vary depending of the type of
video content. The best way to choose is to experiment. Using 0.9 as the
starting point for this is probably a good idea.\

Displaying the video
--------------------

You can optionally ask to be shown the video live (without sound
unfortunately!) as the cut detection takes place. Use the ` --show `
command line option to do this. For example:\

``` {style="margin-left: 40px;"}
> ./ShotChangeDetector.py --show myvideofile.avi
```

The video will be rate limited to 25fps, irrespective of the actual
frame rate of the video. Detected cuts will be sent to standard output
as usual.\
\
Bear in mind that becuase the detection algorithm needs to compare
multiple frames, the detected cuts will be output several frames after
they were detected - do not expect them to be displayed the moment the
shot change happens in the displayed video!\
\
\

\-- Matt, April 2007

\
