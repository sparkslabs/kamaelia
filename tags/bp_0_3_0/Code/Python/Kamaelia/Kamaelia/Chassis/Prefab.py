#!/usr/bin/env python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
#
#
# This will be a collection of functions that act as prefabs. That
# is they take a collection of arguments that will be linked up in
# a standardised way.
#

from Kamaelia.Util.Graphline import Graphline

#
# Automated "What are arguments should I use next time for my reusable component?" prefab.
#
# Takes a carousel that will repeatedly create components of particular type.
# It asks the chooser what the arguments should be for the next item.
#
# Purpose of carousel : 
#    Repeatedly creates a component. 
#    It creates the component with a set of arguments. 
#    The magic is that it can recieve those arguments on "next" inbox.
#    Further magic: it can ask something else to give it it's "next" set of arguments
# 
# Purpose of chooser : 
#    To step through a list of things given to it.
#    When asked "what next" it provides the next in the list.
#
# Combination, for example, allows you to wire up a playlist to something reusable
# that reads files at a given rate.
#
# Equally it could be a list of videos passed to a reusable video player
# It could be a list of pictures to be passed to a reusable picture viewer.
# It could even be a list shell commands passed to a reusable shell/system caller.
# etc.
#
# Currently the name reflects design, not what it can *do*. 
#

def JoinChooserToCarousel(chooser, carousel):  # CHASSIS
    """Combines a Chooser with a Carousel
           chooser = A Chooser component, or any with similar behaviour and interfaces.
           carousel = A Carousel component, or any with similar behaviour and interfaces.
       This component encapsulates and connects together a Chooser and a Carousel component.

       The chooser must have an inbox that accepts 'next' style commands, and an outbox for outputting
       the next file information.

       The carousel must have a 'next' inbox for receiving next file info, and a 'requestNext'
       outbox for outputting 'next' style messages.
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
