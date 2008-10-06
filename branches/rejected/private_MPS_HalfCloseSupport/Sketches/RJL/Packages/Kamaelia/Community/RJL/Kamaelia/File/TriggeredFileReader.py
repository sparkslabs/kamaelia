#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# Licensed to the BBC under a Contributor Agreement: RJL

"""\
=======================
Triggered File Reader
=======================

This component accepts a filepath as an "inbox" message, and outputs the
contents of that file to "outbox". All requests are processed sequentially.

This component does not terminate.

Drawback - this component uses blocking file reading calls but does not
run on its own thread.
"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown

class TriggeredFileReader(component):
    """\
    TriggeredFileReader() -> component that reads arbitrary files 
    """
    Inboxes = {
        "inbox"   : "filepaths to read",
        "control" : "Shut me down"
    }
    Outboxes = {
        "outbox"  : "file contents, 1 per message",
        "signal"  : "Signal my shutdown with producerFinished"
    }
	
    def __init__(self):
        super(TriggeredFileReader, self).__init__()
		
    def readFile(self, filename):
        """Read data out of a file"""
        print "readFile(" + filename + ")"
        file = open(filename, "rb", 0)
        data = file.read()
        file.close()
        return data

    def main(self):
        """Main loop"""
        while 1:
            yield 1

            while self.dataReady("inbox"):
                command = self.recv("inbox")
                self.send(self.readFile(command), "outbox")				
            
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdown):
                    self.send(producerFinished(self), "signal")
                    return
            
            self.pause()

__kamaelia_components__  = ( TriggeredFileReader, )

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

    # Example - display the contents of files whose names are entered
    pipeline(
        ConsoleReader(eol=""),
        TriggeredFileReader(),
        ConsoleEchoer()
    ).run()
