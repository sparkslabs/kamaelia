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
