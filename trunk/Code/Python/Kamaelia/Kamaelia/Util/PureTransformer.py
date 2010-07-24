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
"""\
==========================
Pure Transformer component
==========================

This component applies a function specified at its creation to messages
received (a filter). If the function returns None, no message is sent,
otherwise the result of the function is sent to "outbox".

Example Usage
-------------

To read in lines of text, convert to upper case and then write to the console::
    
    Pipeline(
        ConsoleReader(),
        PureTransformer(lambda x : x.upper()),
        ConsoleEchoer()
    ).run()

"""

from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess,shutdown

class PureTransformer(component):
    def __init__(self, function=None):
        super(PureTransformer, self).__init__()
        if function:
            self.processMessage = function
        
    def processMessage(self, msg):
        pass
        
    def main(self):
        while 1:
            yield 1
            while self.dataReady("inbox"):
                returnval = self.processMessage(self.recv("inbox"))
                if returnval != None:
                    self.send(returnval, "outbox")
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdown):
                    self.send(producerFinished(self), "signal")
                    return
            self.pause()

__kamaelia_components__  = ( PureTransformer, )

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

    # Example - prepend "foo" and append "bar" to lines entered.
    pipeline(
        ConsoleReader(eol=""),
        PureTransformer(lambda x : "foo" + x + "bar!\n"),
        ConsoleEchoer()
    ).run()
