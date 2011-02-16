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
# Aim: Test Runner for all the Axon tests
#

# Test the module loads
import unittest
import test_AdaptiveCommsComponent
import test_Axon
import test_Component
import test_CoordinatingAssistantTracker
import test_Ipc
import test_Linkage
import test_Microprocess
import test_Postoffice
import test_Scheduler
import test_ThreadedComponent
import test___str__
import test_util

class VerboseTestResults(unittest.TestResult):
   def startTest(self,test):
      print(test)
      unittest.TestResult.startTest(self, test)

def suite():
   suite = unittest.TestSuite()
   suite.addTest(unittest.makeSuite(test_Scheduler.scheduler_Test))
   suite.addTest(unittest.makeSuite(test_AdaptiveCommsComponent.AdaptiveCommsComponent_Test))
   suite.addTest(unittest.makeSuite(test_Axon.Axon_Test))
   suite.addTest(unittest.makeSuite(test_Component.Component_Test))
   suite.addTest(unittest.makeSuite(test_Component.MessageDeliveryNotifications_Test))
   suite.addTest(unittest.makeSuite(test_CoordinatingAssistantTracker.CoordinatingAssistantTracker_Test))
   suite.addTest(unittest.makeSuite(test_Ipc.ipc_Test))
   suite.addTest(unittest.makeSuite(test_Linkage.linkage_Test))
   suite.addTest(unittest.makeSuite(test_Microprocess.MicroProcess_Test))
   suite.addTest(unittest.makeSuite(test_Postoffice.postoffice_Test))
   suite.addTest(unittest.makeSuite(test_Postoffice.linkagechaining_Test))
   suite.addTest(unittest.makeSuite(test_Postoffice.SizeLimitedBoxes_Test))
   suite.addTest(unittest.makeSuite(test_ThreadedComponent.threadedcomponent_Test))
   suite.addTest(unittest.makeSuite(test_ThreadedComponent.threadedadaptivecommscomponent_Test))
   suite.addTest(unittest.makeSuite(test___str__.str_Test))
   suite.addTest(unittest.makeSuite(test_util.util_Test))
   return suite

class FixedTestProgram(unittest.TestProgram):
      def createTests(self):
         self.test = suite()
   
#class AddNameToVerboseTextString(unittest._TextTestResult):
def startTest(self,test):
   unittest.TestResult.startTest(self, test)
   if self.showAll:
      self.stream.write(test.__class__.__name__ + ":")
      self.stream.write(self.getDescription(test))
      self.stream.write(" ... ")
         
if __name__=="__main__":
   ##~    res = unittest.TestResult()
   ##~    suite().run(res)
   ##~    print res
   ##~    for x in res.errors:
   ##~       print x[0].__class__.__name__
   ##~       print x[1]
   ##~    for x in res.failures:
   ##~       print x[0].__class__.__name__
   ##~       print x[1]

# This is really hacky and relies on the internals of unittest not changing.  Could easily turn into a steaming heap of poo.
# The commented out code above is far safer.
   unittest._TextTestResult.startTest=startTest
   FixedTestProgram(defaultTest="trick argument.  Causes createTests to be called which is overridden.")
