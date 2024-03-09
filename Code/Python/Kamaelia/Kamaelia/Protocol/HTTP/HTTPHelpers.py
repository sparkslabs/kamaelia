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

"""Helper classes and components for HTTP"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown

class HTTPMakePostRequest(component):
    """\
    HTTPMakePostRequest is used to turn messages into HTTP POST requests
    for SimpleHTTPClient.
    """
    def __init__(self, uploadurl):
        super(HTTPMakePostRequest, self).__init__()
        self.uploadurl = uploadurl
        
    def main(self):
        while 1:
            yield 1
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                msg = { "url" : self.uploadurl, "postbody" : msg }
                self.send(msg, "outbox")
            
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdown):
                    self.send(producerFinished(self), "signal")
                    return

            self.pause()

__kamaelia_components__ = ( HTTPMakePostRequest, )
            
if __name__ == "__main__":
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
    
    postscript = input("Post Script URL: ") # e.g. "http://www.example.com/upload.php"
    
    pipeline(
        ConsoleReader(eol=""),
        HTTPMakePostRequest(postscript),
        SimpleHTTPClient()
    ).run()
