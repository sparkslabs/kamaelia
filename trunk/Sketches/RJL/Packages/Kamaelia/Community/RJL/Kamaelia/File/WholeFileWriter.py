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
Whole File Writer
=======================

This component accepts file creation jobs and signals the completion of each
jobs. Creation jobs consist of a list [ filename, contents ] added to "inbox".
Completion signals consist of the string "done" being sent to "outbox".

All jobs are processed sequentially.

This component does not terminate.
"""

from Axon.Component import component

class WholeFileWriter(component):
    """\
    WholeFileWriter() -> component that creates and writes files 
    
    Uses [ filename, contents ] structure to file creation messages in "inbox"
    """
    Inboxes = {
        "inbox" : "file creation jobs",
        "control" : "UNUSED"
    }
    Outboxes = {
        "outbox" : "filename written",
        "signal" : "UNUSED"
    }
    
    def __init__(self):
        super(WholeFileWriter, self).__init__()
    	
    def writeFile(self, filename, data):
        """Writes the data to a new file"""
        file = open(filename, "wb", 0)
        data = file.write(data)
        file.close()
		
    def main(self):
        """Main loop"""
        while 1:
            yield 1
            
            if self.dataReady("inbox"):
                command = self.recv("inbox")
                self.writeFile(command[0], command[1])
                self.send(command[0], "outbox")
            else:
                self.pause()

__kamaelia_components__  = ( WholeFileWriter, )
