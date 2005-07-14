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

from Sequencer import Sequencer
from ReadFileAdapter import ReadFileAdapter
from RateControl import RateControl

from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Graphline import Graphline


def JoinChooserSequencer(chooser, sequencer):
    """Joins a chooser to a sequencer.
       The chooser must have an inbox that accepts 'next' style commands, and an outbox for outputting
       the next file information.
       The sequencer must have a 'next' inbox for receiving next file info, and a 'requestNext'
       outbox for outputting 'next' style messages.
    """
    return Graphline(CHOOSER = chooser, SEQUENCER = sequencer,
                     linkages = { ("CHOOSER", "outbox")        : ("SEQUENCER", "next"),
                                  ("CHOOSER", "signal")        : ("SEQUENCER", "control"),
                                  ("self", "inbox")            : ("SEQUENCER", "inbox"),
                                  ("SEQUENCER", "requestNext") : ("CHOOSER", "inbox"),
                                  ("SEQUENCER", "outbox")      : ("self", "outbox"),
                                  ("SEQUENCER", "signal")      : ("self", "signal")
                                }
                    )

    
def RateControlledReadFileAdapter(filename, readmode = "bytes", **rateargs):
    """Returns a component encapsulating RateControl and ReadFileAdapter.
         filename   = filename
         readmode   = "bytes" or "lines"
         **rateargs = named arguments to be passed to RateControl
    """
    return Graphline(RC  = RateControl(**rateargs),
                     RFA = ReadFileAdapter(filename, readmode),
                     linkages = { ("RC",  "outbox")  : ("RFA", "inbox"),
                                  ("RFA", "outbox")  : ("---", "outbox"),
                                  ("RFA", "signal")  : ("RC",  "control"),
                                  ("RC",  "signal")  : ("---", "signal"),
                                  ("---", "control") : ("RFA", "control")
                                }
                    )


def ReadMultiFileAdapter(readmode = "bytes"):
    """Returns a Sequencer for file reading, with no rate control component.
    """
    def factory(filename):
        return ReadFileAdapter(filename=filename, readmode=readmode)
    
    return Sequencer( factory )


def PerFileRateReadMultiFileAdapter(readmode = "bytes"):
    """Returns a Sequencer for file reading, with rates specified per file.
       sequencer 'next' argument = (filename, rateargdict)
    """
    def factory(arg):
        filename, rateargs = arg
        return RateControlledReadFileAdapter(filename, readmode, **rateargs)

    return Sequencer( factory )



def FixedRateReadMultiFileAdapter(readmode = "bytes", **rateargs):
    """Returns a Sequencer, liked with a RateControl.
       The Sequencer's 'requestNext' and 'next' postboxes are accessible.
    """
    return Graphline(RC  = RateControl(**rateargs),
                     SEQ = ReadMultiFileAdapter(readmode),
                     linkages = { ("self", "inbox")      : ("RC", "inbox"),
                                  ("self", "control")    : ("RC", "control"),
                                  ("RC", "outbox")       : ("SEQ", "inbox"),
                                  ("RC", "signal")       : ("SEQ", "control"),
                                  ("SEQ", "outbox")      : ("self", "outbox"),
                                  ("SEQ", "signal")      : ("self", "signal"),
                                  ("SEQ", "requestNext") : ("self", "requestNext"),
                                  ("self", "next")       : ("SEQ", "next")
                                }
                    )
                     


if __name__ == "__main__":

   from Axon.Scheduler import scheduler
   from Kamaelia.Util.ConsoleEcho import consoleEchoer
   from InfiniteChooser import InfiniteChooser


#   test = "RateControlledReadFileAdapter"
#   test = "PerFileRateReadMultiFileAdapter"
   test = "FixedRateReadMultiFileAdapter"

   if test == "RateControlledReadFileAdapter":
   
        pipeline( RateControlledReadFileAdapter("./Sequencer.py", readmode = "lines", rate=20, chunksize=1),
                  consoleEchoer()
                ).activate()

   elif test == "PerFileRateReadMultiFileAdapter":
        def filelist():
        #       while 1:
                yield ( "./Sequencer.py", {"rate":500, "chunkrate":1} )
                yield ( "./Sequencer.py", {"rate":400, "chunkrate":20} )
                yield ( "./Sequencer.py", {"rate":1000, "chunkrate":100} )
        
        pipeline( JoinChooserSequencer( InfiniteChooser(filelist()),
                                        PerFileRateReadMultiFileAdapter(readmode="bytes")
                                      ),
                  consoleEchoer()
                ).activate()

   elif test == "FixedRateReadMultiFileAdapter":
        files = [ "./Sequencer.py" for _ in range(0,3) ]
        rate  = {"rate":400, "chunkrate":100}
       
        pipeline( JoinChooserSequencer( InfiniteChooser(files),
                                        FixedRateReadMultiFileAdapter(readmode="bytes", **rate)
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
    
