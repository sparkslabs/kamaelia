#!/usr/bin/env python2.3
#
# Aim: Test Runner for all the Axon tests
#

# Test the module loads
import unittest
import test_AdaptiveCommsComponent
import test_Axon
import test_Component
import test_CoordinatingAssistantTracker
#import test_debugConfigFile
#import test_debug
#import test_idGen
import test_Ipc
import test_Linkage
import test_Microprocess
import test_Postman
import test_Scheduler
import test___str__
import test_util

class VerboseTestResults(unittest.TestResult):
   def startTest(self,test):
      print test
      unittest.TestResult.startTest(self, test)

def suite():
   suite = unittest.TestSuite()
   suite.addTest(unittest.makeSuite(test_Scheduler.Scheduler_Test))
   suite.addTest(unittest.makeSuite(test_AdaptiveCommsComponent.AdaptiveCommsComponent_Test))
   suite.addTest(unittest.makeSuite(test_Axon.Axon_Test))
   suite.addTest(unittest.makeSuite(test_Component.Component_Test))
   suite.addTest(unittest.makeSuite(test_CoordinatingAssistantTracker.CoordinatingAssistantTracker_Test))
   suite.addTest(unittest.makeSuite(test_Ipc.ipc_Test))
   suite.addTest(unittest.makeSuite(test_Linkage.linkage_Test))
   suite.addTest(unittest.makeSuite(test_Microprocess.MicroProcess_Test))
   suite.addTest(unittest.makeSuite(test_Postman.postman_Test))
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
