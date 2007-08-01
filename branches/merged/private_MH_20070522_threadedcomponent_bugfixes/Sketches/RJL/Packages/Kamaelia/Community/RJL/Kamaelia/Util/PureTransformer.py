#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""\
=================
Pure Transformer component
=================

This component applies a function specified at its creation to messages
received (a filter). If the function returns None, no message is sent,
otherwise the result of the function is sent to "outbox".

Example Usage
-------------

To read in lines of text, convert to upper case and then write to the console.
pipeline(
    ConsoleReader(),
    PureTransformer(lambda x : x.upper()),
    ConsoleEchoer()
).run()
"""

from Axon.Component import component

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
