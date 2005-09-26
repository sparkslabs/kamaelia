#!/usr/bin/python
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
# A collection of factory methods for making useful use of ReadFileAdapter

from Carousel import Carousel
from ReadFileAdapter import ReadFileAdapter
from RateControl import RateControl

from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Graphline import Graphline


class ReadFileAdapter_Carousel(Carousel):
    """A Carousel for file reading (with no rate control).
       Takes string filenames.
    """
    def __init__(self, readmode = "bytes"):
        """Initialisation
        """
        def RFAfactory(filename):
            return ReadFileAdapter(filename=filename, readmode=readmode)

        super(ReadFileAdapter_Carousel, self).__init__( RFAfactory )
        
class RateControlledReadFileAdapter_Carousel(Carousel):
    """A Carousel for file reading (with rate control specified per file).
       Takes ( filename, rateargdict )
    """

    def __init__(self, readmode = "bytes"):
        def RCRFAfactory(arg):
            filename, rateargs = arg
            return RateControlledReadFileAdapter(filename, readmode, **rateargs)

        super(RateControlledReadFileAdapter_Carousel, self).__init__( RCRFAfactory )

def JoinChooserToCarousel(chooser, carousel):
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

def RateControlledReadFileAdapter(filename, readmode = "bytes", **rateargs):
    """ReadFileAdapter combined with a RateControl component
       Returns a component encapsulating a RateControl and ReadFileAdapter components.
            filename   = filename
            readmode   = "bytes" or "lines"
            **rateargs = named arguments to be passed to RateControl
        """
    return Graphline(RC  = RateControl(**rateargs),
                     RFA = ReadFileAdapter(filename, readmode),
                     linkages = { ("RC",  "outbox")  : ("RFA", "inbox"),
                                  ("RFA", "outbox")  : ("self", "outbox"),
                                  ("RFA", "signal")  : ("RC",  "control"),
                                  ("RC",  "signal")  : ("self", "signal"),
                                  ("self", "control") : ("RFA", "control")
                                }
    )

def FixedRate_ReadFileAdapter_Carousel(readmode = "bytes", **rateargs):
    """A file reading carousel, that reads at a fixed rate.
       Takes filenames on its inbox
    """
    return Graphline(RC       = RateControl(**rateargs),
                     CAR      = ReadFileAdapter_Carousel(readmode),
                     linkages = { 
                         ("self", "inbox")      : ("CAR", "next"),
                         ("self", "control")    : ("RC", "control"),
                         ("RC", "outbox")       : ("CAR", "inbox"),
                         ("RC", "signal")       : ("CAR", "control"),
                         ("CAR", "outbox")      : ("self", "outbox"),
                         ("CAR", "signal")      : ("self", "signal"),
                         ("CAR", "requestNext") : ("self", "requestNext"),
                         ("self", "next")       : ("CAR", "next")
                     }
    
    )


if __name__ == "__main__":

   from Axon.Scheduler import scheduler
   from Kamaelia.Util.ConsoleEcho import consoleEchoer
   from InfiniteChooser import InfiniteChooser


#   test = "RateControlledReadFileAdapter"
   test = "PerFileRateReadMultiFileAdapter"
#   test = "FixedRateReadMultiFileAdapter"

   if test == "RateControlledReadFileAdapter":
   
        pipeline( RateControlledReadFileAdapter("./Carousel.py",
                                                readmode = "lines",
                                                rate=20,
                                                chunksize=1),
                  consoleEchoer()
                ).activate()

   elif test == "PerFileRateReadMultiFileAdapter":
        def filelist():
        #       while 1:
                yield ( "./Carousel.py", {"rate":500, "chunkrate":1} )
                yield ( "./Carousel.py", {"rate":400, "chunkrate":20} )
                yield ( "./Carousel.py", {"rate":1000, "chunkrate":100} )
        
        pipeline( JoinChooserToCarousel(
                      InfiniteChooser(filelist()),
                      RateControlledReadFileAdapter_Carousel(readmode="bytes")
                    ),
                  consoleEchoer()
                ).activate()

   elif test == "FixedRateReadMultiFileAdapter":
        files = [ "./Carousel.py" for _ in range(0,3) ]
        rate  = {"rate":400, "chunkrate":100}
       
        pipeline( JoinChooserToCarousel(
                      InfiniteChooser(files),
                      FixedRate_ReadFileAdapter_Carousel(readmode="bytes", **rate)
                    ),
                  consoleEchoer()
                ).activate()

   else:
       pass

   if 0:
        from Kamaelia.Internet.TCPClient import TCPClient
        from Kamaelia.Util.Introspector import Introspector
        pipeline(Introspector(), TCPClient("127.0.0.1",1500)).activate()

   scheduler.run.runThreads(slowmo=0)
    
