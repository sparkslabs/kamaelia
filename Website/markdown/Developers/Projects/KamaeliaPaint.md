---
pagename: Developers/Projects/KamaeliaPaint
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia: Paint
===============

What is it?
-----------

Kamaelia: Paint is still very much in development (so this is my
\"vision\" of what I want \'Paint\' to become). Paint will be a powerful
image editing tool, it will have native support of multiple core
processors and put them all to good use :-). It should handle large
volumes of images and have some simple tools for animations.\

Where do I get it & install it?
-------------------------------

**developers**\

-   svn co\
-   cd
-   python setup.py install

**Linux**\
*Something like:\
*

-   *download .tar.gz\
    *
-   *sudo python setup.py install*\
-   *run*\

\
**Windows**\
*Something like:\
*

-   *download .exe*
-   *Install*
-   *Enjoy*\

\
**Mac**\
*Something like:\
*

-   *download .dmg*
-   *Install*
-   *Enjoy*\

Planned Schedule:
-----------------

-   26/5 - Extend MagnaDoodle (Simple paint tool located in Sketches/DK)
    to implement the features of ProcessGraphline, with the end goal
    being having it running on a Backplane.
-   2/6 - Finish up working on MagnaDoodle / Start planning how the
    paint tool will be packaged. - Working on MagnaDoodle may take
    longer than expected however much of it will cross over to my Paint
    program so time spent here is also contributing to my main project.
-   9/6 - Consider what can be moved from the MagnaDoodle to Paint.
    Begin working on Paint, implementing mutual features from
    MagnaDoodle and extending them.
-   16/6 - Work on the painting canvas, look for the potential ways to
    implement a \"layering\" feature. nb. Something like what happens
    when you run MagnaDoodle with the Graphline.
-   23/6 - Finish up the canvas and start work a separate window for
    tools, such as Circles, lines various vector shapes. - note: this
    might take longer than 1 week
-   30/6 - Finish up the painting tools, and any additional work on the
    Canvas. I expect a colour selector to have been made in MagnaDoodle,
    however, it might be an idea to extend this and add more
    functionality to it.
-   7/7 - Hopefully now I have a fairly robust Paint program at this
    point. Now start to look at ways to extend this to various Animation
    methods.
-   14/7 - Work on Animator, try to reach a stage where I can have a
    \"flick book\" style animation see:
    http://en.wikipedia.org/wiki/Flip\_book This style thing should be
    pretty easy.
-   21/7 - Look at more animation tools, perhaps modifying many frames
    of the animation at once.
-   28/7 - Consider encoding animations using something like dirac.
-   4/8 - Perhaps at this point look at implementing \"given time\"
    features such as simple video editing. Decoding dirac video\'s to a
    bunch of images for animation editing.
-   11/8 - Continue work on video editing features. Try to implement
    \"Resume Session\" feature.
-   18/8 - Wrap up the project and work on packaging it up.

Progress (dates related to the weekly meeting - these are the \"DONE\" lines)
-----------------------------------------------------------------------------

-   15 May: Looked through code for MultiPipeline / Magnadoodle
-   22 May: Got 2 MagnaDoodle.py working together using
    ProcessPipeline(), also implemented simple scaling circle tool.
-   29 May: Got ProcessGraphline to clear one window when right click in
    the other (really cool :D) - this can be easily extended but
    encountered some problems with ProcessGraphline
-   5 June: I got the 2 MagnaDoodles talking, you can draw on the blue
    and it paints also on the Red. Abstracted away pygame events from
    the drawing for more flexibility.
-   12 June: ﻿Merged IRC Logger, got Tools2Apps ready for merge just got
    to resolve merging error. Moved to Paint from MagnaDoodle, started
    working on main project! Just started using an XYPad for paint
    selection
-   19 June: ﻿Recursive flood-fill algorithm for a \"paint bucket fill\"
    tool. Turned an XYPad into a nice colour selector and hooked that up
    to Kamaelia - Paint. Cleaned up code.
-   26 June: Non-recursive flood-fill working nicely lots better than
    last week, cleaned up code and added buttons for controling the
    tools. Started work on methods for layering
-   3 July: Layers (using pygame surfaces) are now working, little
    functionality currently but core is there. Added an Eraser tool and
    Eyedropper tool. PASSED MY EXAMS!
-   10 July: Functionality of layers, adding layers, switching between
    layers and changing the Alpha values (via slider bar) for each
    layer. Made a start using layers as a basis for Animations

Progress so far 
---------------

Screenshots of my progress can be found
[here!](../../../Developers/Projects/KamaeliaPaint/ProgressScreens)\
\
July 28th: I have restructured my code so it\'s worth making clear what
I\'ve changed. Previously I was working with a highly modified version
of the XYPad for sliders and the colour selector. However that wasn\'t
really the Kamaelia way to approach the problem, I had left it that way
for too long and the longer I worked on the XYPad the more convoluted it
became. IMO the Kamaelia way was to break that down into smaller
components, this way the code would be reusable for anyone else. So
I\'ve broke the XYPad into the Slider, ColourSelector and ToolBox
component. The colour selector and slider are both now just some pygame
widgets and the ToolBox is the Paint specific code. Recently I\'ve also
worked on input and output of images, one bug I want to note (for my own
benefit) is that when you save it will merge all layers to the
background. Still looking to solve it but have wasted enough time on it
for now :-).\
\

Wishlist
--------

Everyone has their favourite tools in paint programs like The Gimp and
Photoshop, so if there\'s something you\'d like to see in Kamaelia:
Paint feel free to edit this list and add whatever you want. No
promises! Oh, and don\'t add \"Lens Flare\" :P I\'ll go through this
list and add priorities (5-1 low to high respectively) Thanks! Dave.\

-   Image Layers \[1\]
-   Crop tool \[2\]
-   Rotate tool \[3\]
-   Storyboarding features (strikes me as a really cool idea) \[2\]
-   Multi-frame animation editing \[3\]
-   Various Brushes \[2\]
-   Looking at the what Michael has made with the SpeakNWrite app maybe
    I could implement that with the storyboarding? Reading the dialogue
    from a storyboard? Handling separate speech bubbles using something
    similar to the flood fill algorithm\
