#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------
"""\
=======================================================
Inbox size limiting Pipelines, Graphlines and Carousels
=======================================================

Extended versions of Kamaelia.Chassis.Pipeline, Kamaelia.Chassis.Graphline and
Kamaelia.Chassis.Carousel that add the ability to specify size limits for
inboxes of components.



Example Usages
--------------

A pipeline with inbox size limits on 3 of the components' "inbox" inboxes::

    Pipeline( 5,  MyComponent(),      # 'inbox' inbox limited to 5 items
              2,  MyComponent(),      # 'inbox' inbox limited to 2 items
                  MyComponent(),      # 'inbox' inbox unlimited
              28, MyComponent()       # 'inbox' inbox limited to 28 items
            )

A graphline where component 'A' has a size limit of 5 on its "inbox" inbox; and
component 'C' has a size limit of 17 on its "control" inbox::

    Graphline( A = MyComponent(),
               B = MyComponent(),
               C = MyComponent(),
               linkages = { ... },
               boxsizes = {
                   ("A","inbox") : 5,
                   ("C","control") : 17
               }
             )

A Carousel, where the child component will have a size limit of 5 on its "inbox"
inbox::

    Carousel( MyComponent(), boxsize=5 )

Decoding a Dirac video file and saving each frame in a separate file::

    Pipeline(
        RateControlledFileReader("video.dirac", ... ),
        DiracDecoder(),
        TagWithSequenceNumber(),
        InboxControlledCarousel(
            lambda (seqnum, frame) :
                Pipeline( OneShot(frame),
                          FrameToYUV4MPEG(),
                          SimpleFileWriter("%08d.yuv4mpeg" % seqnum),
                        )
            ),
        )


More details
------------

The behaviour of these three components/prefabs is identical to their original
counterparts (Kamaelia.Chassis.Pipeline, Kamaelia.Chassis.Graphline and
Kamaelia.Chassis.Carousel).

*For Pipelines*, if you want to size limit the "inbox" inbox of a particular
component in the pipeline, then put the size limit as an integer before it.
Any component without an integer before it is left with the default of an
unlimited "inbox" inbox.

The behaviour therefore reduces back to be identical to that of the normal
Pipeline component.

*For Graphlines*, if you want to size limit particular inboxes, supply the
"boxsizes" argument with a dictionary that maps (componentName, boxName) keys
to the size limit for that box.

Again, if you don't specify a "boxsizes" argument, then behaviour is identical
to that of the normal Graphline component.

*For Carousels*, if you want a size limit on the "inbox" inbox of the child
component (created by the factory function), then specify it using the
"boxsizes" argument.

Again, if you don't specify a "boxsizes" argument, then behaviour is identical
to that of the normal Carousel component.

*InboxControlledCarousel* behaves identically to Carousel.

The "inbox" inbox is equivalent to the "next" inbox of Carousel.
The "data_inbox" inbox is equivalent to the "inbox" inbox of Carousel.


"""


from Kamaelia.Chassis.Pipeline import Pipeline as _Pipeline

def Pipeline(*components):
    """\
    Pipeline(\*components) -> new Pipeline component.

    Encapsulates the specified set of components and wires them up in a chain
    (a Pipeline) in the order you provided them.

    Keyword arguments:

    - components -- the components you want, in the order you want them wired up.
      Any Integers set the "inbox" inbox size limit for the component that follows them.
    """
    truecomponents = []

    boxsize=False
    for item in components:
        if isinstance(item,int):
            boxsize=item
        elif item is None:
            boxsize=item
        else:
            component=item
            if boxsize != False:
                component.inboxes['inbox'].setSize(boxsize)
                boxsize=False
            truecomponents.append(component)

    return _Pipeline(*truecomponents)



from Kamaelia.Chassis.Graphline import Graphline as _Graphline


def Graphline(linkages = None, boxsizes = None,**components):
    """\
    Graphline([linkages][,boxsizes],\*\*components) -> new Graphline component

    Encapsulates the specified set of components and wires them up with the
    specified linkages.

    Keyword arguments:
    
    - linkages   -- dictionary mapping ("componentname","boxname") to ("componentname","boxname")
    - boxsizes   -- dictionary mapping ("componentname","boxname") to size limit for inbox
    - components -- dictionary mapping names to component instances (default is nothing)
    """

    g = _Graphline(linkages,**components)
    
    if boxsizes is not None:
        for ((componentname,boxname),size) in boxsizes.items():
            components[componentname].inboxes[boxname].setSize(size)

    return g


from Kamaelia.Chassis.Carousel import Carousel as _Carousel

def Carousel(componentFactory, make1stRequest=False, boxsize=None):
    """\
    Carousel(componentFactory[,make1stRequest][,boxSize]) -> new Carousel component
    
    Create a Carousel component that makes child components one at a time (in
    carousel fashion) using the supplied factory function.
    
    Keyword arguments:
    
    - componentFactory -- function that takes a single argument and returns a component
    - make1stRequest   -- if True, Carousel will send an initial "NEXT" request. (default=False)
    - boxsize          -- size limit for "inbox" inbox of the created child component
    """
    if boxsize is not None:
        def setBoxSize(component):
            component.inboxes['inbox'].setSize(boxsize)
            return component
        newComponentFactory = lambda meta : setBoxSize(componentFactory(meta))
    else:
        newComponentFactory = componentFactory
        
    return _Carousel(newComponentFactory, make1stRequest)



def InboxControlledCarousel(*argv, **argd):
    """\
    InboxControlledCarousel(componentFactory[,make1stRequest][,boxSize]) -> new Carousel component
    
    Create an InboxControlledCarousel component that makes child components one at a time (in
    carousel fashion) using the supplied factory function.
    
    Keyword arguments:
    
    - componentFactory -- function that takes a single argument and returns a component
    - make1stRequest   -- if True, Carousel will send an initial "NEXT" request. (default=False)
    - boxsize          -- size limit for "inbox" inbox of the created child component
    """
    
    return Graphline( CAROUSEL = Carousel( *argv, **argd ),
                      linkages = {
                          ("", "inbox")   : ("CAROUSEL", "next"),
                          ("", "data_inbox") : ("CAROUSEL", "inbox"),
                          ("", "control") : ("CAROUSEL", "control"),
                          ("CAROUSEL", "outbox") : ("", "outbox"),
                          ("CAROUSEL", "signal") : ("", "signal"),
                      }
                    )

__kamaelia_prefabs__ = ( Pipeline, Graphline, Carousel, InboxControlledCarousel, )

