# -*- coding: utf-8 -*-
# Helper classes for HTTP
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

from Axon.Component import component

"""HTTPMakePostRequest is used to turn messages into HTTP POST requests
for SimpleHTTPClient.
"""

class HTTPMakePostRequest(component):
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
            
            self.pause()
