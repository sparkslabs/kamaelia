---
pagename: Projects/Soc2006/OpenGLWidgets
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
SoC Project: Open GL Widgets
============================

There is 1 project application in this area that is summarised here.
There was also an active SoC Project in this area over the course of the
summer which was extremely prouctive. This page contains the
depersonalised content, which can be consolidated as necessary. The
depersonalisation is for privacy reasons, credit is here due to those
who spent the time writing these descriptions.\

### Project: OpenGL widget framework for Kamaelia

\
Benefits to Kamaelia:\
\
Kamaelia has already the pygame widget components, but it displays only
2D images,having OpenGL widget components will just add the capabilities
to display 3D primitives and it will be displaying 2D surfaces too. Just
this will open more the options of Kamaelia\
for topology and games.\
\
Synopsis:\
\
The project will consist in creating the components needed for a basic
OpenGL widget framework that could work with the PyGame components that
have been created for Kamaelia.\
One of the main goals is to create components that can setup a OpenGL
rendering context, in this case the rendering context will be the PyGame
display component.\
\
Project details:\
\
OpenGL is a well know API for developing 2D and 3D graphics
applications. For the project, PyOpenGL will be used, PyOpenGL is a
cross platform Python binding to OpenGL and it can use PyGame as a
rendering context. PyOpenGL has all the functions that OpenGL 1.1
supports and can use GLUT windows as rendering context too. It has not
support for all the OpenGL extensions, but for this project there is no
need to use OpenGL extensions.\
\
Some examples on how to use the OpenGL widget framework will be created
with three objectives, first as a way to get feedback from the
community, second to test the framework and the last as a learning tool
for the community to understand how the framework works.\
\
One of the features in that I will work depending in the time, is the
collision detection, this would be very useful, because pygame doesn\'t
have collision detection for 3D objects.\
\
Deliverables:\
\
OpenGL widget components.\
Examples using OpenGL and PyGame components.\
Documentation for the OpenGL widget components.\
\
Project Schedule:\
\
An estimated project schedule:\
\
May 22: Begin the creation of the basic OpenGL components.\
Experimenting with different solutions.\
June 12: Get OpenGL and PyGame components working together.\
June 19-25: Testing period.\
Test using OpenGL Primitives.\
June 26: Creation of an example.\
July 3: Show to the community the example for feedback and then make
possible modifications.\
July 10: Begin the creation of the advanced OpenGL components.\
Experimenting with different solutions.\
Creation of the texture handler component.\
July 24 -30: Testing period.\
Test using GLU Quadrics.\
Test the camera.\
Test lighting.\
Test texture handler.\
July 31 : Creation of a second example.\
August 7: Show to the community the example for feedback and then make
possible modifications.\
August 14: Create the final documentation for the components and
examples.\
August 21: The project should be done by this date.\
\
\*I could work in collision detection, it would be very useful and I
will be working on it depending on the time left.\
\
References:\
\
1.- www.pygame.org\
2.- http://pyopengl.sourceforge.net/\
\
\
