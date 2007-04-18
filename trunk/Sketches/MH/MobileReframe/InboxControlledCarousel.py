#!/usr/bin/env python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""\
============================================================
A carousel controlled by its "inbox" instead of "next" inbox
============================================================

Identical in functionality to Kamaelia.Chassis.Carousel, except instead of
sending orders to a "next" inbox, send them to the "inbox" inbox instead.

Data that would have been sent to the "inbox" inbox can be sent to the
"data_inbox" inbox instead.



Example Usage
-------------

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



Behaviour
---------

This component behaves identically to Kamaelia.Chassis.Carousel.

The "inbox" inbox is equivalent to the "next" inbox of Carousel.
The "data_inbox" inbox is equivalent to the "inbox" inbox of Carousel.

"""

#from Kamaelia.Chassis.Carousel import Carousel
from CarouselRewrite import Carousel
from Kamaelia.Chassis.Graphline import Graphline

def InboxControlledCarousel(*argv, **argd):
    return Graphline( CAROUSEL = Carousel( *argv, **argd ),
                      linkages = {
                          ("", "inbox")   : ("CAROUSEL", "next"),
                          ("", "data_inbox") : ("CAROUSEL", "inbox"),
                          ("", "control") : ("CAROUSEL", "control"),
                          ("CAROUSEL", "outbox") : ("", "outbox"),
                          ("CAROUSEL", "signal") : ("", "signal"),
                      }
                    )

__kamaelia_prefabs__ = ( InboxControlledCarousel, )
