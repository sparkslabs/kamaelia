#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import Axon
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess


class Router(component):
    """\
    Router([(rule,dest)][,(rule,dest)]...) -> new Router component.
    
    Component that routes incoming messages to destination outboxes according to
    whether or not they pass the specified rules.
    """
    def __init__(self, *routing):
        for (rule,destination) in routing:
            self.Outboxes[destination] = "Routing destination"
        
        super(Router,self).__init__()
        self.routing = routing
        
    def shutdown(self):
       """Return 0 if a shutdown message is received, else return 1."""
       if self.dataReady("control"):
           msg=self.recv("control")
           if isinstance(msg,producerFinished) or isinstance(msg,shutdownMicroprocess):
               self.send(producerFinished(self),"signal")
               return 0
       return 1
        
    def main(self):
        while self.shutdown():
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                for (rule,destination) in self.routing:
                    if rule(data):
                        self.send(data,destination)
            self.pause()
            yield 1

class TwoWaySplitter(Axon.Component.component):
    Outboxes = { "outbox"  : "",
                 "outbox2" : "",
                 "signal"  : "",
                 "signal2" : "",
               }

    def main(self):
        done=False
        while not done:

            while self.dataReady("inbox"):
                data = self.recv("inbox")
                self.send(data, "outbox")
                self.send(data, "outbox2")

            while self.dataReady("control"):
                data = self.recv("control")
                self.send(data, "signal")
                self.send(data, "signal2")
                if isinstance(data, (producerFinished, shutdownMicroprocess)):
                    return

            self.pause()
            yield 1

class ConditionalSplitter(Axon.Component.component): # This is a data tap/siphon/demuxer
    Outboxes = ["true", "false"]
    def condition(self, data): return True
    def true(self,data): self.send(data, "true")
    def false(self,data): self.send(data, "false")
    def main(self):
        while 1:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                if self.condition(data):
                    self.true(data)
                else:
                    self.false(data)
            if not self.anyReady():
                self.pause()
            yield 1
