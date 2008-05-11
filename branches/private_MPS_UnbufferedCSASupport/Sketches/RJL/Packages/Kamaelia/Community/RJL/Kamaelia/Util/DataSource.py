#!/usr/bin/env python
#
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
=================
Data Source component
=================

This component outputs messages specified at its creation one after another.

Example Usage
-------------

To output "hello" then "world":
pipeline(
    DataSource(["hello", "world"]),
    ConsoleEchoer()
).run()

=================
Triggered Source component
=================

Whenever this component receives a message on inbox, it outputs a certain message.

Example Usage
-------------

To output "wibble" each time a line is entered to the console.
pipeline(
    ConsoleReader(),
    TriggeredSource("wibble"),
    ConsoleEchoer()
).run()

"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown
from PureTransformer import PureTransformer

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

TriggeredSource = lambda msg : PureTransformer(lambda r : msg)

__kamaelia_components__  = ( DataSource, )
__kamaelia_prefabs__  = ( TriggeredSource, )

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

    pipeline(
        DataSource( ["hello", " ", "there", " ", "how", " ", "are", " ", "you", " ", "today\r\n", "?", "!"] ),
        ConsoleEchoer()
    ).run()
