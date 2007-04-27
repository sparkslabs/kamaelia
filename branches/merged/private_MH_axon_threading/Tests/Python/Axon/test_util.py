#!/usr/bin/python
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
#
# Aim: Full coverage testing of the util module
#

# Test the module loads
import unittest
from Axon.util import *
from Axon.Component import component
from Axon.AxonExceptions import AxonException, normalShutdown

class util_Test(unittest.TestCase):
   def test_logError(self):
       "logError - At the moment this function does nothing but can be rewritten to log ignored exception data.  Equally the test does nothing."
       pass
   def test_production(self):
        """production - is a module value that turns off some exception to make the system tolerant of failure when running in production.
        For development and testing it should be False to allow uncaught exceptions to bring down the system."""
        self.failIf(production, "production set true.  This is inappropriate for development, testing and debugging as exceptions will be hidden.  This should only be true when fully developed and tested although tests should be run again in this mode and this test should fail!")
   def test_axonRaise(self):
        """axonRaise - behaviour depends on the value of production.  If true it will simply return False.  Otherwise it will throw an
        exception of the type passed to it with the other arguments passed to the constructor."""
        if production:
            self.failIf(axonRaise(AxonException,"a","b"), "If production axonRaise should return False.")
            self.failIf(axonRaise(normalShutdown, "a", "b","c"),"If production axonRaise should return False.")
        else:
            self.failUnlessRaises(AxonException, axonRaise, AxonException, "a", "b")
            self.failUnlessRaises(normalShutdown, axonRaise, normalShutdown, "a","b","c")
            try:
                axonRaise(AxonException, "a","b")
            except Exception, e:
                self.failUnless(isinstance(e, AxonException), "Unexpected exception type.")
                self.failUnless(e.args==("a","b"), "Extra args not passed to exception.")
            try:
                axonRaise(normalShutdown, "a","b","c")
            except Exception, e:
                self.failUnless(isinstance(e, normalShutdown), "Unexpected exception type.")
                self.failUnless(e.args==("a","b","c"), "Extra args not passed to exception.")
            
   def test_removeAll(self):
      "removeAll - (xs:list,y) - removes all occurances of y from the list xs."
      L=[]
      removeAll(L,"blah")
      self.failUnless(L==[])
      L=["blah","blah","blah"]
      removeAll(L, "blah")
      self.failUnless(L==[])
      L=["ba","blah","da","blah","bing","blah","!","!"]
      removeAll(L ,"blah")
      self.failUnless(L==["ba","da","bing","!","!"])
   def test_listSubset(self):
      "listSubset - returns true if the first list argument is a subset of the second list argument."
      self.failUnless(listSubset([],[]))
      self.failIf(listSubset(["a"],[]))
      self.failUnless(listSubset(["b","a"],["a","b"]))
      self.failUnless(listSubset(["a","b"],["A","Z","G","b","H","a","fred"]))
      self.failIf(listSubset(["a","b","c"],["A","Z","G","b","H","a","fred"]))
   def test_testInterface_smokeSuccess(self):
      "testInterface - returns true for a _minimal match_ on the interface of the component."
      # Test assumes component defaults to having inboxes: "inbox" and "control" and "outboxes": "outbox" and "signal"
      self.failUnless(testInterface(component(), (["inbox","control"],["outbox","signal"])), "Failed with all boxes required.")
      self.failUnless(testInterface(component(), ([],[])), "Failed with no boxes required.")
      self.failUnless(testInterface(component(), (["inbox"],[])), "Failed with no boxes required.")
      self.failUnless(testInterface(component(), ([],["outbox"])), "Failed with no boxes required.")
      
   def test_testInterface_failmodes(self):
      "In production mode failed tests will return false.  Otherwise they will throw an exception that is likely to stop the system."
      if production:
          self.failIf(testInterface(component(), (["fred"],[])), "Does not return false for failed test.")
          self.failIf(testInterface(component(), (["inbox","control","fred"],["outbox","signal"])), "Does not return false for failed test.")
          self.failIf(testInterface(component(), ([],["fred"])), "Does not return false for failed test.")
          self.failIf(testInterface(component(), (["inbox","control"],["outbox","signal","fred"])), "Does not return false for failed test.")
      else:
          self.failUnlessRaises(invalidComponentInterface, testInterface, component(), (["fred"],[]))
          self.failUnlessRaises(invalidComponentInterface, testInterface, component(), ([],["fred"]))
          self.failUnlessRaises(invalidComponentInterface, testInterface, component(), (["inbox","control","fred"],[]))
          self.failUnlessRaises(invalidComponentInterface, testInterface, component(), (["inbox","control"],["outbox","signal","fred"]))
          c = component()
          exceptioncount=0
          try:
              testInterface(c,(["fred"],[]))
          except Exception, e:
              self.failUnless(isinstance(e, invalidComponentInterface))
              self.failUnless(e.args == ("inboxes", c, (["fred"],[])), "Exception not as expected.")
              exceptioncount=exceptioncount+1
          try:
              testInterface(c,([],["fred"]))
          except Exception, e:
              self.failUnless(isinstance(e, invalidComponentInterface))
              self.failUnless(e.args == ("outboxes", c, ([],["fred"])), "Exception not as expected.")
              exceptioncount=exceptioncount+1
          try:
              testInterface(c,(["inbox","control","fred"],[]))
          except Exception, e:
              self.failUnless(isinstance(e, invalidComponentInterface))
              self.failUnless(e.args == ("inboxes", c, (["inbox","control","fred"],[])), "Exception not as expected.")
              exceptioncount=exceptioncount+1
          try:
              testInterface(c,(["inbox","control"],["outbox","signal","fred"]))
          except Exception, e:
              self.failUnless(isinstance(e, invalidComponentInterface))
              self.failUnless(e.args == ("outboxes", c, (["inbox","control"],["outbox","signal","fred"])), "Exception not as expected.")
              exceptioncount=exceptioncount+1
          self.failUnless(exceptioncount == 4, "Expected exception wasn't thrown!!!")

   def test_safeList_correct(self):
      "safeList - always returns a list even if the arg for constructing the list would normally cause a typeerror."
      self.failUnless(safeList(())==[], "Can't create empty list from empty tuple.")
      self.failUnless(safeList((1,))==[1], "Can't create list from 1 item tuple.")
      self.failUnless(safeList((1,2,3))==[1,2,3], "Can't create list from multiple item tuple.")
   def test_safeList_empty(self):
      "safeList - Like list it returns an empty list when called without an argument."
      self.failUnless(safeList()==[], "Fails when called with no argument.")
      
   def test_safeList_error(self):
      "safeList - returns an empty list if the argument would cause a TypeError if passed to list().  That is anything without an iterator method."
      self.failUnless(safeList(1)==[])

   def test_Finality(self):
      "Finality - dummy class deriving from Exception - used for implementing try...finally in a generator."
      self.failUnless(isinstance(Finality(),Exception))
if __name__=='__main__':
   unittest.main()
