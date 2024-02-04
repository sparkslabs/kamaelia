---
pagename: Developers/Projects/3DTopologyVisualiser
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia: 3DTopologyVisualiser {#kamaelia-3dtopologyvisualiser align="left"}
==============================

\

What is it?
-----------

This is a Google Summer of Code project. The project is to parse
relationships defined in database, a file or console inputs and then
show them in 3D graph. Current Kamaelia topology visualiser is
implemented by PyGame which is limited to 2D graph. This project is to
extend topology visualiser by OpenGL to be able to show relationships in
3D domain which is potentially clearer and can carry more information.\
\
First, an OpenGL version of topology visualiser, having the same
functions with 2D topology visualiser, is developed. Then it is extended
to make particles customizable, to make topology visualiser able to show
hierarchical structures and able to show 3D special behaviours (e.g.
rotate and move nearer or farther from the viewer). Finally, the
visualiser is used to implement two applications, i.e. FOAFViewer to
draw the relations of friends and CollabViewer to draw the collaboration
relations of organizations.\
\

Where do I get it & install it?
-------------------------------

-   svn checkout
    https://kamaelia.googlecode.com/svn/branches/private\_CL\_Topology3D\
-   cd private\_CL\_Topology3D/Axon
-   sudo python setup.py install
-   cd private\_CL\_Topology3D/Kamaelia
-   sudo python setup.py install

```{=html}
<!-- -->
```

Planned Schedule:
-----------------

-   Complete TODO list and optimise code in terms of design and running
    speed\

Progress (dates related to the weekly meeting - these are the \"DONE\" lines)
-----------------------------------------------------------------------------

-   12/5 - Parsed simple relations and shew them in TopologyView
-   20/5 - Made particle\'s colour customizable\
-   1/6 - Added picture support for particles, (reviewed
    private\_MPS\_JL\_IRCSupport/)
-   9/6 - Solved some problems with the picture support, and extended
    particles to make more properties customizable
-   16/6 - Extended the viewer to be able to update the figure
    dynamically; added link arrow and text; cleaned up cod and finished
    up the PyGame version extention; prepared for OpenGL version coding
-   23/6 - Started OpenGL extention of TopologyView and base coding,
    experimented on different particles (sphere and cube) and
    TopologyViewer3D. First, let SimpleTopologyViewer3D subclass
    OpenGLComponent, draw particles from OpenGL display list. It works,
    but it\'s not ideal because TopologyViewer3D is not a typical
    OpenGLComponent (it only create an PyGame OpenGL display, has no
    position, rotation and other attributes) and OpenGLComponent cannot
    provide a loop for receiving instructions from inbox. Then, change
    SimpleTopologyViewer3D\'s parent from OpenGLComponent to component,
    and use OpenGLComponent Button as particle,
    MatchedTranslationInteractor as dragHandler just for demonstration
    because they have all attributes particle needs (OpenGL project and
    event handling), though their component properties are reductant and
    are not easy to update. It also works.
-   30/6 - Started TopologyViewer3D and Particles3D coding from stratch
    (inherit component rather than OpenGLComponent). Particles3D: OpenGL
    cuboid with label, position, size, rotation customizable and
    updatable; TopologyViewer3D: add particles, random position
    generation and event handling (click and drag).\
-   7/7 - Added vewer position change, rotation and  selection functions
    to TopologyViewer3D; extended ParticleSystem to be able to make
    selected particles not subject to physics laws, otherwise selected
    particles are hard to be rotated\
-   14/7 -  Added multiple nodes selection, selected nodes rotation,
    mouse motion rotation, key holding handling functions; changed
    rotation behaviour to rotate around common centre from rotate around
    local axises; fixed several rotation bugs; filled out the mid-term
    survey\
-   21/7 - Cleaned code and improved design (e.g. abstract Particles3D
    and concrete rendering classes subclass it, such as
    CuboidParticle3D, SphereParticle3D and TeapotParticle3D), wrote
    simple documentations, posted the work of TopologyViewer3D and
    Particles3D to the list and asked for feedbacks; coded simple
    hierarchy structure\
-   28/7 - Improved, extended and finished up hierarchy structure;
    started FOAF app coding which shows the connections between friends
    and experimented on SPARQL, rdflib and librdf to find foaf data from
    an uri and fetch N layers\' FOAF data from a uri as a preparation\
-   4/8 - Finished RDFParser to parse FOAF data  and linked it to
    TopologyViewer3D to draw FOAF data; extended TopologyViewer3D and
    Particles3D to accept more parameters; fixed several bugs of
    TopologyViewer3D; created my branch private\_CL\_Topology3D for this
    project; posted the work of FOAF viewer to the list and asked for
    feedbacks
-   11/8 - Coded a new app of TopologyViewer3D (collaboration viewer)
    which shows the collaboration relations of organizations; created
    Kamaelia.Codec.JSON JSONEncoder and JSONDecoder to serialise data;
    extended SimpleFileWriter in Writing.py to output the file name
    written; created Kamaelia.Util.DictChooser DictChooser to choose
    different view of CollabViewer (e.g. orgView, staffView); cleaned
    code and added documentation.
-   18/8 - Added more documentation and comments; further cleaned up
    code; improved code with respect to Joe\'s suggestion; reviewed
    Dave\'s code\

Log/Discussion
--------------

I\'ve removed the installation section above since it bore no
resemblance to reality\
\-- Michael, June 2008\
\
\
\
