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
"""
==================
Simple File Writer
==================

This component writes any data it receives to a file.


Example Usage
-------------

Copying a file::

    from Kamaelia.File.Writing import SimpleFileWriter

    Pipeline(RateControlledFileReader("sourcefile",rate=1000000),
             SimpleFileWriter("destinationfile")
            ).activate()



More detail
-----------

Any data sent to this component's inbox is written to the specified file. 
Any existing file with the same name is overwritten.

The file is opened for writing when the component is activated, and is closed
when it shuts down.

This component terminates, closing the file, if it receives a
shutdownMicroprocess or producerFinished message on its "control" inbox. The
message is passed on out of its "signal" outbox.



Development history
-------------------

SimpleFileWriter
- prototyped in /Sketches/filereading/WriteFileAdapter.py
"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class SimpleFileWriter(component):
    """\
    SimpleFileWriter(filename) -> component that writes data to the file

    Writes any data sent to its inbox to the specified file.
    """
    Inboxes = { "inbox" : "data to write to file",
                "control" : "to receive shutdown/finished messages"
              }
    Outboxes = { "outbox" : "not used",
                 "signal" : "shutdown/finished signalling"
               }
    
    def __init__(self, filename, mode = "wb"):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        self.filename = filename
        self.mode = mode
        super(SimpleFileWriter, self).__init__()
        
    def writeData(self, data):
        """Writes the data to the file"""
        data = self.file.write(data)

        
    def main(self):
        """Main loop"""
        self.file = open(self.filename, self.mode, 0)
        done = False
        while not done:
            yield 1
            
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                self.writeData(data)
            
            if self.shutdown():
                done = True
            else:
                self.pause()

                
    def shutdown(self):
        """\
        Returns True if a shutdownMicroprocess or producerFinished message is received.

        Also passes the message on out of the "signal" outbox.
        """
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                self.send(msg, "signal")
                return True
        return False
        
                
    def closeDownComponent(self):
        """Closes the file handle"""
        self.file.close()

__kamaelia_components__  = ( SimpleFileWriter, )
      
if 1:
    if __name__ == "__main__":
        from Kamaelia.Chassis.Pipeline import Pipeline
        from Kamaelia.File.Reading import RateControlledFileReader

        Pipeline( RateControlledFileReader("Writing.py"),
                  SimpleFileWriter("/tmp/tmp_Writing.py")
                ).run()
