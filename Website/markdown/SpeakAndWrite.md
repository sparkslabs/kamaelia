---
pagename: SpeakAndWrite
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Hack for Mashed: Speak And Write
================================

::: {.boxright}
**NOTE:** This doesn\'t replace actually teaching - but it makes a
lovely toy, in the style of a speak and spell from years ago\...
:::

This hack is a \"toy\" for a small child to assist them to learn to read
and write. They are asked to write specific words - both textually and
also using speech synthesis. What they write is then read out to them.
This version is by no means \"complete\", but it works.\

The vocabulary it teaches (currently) is from sheet one of the DFES
[Reception Term, Reception Year word
cards](http://www.standards.dfes.gov.uk/primary/publications/literacy/nls_framework/485701/)
for literacy in reading/writing.\

![](../../../images/SpeakNLearn-1.png){width="623" height="400"}

Where to Get it: 
----------------

First initial version here: (name reflects what I was calling it then)\

-   [http://www.kamaelia.org/release/Kamaelia Speak N
    Learn-0.1.0.tar.gz](../../../release/Kamaelia%20Speak%20N%20Learn-0.1.0.tar.gz)

Installing:
-----------

> \~/incoming/\> tar zxvf Kamaelia\\ Speak\\ N\\ Learn-0.1.0.tar.gz\
> \~/incoming/\> cd Kamaelia\\ Speak\\ N\\ Learn-0.1.0/Kamaelia/\
> \~/Kamaelia/\> python setup.py install\

Where\'s the Source? 
--------------------

-   <https://kamaelia.svn.sourceforge.net/svnroot/kamaelia/branches/private_MPS_SpeakNLearn/Apps/SpeakNLearn/App/SpeakNWrite.py>

Running:
--------

> \~\> SpeakNLearn.py\

Dependencies:
-------------

-   You need to have espeak installed
-   You need to have aplay installed
-   You need to have pygame installed\

Internals
---------

This will shift off to the developers area since you don\'t need to know
this to use it, but provided for those who may find it interesting:\

::: {align="center"}
![](../../../images/SpeakNWriteCodeArchitecture.png)\

::: {align="left"}
To read this, start at the top - with Challenger. That sends a challenge
out, which is sent to both the display and to a backplane called
\"speech\". The speech backplane simply speaks anything that gets to it.
The child hears this and scribbles on the canvas. (The canvas sends
messages about scribbles to the pen which decides what to do - draw,
etc. The pen sends messages to the strokes (handwriting) recogniser.
They both need to be able to draw lines on the canvas, and/or clear it.\
\
The stroke recogniser sends messages to the aggregator which turns the
recognised strokes into commands the textbox understands. This includes
detecting a stroke from top right to bottom left to mean \"press
return\". The output from the text box is then forwarded to the display
and also to something that\'s checking what the challenger asked for. It
then sends a message to the \"speech\" backplane to say something to the
user, and also, if appropriate to the challenger. The challenger then
either repeats or says a new word. This diagram has a 1:1 correspondance
with the code.\
:::
:::

\

### What\'s inside the Stroke Recogniser?

For tomorrow :-)\
\

Follow on Ideas
---------------

Instant Messenger for Children. They write, it speaks.\
\
Michael, June 2008
