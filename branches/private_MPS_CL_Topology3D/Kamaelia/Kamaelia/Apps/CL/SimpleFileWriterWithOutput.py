#!/usr/bin/env python
#
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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

from Kamaelia.File.Writing import SimpleFileWriter

class SimpleFileWriterWithOutput(SimpleFileWriter):
    """\
    SimpleFileWriter(filename) -> component that writes data to the file

    Writes any data sent to its inbox to the specified file.
    
    Send the filename to its outbox.
    """
    def __init__(self, filename, mode = "wb"):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(SimpleFileWriterWithOutput, self).__init__(filename)
    
    def main(self):
        """Main loop"""
        self.file = open(self.filename, self.mode, 0)
        done = False
        while not done:
            yield 1
            
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                self.writeData(data)
                self.send(self.filename, "outbox")
            
            if self.shutdown():
                done = True
            else:
                self.pause()


__kamaelia_components__  = ( SimpleFileWriterWithOutput, )
    