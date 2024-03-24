#!/usr/bin/python
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

# Checked 2024/03/24

import Axon
from Kamaelia.Visualisation.Axon.AxonVisualiserServer import AxonVisualiser
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines import chunks_to_lines
from Kamaelia.Chassis.Pipeline import Pipeline

class Source(Axon.Component.component):
    "A simple data source"
    def __init__(self, data=None):
        super(Source, self).__init__()
        if data == None: data = []
        self.data = data

    def main(self):
        for item in iter(self.data):
            self.send(item, "outbox")
            yield 1

Pipeline(
        ConsoleReader(),
        Source([b"""\
ADD NODE Source Source randompos component
ADD NODE Source#inbox inbox randompos inbox
ADD NODE Source#outbox outbox randompos outbox
ADD LINK Source Source#inbox
ADD LINK Source Source#outbox
ADD NODE Sink Sink randompos component
ADD NODE Sink#inbox inbox randompos inbox
ADD NODE Sink#outbox outbox randompos outbox
ADD LINK Sink Sink#inbox
ADD LINK Sink Sink#outbox
ADD LINK Source#outbox Sink#inbox
ADD LINK Sink#outbox Source#inbox
"""]),
        chunks_to_lines(),
        lines_to_tokenlists(),
        AxonVisualiser(),
        ConsoleEchoer(),
).run()
