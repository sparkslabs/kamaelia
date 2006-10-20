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
"""\
===================
Basic Result Tester
===================

A simple component for testing that a stream of data tests true.
This is NOT intended for live systems, but for testing and development purposes
only.



Example Usage
-------------
::
    Pipeline( source(), TestResult() ).activate()
    
Raises an assertion error if source() generates a value that doesn't test
true.



How does it work?
-----------------

If the component receives a value on its "inbox" inbox that does not test true,
then an AssertionError is raised.

If the component receives a StopSystem message on its "control" inbox then a
StopSystemException message is raised as an exception.

This component does not terminate (unless it throws an exception).

It does not pass on the data it receives.
"""


from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess,ipc
from Axon.AxonExceptions import AxonException

class StopSystem(ipc):
    """\
    This IPC message is the command to the component to throw a 
    StopSystemException and bring the Axon system to a halt.
    """
    pass

    
class StopSystemException(AxonException):
    """This exception is used to stop the whole Axon system."""
    pass


class TestResult(component):
    """\
    TestResult() -> new TestResult.
    
    Component that raises an AssertionError if it receives data on its "inbox"
    inbox that does not test true. Or raises a StopSystemException if a
    StopSystem message is received on its "control" inbox.
    """

    Inboxes = { "inbox"   : "Data to test",
                "control" : "StopSystemException messages",
              }
    Outboxes = { "outbox" : "NOT USED",
                 "signal" : "NOT USED",
               }

    def mainBody(self):
        if self.dataReady():
            if not self.recv():
                raise AssertionError, "false value message received by: %s" % self
        if self.dataReady("control"):
            mes = self.recv("control")
            if isinstance(mes, StopSystem):
                raise StopSystemException("StopSystem request raised from TestResult")
        return 1
    
__kamaelia_components__  = ( TestResult, )
