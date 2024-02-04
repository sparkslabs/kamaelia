---
pagename: Projects/Soc2006/DistributedPhysics
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
SoC Project: Distributed Physics
================================

There was one project application in this area that is summarised here.
This page contains the depersonalised content, which can be consolidated
as necessary. The depersonalisation is for privacy reasons, credit is
here due to those who spent the time writing these descriptions.\
\

### Project Title: Distributed physics

Benefits to Kamaelia:\
By distributing the physical calculations across distributed components
there will be no direct benefit to the BBC audience, but for BBC and
everyone else from the community using Kamaelia. The reason for this is
the introduction of dual- and quad-core processors into the home user
market last or next year respectively. Software designed to run on one
core only is expected to obtain serious performance problems or at least
waste most of the available computation power. With a distributed
physical component Kamaelia will be ready for this forthcoming challenge
since this new component will speed up working with every software which
uses the current physics component.\
\
Synopsis:\
The physics component in Kamaelia is used by different software, e.g.
the Axon Visualiser. The goal of this project is to enhance the current
physics component by parallelization. This will expose the computational
power of the next generation processors decisively.\
\
The Kamaelis physics component is (as a lot of other physics systems) a
N-body simulation. The parallelisation of such systems has been an
active area of research for a long time. Therefore a lot of different
approaches have been published and some of them will be tested as part
of this project. Furthermore it is very interesting to optimize the
physics component not just by using distributed components but also
optimizing the component itself. This could be done e.g. with the help
of modern graphic processing units (GPUs) because physical calculations
seem to fit to GPU architectures quite well \[1\].\
\
Deliverables:\
The deliverables are divided into two categories. The first category
contains everything that will be delivered at the end of the project.
The second category consists of optional components which will not all
be delivered. The decision regarding the optional component will be made
by weighing up the general usefulness for the Kamaelia project and the
available time.\
\
will be delivered:\
- a distributed physics component\
- unit tests proving the correct functionality of the distributed
physics component compared to the current physics component\
- a complex test case showing the possible speedup of the new component
(maybe part of the unit tests)\
- documentation describing the final parallelization approach and how
the new component should to be used\
\
optional:\
- implementation of different parallelization approaches to see which of
them fits best to Kamaelia\
- optimizing the component itself e.g. with the use of GPUs\
- - back porting the optimizations to the old physic component if there
is still need for that component\
\
Project Details:\
At the beginning of the project I will improve my knowledge of
Python/PyUnit and have a closer look at the Kamaelia source code to see
how the current physics component and Kamaelia in general are
implemented. After completing this first step I will write test cases
(unit tests) based on the current physics component. These tests will
later be used to verify that the new distributed physics component
produces the same results as the old one. The tests itself will be
written by using PyUnit.\
\
If the unit tests have covered all relevant parts of the physics
component, the development of the new distributed physics component will
start. As almost every part of Kamaelia is written in Python, the
distributed physics component will be written in Python, too. The
communication between the components will be handled using the message
system of Kamaelia. This will help keeping the Kamaelia design clear and
easy to maintain.\
\
When different parallelization ideas will be implemented, these will
result in multiple new components for the time being. But at the end of
development time, there will be only one of these coponents being chosen
to be released as a part of Kamaelia. Releasing multiple components
differing just in the algorithm normally results in more confusion for
the developers using the Kamaelia library than it would help choosing
the best fitting algorithm for the current situation.\
\
Whereas the first implementation of the distributed physics component
will be based on the idea of just dividing the world into N parts (with
N being the number of components available) and distribute them across
the multiple physics components, the optimized components could
incorporate a lot of different algorithms like the methods by Barnes and
Hut \[2\] or the fast multipole method \[3\].\
\
When the physical calculations will be optimized by using a GPU this
could be by the help of PyGPU \[4\] PyGPU seems to be in an early stage
of development and needs to be evaluated first, but after all it looks
promising.\
\
Project Schedule:\
After the brief outline of the schedule above, I give a more detailed
schedule now:\
\
      24.05.06 - Project start\
until 07.06.06 - Improving my Python/PyUnit knowledge and have a close
look at the Kamaelia source\
until 17.06.06 - Writing unit tests for the physics component\
      26.06.06 - Mid-term evaluation - There should be an early working
distributed physics component be available, but it will not pass all
test cases and may still contain some major bugs (\"alpha\" stage)\
until 08.07.06 - Completion of the first distributed physics component;
completing of all test cases\
until 15.07.06 - Writing of a test case to be used for performance
testing and comparing the speed of the old and the new versions of the
physics component\
until 07.08.06 - Working on the optional part - exact timetable depends
on which optional deliverable will be worked on\
until 14.08.06 - Writing the final documentation\
until 21.08.06 - Polish both the code and the documentation.\
      21.08.06 - Project end\
\
References:\
\[1\] http://developer.nvidia.com/object/havok-fx-gdc-2006.html\
\[2\] \'A Hierarchical O(N log N) Force Calculation Algorithm\', Josh
Barnes & Piet Hut, 1986. Nature 324, 446.\
\[3\] \'A Practical Comparison of N-Body Algorithms\', Guy Blelloch and
Girija Narlikar, 1997, Parallel Algorithms. Series in Discrete
Mathematics and Theoretical Computer Science, Volume 30\
\[4\] http://www.cs.lth.se/home/Calle\_Lejdfors/pygpu/\
\
\
\
\
