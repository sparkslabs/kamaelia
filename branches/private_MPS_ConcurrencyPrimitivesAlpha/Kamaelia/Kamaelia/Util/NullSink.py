#!/usr/bin/env python
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""
===================
Null Sink Component
===================

NullSinkComponent has the same role in a Kamaelia system as /dev/null. The
older nullSinkComponent has the same role, but that capitalisation is
deprecated. It is relatively rarely needed, but really useful when needed.

Example Usage
-------------

To ignore everything read from a file::

    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
    from Kamaelia.Util.Console import ConsoleEchoer

    Pipeline(
        ReadFileAdaptor("/etc/fstab"),
        NullSinkComponent(),
        ConsoleEchoer()
    ).run()


"""
from Axon.Component import component, scheduler
from Axon.Ipc import producerFinished, shutdownMicroprocess

class nullSinkComponent(component):
    def shutdown(self):
        if self.dataReady("control"):
            data = self.recv("control")
            if isinstance(data,producerFinished) or isinstance(data, shutdownMicroprocess):
                self.send(data, "signal")
                return True
        return False
       
    def main(self):
        # FIXME: This component is best changed to have NullSink inboxes, whether linked to or not.
        while not self.shutdown():
            for _ in self.Inbox("inbox"):
                pass # Throw away
            while not self.anyReady():
                self.pause()
                yield 1
            yield 1
      
NullSinkComponent = nullSinkComponent # FIXME, in future deprecate the badly named class

__kamaelia_components__  = ( nullSinkComponent, NullSinkComponent)

if __name__ =="__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
    from Kamaelia.Util.Console import ConsoleEchoer

    Pipeline(
        ReadFileAdaptor("/etc/fstab"),
        NullSinkComponent(),
        ConsoleEchoer()
    ).run()