---
pagename: Projects/Soc2006/VisualEditor
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
SoC Project: Visual Editor
==========================

There was one project application in this area that is summarised here.
This page contains the depersonalised content, which can be consolidated
as necessary. The depersonalisation is for privacy reasons, credit is
here due to those who spent the time writing these descriptions.

### Project Title: Kamaelia Visual Editor, Graphical IDE 

Benefits to Kamaelia\
====================\
Extremely helpful to newcomers that wants to try Kamaelia out. Also good
for experienced users that quickly wants to patch something together,
maybe to see how their server responds to sent data before they\'ve
written the real client.\
\
Synopsis\
========\
When I found the Axon/Kamaelia Visualiser and read about that Kamaelia
had an early staged program in which you could \"write\" code visually,
I knew directly that this was something I wanted to work on. The ability
to be able to create, edit and run programs visually would be an immense
help to anyone new to Kamaelia.\
\
What I want to do could be compared to a visual IDE. I want to have that
same plain white field as in the Axon Visualiser. Then some kind of GUI
along the bottom or side in which you can select your \"pencil\". The
pencils can draw components (which can be given names), dataflow links
and passtrough links.\
\
In the GUI there will also be buttons to save and load the stuff you\'ve
done. There will also be a button for generating code out of your
visually built project.\
\
The Axon Visualiser will be integrated. So that you could press \"Run\"
and see your program spring to life through the Axon Visualiser.\
\
Deliverables\
============\
Will deliver:\
- A module with a GUI in which you can see and edit the Kamaelia program
visually.\
- A module for saving/loading the visual Kamaelia program.\
- A module that can generate useable code out of the visually built
Kamaelia program.\
\
Given Sufficient time:\
- Graphical components. In the visual editor, components will (if
applicable) be displayed with an image representing the component.\
- A module for turning already written Kamaelia code into a visually
built project.\
\
Project Details\
===============\
Everything will be written in Python so it can easily work with the rest
of Kamaelia. Pygame will be used to handle the input and graphics.\
\
Project Schedule\
================\
Early June: Design document written/set in stone what should be done.\
Late June: Everything related to graphics/input/GUI/pygame done and
added to project.\
Early July: Save/load visual projects module added.\
Late July: Code generation module added.\
Early August: Beta release/test phase begin.\
Late August: Project end/delivery.\
\
