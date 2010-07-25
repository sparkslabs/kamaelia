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
"""
=======================
Triggered File Reader
=======================

This component accepts a filepath as an "inbox" message, and outputs the
contents of that file to "outbox". All requests are processed sequentially.

This component does not terminate.
"""

from Axon.Component import component

class TriggeredFileReader(component):
    """\
    TriggeredFileReader() -> component that creates and writes files 
    """
    Inboxes = { "inbox" : "filepaths to read",
				"control" : "UNUSED"
			  }
    Outboxes = { "outbox" : "file contents, 1 per message",
				 "signal" : "UNUSED"
			   }
	
    def __init__(self):
        super(TriggeredFileReader, self).__init__()
		
    def readFile(self, filename):
        """Read data out of a file"""
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
                #print "Read file " + command
                self.send(self.readFile(command), "outbox")				
            self.pause()
