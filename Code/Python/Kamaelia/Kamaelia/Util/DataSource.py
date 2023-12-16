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
=====================
Data Source component
=====================

This component outputs messages specified at its creation one after another.

Example Usage
-------------

To output "hello" then "world"::
  
    pipeline(
        DataSource(["hello", "world"]),
        ConsoleEchoer()
    ).run()

    

==========================
Triggered Source component
==========================

Whenever this component receives a message on inbox, it outputs a certain message.

Example Usage
-------------

To output "wibble" each time a line is entered to the console::

    pipeline(
        ConsoleReader(),
        TriggeredSource("wibble"),
        ConsoleEchoer()
    ).run()

"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown
from .PureTransformer import PureTransformer

class DataSource(component):
    def __init__(self, messages):
        super(DataSource, self).__init__()
        self.messages = messages
        
    def main(self):
        while len(self.messages) > 0:
            yield 1
            self.send(self.messages.pop(0), "outbox")
        yield 1
        self.send(producerFinished(self), "signal")
        return

def TriggeredSource(msg):
    return PureTransformer(lambda r : msg)

__kamaelia_components__  = ( DataSource, )
__kamaelia_prefabs__  = ( TriggeredSource, )

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

    pipeline(
        DataSource( ["hello", " ", "there", " ", "how", " ", "are", " ", "you", " ", "today\r\n", "?", "!"] ),
        ConsoleEchoer()
    ).run()
