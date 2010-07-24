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
#
# Aim: Full coverage testing of the Ipc classes
#

# Test the module loads
import unittest
from Axon.Ipc import *

class ipc_Test(unittest.TestCase):
    def test_SmokeTest(self):
        "ipc - Should be derived from object."
        self.failUnless(isinstance(ipc(),object), "IPC objects should also be instances of object.")

class newComponent_Test(unittest.TestCase):
   def test___init__SmokeTest_NoArguments(self):
      "newComponent.__init__ - Should work without problems."
      nc=newComponent()
      self.failUnless(isinstance(nc, ipc), "newComponent should be derived from ipc class")
      self.failUnless(len(nc.components())==0, "There should be no components in the message if the constructor was called with no arguments.")
   def test___init__SmokeTest(self):
      "newComponent.__init__ - Groups all the arguments as a tuple of components that need to be activated/added to the run queue. Order is unimportant, scheduler doesn't care."
      nc=newComponent("ba","da","bing")
      self.failUnless(nc.components()==("ba","da","bing"), "Component tuple is not as expected.")
   def test_components(self):
      "newComponent.components - Returns a tuple of components that need to be added to the run queue/activated. Same test as for __init__ as they are counterparts."
      nc=newComponent("ba","da","bing")
      self.failUnless(nc.components()==("ba","da","bing"), "components returned something other than expected.")

class shutdownMicroprocess_Test(unittest.TestCase):
   def test___init__SmokeTest_NoArguments(self):
      "shutdownMicroprocess.__init__ - Should work without problems."
      sm=shutdownMicroprocess()
      self.failUnless(isinstance(sm,ipc), "shutdownMicroprocess should be derived from ipc")
      self.failUnless(sm.microprocesses()==(), "Microprocess tuple not empty as expected.")
   def test___init__SmokeTest(self):
      "shutdownMicroprocess.__init__ - Treats all the arguments as a tuple of microprocesses that need to be shutdown."
      sm=shutdownMicroprocess("ba","da","bing")
      self.failUnless(sm.microprocesses()==("ba","da","bing"), "Stored tuple not as expected.")
   def test_microprocesses(self):
      "shutdownMicroprocess.microprocesses- Returns the list of microprocesses that need to be shutdown. This is essentially the counterpart to the __init__ test."
      sm=shutdownMicroprocess("ba","da","bing")
      self.failUnless(sm.microprocesses()==("ba","da","bing"), "Returned tuple not as expected.")

class notify_Test(unittest.TestCase):
   def test_SmokeTest_NoArguments(self):
      "notify.__init__ - Called without arguments fails."
      self.failUnlessRaises(TypeError, notify)
   def test_SmokeTest_MinArguments(self):
      "notify.__init__ - Creates a message from a specific caller with some data payload to notify part of the system of an event."
      n=notify("caller", "payload")
      self.failUnless(isinstance(n, ipc), "Expected notify to be an instance of ipc.")
      self.failUnless(n.object == "payload", "Payload argument not stored in object member.")
      self.failUnless(n.caller == "caller", "Caller argument not stored in caller member.")

class status_Test(unittest.TestCase):
   def test_SmokeTest_NoArguments(self):
      "status.__init__ - Called without arguments fails."
      self.failUnlessRaises(TypeError, status)
   def test_SmokeTest_MinArguments(self):
      "status.__init__ - Stores the status message - for extraction by the recipient of the message.  Checks object is instance of ipc."
      s=status("Status message.")
      self.failUnless(isinstance(s, ipc), "status should be derived from ipc.")
      self.failUnless(s.status() == "Status message.", "Status message not stored properly.")
   def test_status(self):
      "status.status - Returns the status message stored inside the status object.  Counterpart to __init__ test."
      s=status("Status message.")
      self.failUnless(s.status() == "Status message.", "Status message not stored properly.")

class wouldblock_Test(unittest.TestCase):
   def test_SmokeTest_NoArguments(self):
      "wouldblock.__init__ - Called without arguments fails."
      self.failUnlessRaises(TypeError, wouldblock)
   def test_SmokeTest_MinArguments(self):
      "wouldblock.__init__ - Stores the caller in the wouldblock message. Allows the scheduler to make a decision.  Checks wouldblock is a subclass of ipc."
      wb=wouldblock(self)
      self.failUnless(isinstance(wb, ipc), "wouldblock should be derived from ipc")
      self.failUnless(wb.caller == self, "caller not properly set by __init__.")

class producerFinished_Test(unittest.TestCase):
   def test_SmokeTest_NoArguments(self):
      "producerFinished.__init__ - Called without arguments defaults to a caller of None, message of None.  Checks producerFinished is a subclass of ipc"
      pf=producerFinished()
      self.failUnless(isinstance(pf, ipc), "producerFinished should be an derived from ipc.")
      self.failUnless(pf.caller== None,  "caller does not default to None")
      self.failUnless(pf.message == None, "message does not default to None")
   def test_SmokeTest_MinArguments(self):
      "test_SmokeTest.__init__ - Creates a producerFinished message with specified caller & shutdown 'last' message."
      pf = producerFinished("caller", "message")
      self.failUnless(pf.caller == "caller", "caller not set correctly by position.")
      self.failUnless(pf.message == "message", "message not set correctly by position.")
      
      pf2 = producerFinished(message="message", caller="caller")
      self.failUnless(pf2.caller == "caller", "caller not set correctly by name.")
      self.failUnless(pf2.message == "message", "message not set correctly by name.")

class errorInformation_Test(unittest.TestCase):
   def test_SmokeTest_NoArguments(self):
      "errorInformation.__init__ - Called without arguments fails - must include caller."
      self.failUnlessRaises(TypeError, errorInformation)
   def test_SmokeTest_MinArguments(self):
      "errorInformation.__init__ - Takes the supplied caller, and creates an errorInformation object. Checks errorInformation object is an instance of ipc."
      ei=errorInformation(self)
      self.failUnless(isinstance(ei, ipc), "errorInformation should be derived from ipc.")
      self.failUnless(ei.caller == self, "Caller is not set properly.")
   def test_SmokeTest_MinSensibleArguments(self):
      "errorInformation.__init__ - An exception & message (any object) in addition to the caller to provide a more meaningful errorInformation message where appropriate. ttbw "
      ei=errorInformation("caller", "exception", "message")
      self.failUnless(ei.caller == "caller", "Caller is not set properly by position.")
      self.failUnless(ei.message == "message", "Caller is not set properly by position.")
      self.failUnless(ei.exception == "exception", "Caller is not set properly by position.")

      ei=errorInformation(exception="exception", message="message", caller = "caller")
      self.failUnless(ei.caller == "caller", "Caller is not set properly by name.")
      self.failUnless(ei.message == "message", "Caller is not set properly by name.")
      self.failUnless(ei.exception == "exception", "Caller is not set properly by name.")
      
if __name__=='__main__':
   unittest.main()
