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
#
"""\
================================
Pre-fabrication function chassis
================================

This is a collection of functions that link up components standardised ways.

They take a collection of components as arguments, and then wire them up in a
particular fashion. These components are children inside the prefab.



JoinChooserToCarousel
---------------------

Automated "what arguments should I use for my next reusable component?"

Take a Carousel that makes components on request from a set of arguments.
Take a Chooser that responds to request for the 'next' set of arguments.

This pre-fab is a component that wires them together. When the Carousel
requests the arguments for the next component, the Chooser can respond with
them.

For example, you could wire up a playlist to something reusable that reads
files at a given rate. Alternatively, it could be a list of videos or
pictures passed to a reusable media viewer. It could even be a list of shell
commands passed to a reusable shell/system caller.



Example Usage
~~~~~~~~~~~~~

Reading from a playlist of files::

    def makeFileReader(filename):
        return ReadFileAdapter(filename = filename, ...other args... )

    reusableFileReader = Carousel componentFactory = makeFileReader)
    playlist = Chooser(["file1","file2" ... ])

    playlistreader = JoinChooserToCarousel(playlist, reusableFileReader)
    playlistreader.activate()



More detail
~~~~~~~~~~~

Any component can be used that has the expected inboxes and outboxes, and
which behaves in a relevant manner.

Chooser must have inboxes "inbox" and "control" and outboxes "outbox" and
"signal".

Carousel must have inboxes "inbox", "control" and "next" and outboxes
"outbox", "signal" and "requestNext".

The Chooser and Carousel are encapsulated within this prefab component as
children.

"inbox", "outbox" and "signal" of the Carousel are "inbox", "outbox" and
"signal" of this prefab.

Messages sent to this prefab's "control" inbox go to the Chooser, which
should then pass it onto the Carousel, allowing shutdown.



To do
~~~~~

This prefab needs a better name - it currently describes its design, not
what its for.
"""

from Kamaelia.Chassis.Graphline import Graphline


def JoinChooserToCarousel(chooser, carousel):  # CHASSIS
    """
    JoinChooserToCarousel(chooser, carousel) -> component containing both wired up
    
    Wires up a Chooser and a Carousel, so when the carousel requests the next item,
    the Chooser supplies it.
    
    Keyword arguments:
    
    - chooser   -- A Chooser component, or one with similar interfaces
    - carousel  -- A Carousel component, or one with similar interfaces
    """

    return Graphline(CHOOSER = chooser,
                     CAROUSEL = carousel,
                     linkages = {
                         ("CHOOSER", "outbox")        : ("CAROUSEL", "next"),
                         ("CHOOSER", "signal")        : ("CAROUSEL", "control"),
                         ("self", "inbox")            : ("CAROUSEL", "inbox"),
                         ("self", "control")          : ("CHOOSER", "control"),
                         ("CAROUSEL", "requestNext") : ("CHOOSER", "inbox"),
                         ("CAROUSEL", "outbox")      : ("self", "outbox"),
                         ("CAROUSEL", "signal")      : ("self", "signal")
                     }
    )

__kamaelia_prefabs__ = ( JoinChooserToCarousel, )
