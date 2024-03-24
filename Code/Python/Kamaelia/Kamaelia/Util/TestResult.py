#!/usr/bin/python
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
                raise AssertionError("false value message received by: %s" % self)
        if self.dataReady("control"):
            mes = self.recv("control")
            if isinstance(mes, StopSystem):
                raise StopSystemException("StopSystem request raised from TestResult")
        return 1
    
__kamaelia_components__  = ( TestResult, )
