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
"""\
================================
Sequential Transformer component
================================

This component applies all the functions supplied to incoming messages.
If the output from the final function is None, no message is sent.



Example Usage
-------------

To read in lines of text, convert to upper case, prepend "foo", and append "bar!"
and then write to the console::

    Pipeline(
        ConsoleReader(eol=""),
        SequentialTransformer( str,
                               str.upper,
                               lambda x : "foo" + x,
                               lambda x : x + "bar!",
                             ),
        ConsoleEchoer(),
    ).run()

"""

from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess,shutdown

class SequentialTransformer(component):
    def __init__(self, *functions):
        super(SequentialTransformer, self).__init__()

        if len(functions)>0:
            self.processMessage = self.pipeline
            self.functions = functions
        
    def processMessage(self, msg):
        pass

    def pipeline(self,msg):
        for function in self.functions:
            msg = function(msg)
        return msg
        
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

__kamaelia_components__  = ( SequentialTransformer, )

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

    # Example - prepend "foo" and append "bar" to lines entered.
    Pipeline(
        ConsoleReader(eol=""),
        SequentialTransformer(
                str,
                str.upper,
                lambda x : "foo" + x,
                lambda x : x + "bar!\n"
                ),
        ConsoleEchoer()
    ).run()
