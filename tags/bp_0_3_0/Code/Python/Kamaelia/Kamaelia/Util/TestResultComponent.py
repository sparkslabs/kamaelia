#!/usr/bin/env python2.3
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess,ipc
from Axon.AxonExceptions import AxonException

class StopSystem(ipc):
    "This IPC message is the command to the component to throw a StopSystemException and bring the Axon system to a halt."
    pass
    
class StopSystemException(AxonException):
    "This exception is used to stop the whole Axon system."
    pass

class testResultComponent(component):
    """DO NOT USE IN LIVE SYSTEMS.  This class is largely intended for use is
    system testing and particularly unit testing of other components.  In the
    case of error or request it is intended to throw an exception stop the Axon
    system and jump back to the unit test."""
    Outboxes = []
    def mainBody(self):
        if self.dataReady():
            if not self.recv():
                raise AssertionError, "false value message received by: %s" % self
        if self.dataReady("control"):
            mes = self.recv("control")
            if isinstance(mes, StopSystem):
                raise StopSystemException("StopSystem request raised from TestResultComponent")
        return 1
    
