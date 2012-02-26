#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Needed to allow import
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
    