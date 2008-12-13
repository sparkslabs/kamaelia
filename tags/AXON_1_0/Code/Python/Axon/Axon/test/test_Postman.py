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
#
# Aim: Full coverage testing of the
#

# Test the module loads
import unittest
import re
import sys ; sys.path.append("..")
from Component import component
from Linkage import linkage
from Postman import *

class MockLinkage:
   def __init__(self, source="blah", sink="bling"):
      self.source = source
      self.sink = sink
   def dataToMove(self):
      return False
   def moveData(self):
      raise AxonException("This linkage never has data to move.  It is just a dummy.")
      
class named:
   def __init__(self):
      self.name = "Dummyname"
      
class AdvancedMockLinkage:
   def __init__(self):
      self.sink = named()
      self.sinkbox = "dummysink"
      self.source = named()
      self.sourcebox = "dummysource"
      self.showtransit = False
      self.moveDataCount = 0
   def dataToMove(self):
      return True
   def moveData(self):
      self.moveDataCount = 1+ self.moveDataCount
      
class AdvancedMockLinkage2(AdvancedMockLinkage):
   def dataToMove(self):
      return False

class postman_Test(unittest.TestCase):
    def setUp(self):
        "Creates some default objects to test with."
        self.pm = postman()
        self.pmname = postman("specialname")
        
        self.dummyc1name = "nameofcomponent1"
        self.dummyc2name = "nameofcomponent2"
        self.dummyc1 = "component1"
        self.dummyc2 = "component2"
        self.dummyc2 = "component2"
        self.dummyc3 = "component3"
        self.pmreg = postman()
        self.pmreg.register(self.dummyc1name, self.dummyc1)
        self.pmreg.register(self.dummyc2name, self.dummyc2)
        self.dummylink1=MockLinkage()
        self.dummylink2=MockLinkage(source = self.dummyc1)
        self.dummylink3=MockLinkage(sink = self.dummyc1)
        self.pmreg.registerlinkage(self.dummylink1)
        self.pmreg.registerlinkage(self.dummylink2)
        self.pmreg.registerlinkage(self.dummylink2)
        self.pmreg.registerlinkage(self.dummylink3)
        
    def test___init__SmokeTest_NoArguments(self):
        "__init__ - Called with no arguments.  This is the normal case."
        self.failUnless(self.pm.linkages==[] and self.pm.things=={} and self.pm.reversethings=={}, "postman not initialized properly.")
        self.failUnless(self.pm.debugname=="", "debugname is not an empty string.")
    
    def test___init__SmokeTest_withArgument(self):
        '__init__ - Called with a debugname which will be stored with ":debug " appended'
        self.failUnless(self.pmname.linkages==[] and self.pmname.things=={} and self.pmname.reversethings=={}, "postman not initialized properly.")
        self.failUnless(self.pmname.debugname=="specialname:debug ", "Debug name not set properly.")

    def strtest(self, postman):
        teststr = "{{ POSTMAN: " + postman.debugname + "links "+ str(postman.linkages) +"; things "+ str(postman.things) +"; " + microprocess.__str__(postman) + " }}"
        return (teststr == str(postman))
    
    def test__str__checksStringFormatStrict(self):
        '__str__ - Checks the formatted string is of the correct format.'
        self.failUnless(self.strtest(self.pm))
        self.failUnless(self.strtest(self.pmname))
        
    def test__register(self):
       'register - Registers a component with the postman.'
       comp = "bing"
       self.pm.register("blah", comp)
       self.failUnless(self.pm.things["blah"] is comp)
       self.failUnless(self.pm.reversethings[id(comp)]=="blah")
       
    def test_deregister_byname(self):
       'deregister - Deregisters a component from the postman by name'
       self.pmreg.deregister(name=str(self.dummyc1name))
     #  print self.pmreg.reversethings.__getitem__((id(self.dummyc1)))
       self.failUnlessRaises(KeyError, self.pmreg.things.__getitem__,(str(self.dummyc1name)))
       self.failUnlessRaises(KeyError, self.pmreg.reversethings.__getitem__,(id(self.dummyc1)))
       self.failUnless(self.pmreg.things[str(self.dummyc2name)] is self.dummyc2)
       self.failUnless(self.pmreg.reversethings[id(self.dummyc2)] == self.dummyc2name)
       self.failUnless(self.pmreg.linkages.count(self.dummylink1)==1)
       self.failUnless(self.pmreg.linkages.count(self.dummylink2)==0)
       self.failUnless(self.pmreg.linkages.count(self.dummylink3)==0)
    
    def test_deregister_bynameandcomponent(self):
       'deregister - Deregisters a component from the postman by name and component'
       self.pmreg.deregister(name=str(self.dummyc1name), component=self.dummyc1)
     #  print self.pmreg.reversethings.__getitem__((id(self.dummyc1)))
       self.failUnlessRaises(KeyError, self.pmreg.things.__getitem__,(str(self.dummyc1name)))
       self.failUnlessRaises(KeyError, self.pmreg.reversethings.__getitem__,(id(self.dummyc1)))
       self.failUnless(self.pmreg.things[str(self.dummyc2name)] is self.dummyc2)
       self.failUnless(self.pmreg.reversethings[id(self.dummyc2)] == self.dummyc2name)
       self.failUnless(self.pmreg.linkages.count(self.dummylink1)==1)
       self.failUnless(self.pmreg.linkages.count(self.dummylink2)==0)
       self.failUnless(self.pmreg.linkages.count(self.dummylink3)==0)
       
    def test_deregister_bynameandcomponenterror(self):
       'deregister - Deregisters a component from the postman by name'
       self.failUnlessRaises(AxonException, self.pmreg.deregister,name=str(self.dummyc1name), component=self.dummyc2)
     #  print self.pmreg.reversethings.__getitem__((id(self.dummyc1)))
       self.failUnless(self.pmreg.things[str(self.dummyc1name)] is self.dummyc1)
       self.failUnless(self.pmreg.reversethings[id(self.dummyc1)] == self.dummyc1name)
       self.failUnless(self.pmreg.things[str(self.dummyc2name)] is self.dummyc2)
       self.failUnless(self.pmreg.reversethings[id(self.dummyc2)] == self.dummyc2name)
       self.failUnless(self.pmreg.linkages.count(self.dummylink1)==1)
       self.failUnless(self.pmreg.linkages.count(self.dummylink2)==2)
       self.failUnless(self.pmreg.linkages.count(self.dummylink3)==1)
       
    def test_deregister_bycomponent(self):
       'deregister - Deregisters a component from the postman by name'
       self.pmreg.deregister(component=self.dummyc1)
     #  print self.pmreg.reversethings.__getitem__((id(self.dummyc1)))
       self.failUnlessRaises(KeyError, self.pmreg.things.__getitem__,(str(self.dummyc1name)))
       self.failUnlessRaises(KeyError, self.pmreg.reversethings.__getitem__,(id(self.dummyc1)))
       self.failUnless(self.pmreg.things[str(self.dummyc2name)] is self.dummyc2)
       self.failUnless(self.pmreg.reversethings[id(self.dummyc2)] == self.dummyc2name)
       self.failUnless(self.pmreg.linkages.count(self.dummylink1)==1)
       self.failUnless(self.pmreg.linkages.count(self.dummylink2)==0)
       self.failUnless(self.pmreg.linkages.count(self.dummylink3)==0)
       
    def test_deregister_noarg(self):
       'deregister - Deregisters a component from the postman by name'
       self.failUnlessRaises(AxonException, self.pmreg.deregister)
     #  print self.pmreg.reversethings.__getitem__((id(self.dummyc1)))
       self.failUnless(self.pmreg.things[str(self.dummyc1name)] is self.dummyc1)
       self.failUnless(self.pmreg.reversethings[id(self.dummyc1)] == self.dummyc1name)
       self.failUnless(self.pmreg.things[str(self.dummyc2name)] is self.dummyc2)
       self.failUnless(self.pmreg.reversethings[id(self.dummyc2)] == self.dummyc2name)
       self.failUnless(self.pmreg.linkages.count(self.dummylink1)==1)
       self.failUnless(self.pmreg.linkages.count(self.dummylink2)==2)
       self.failUnless(self.pmreg.linkages.count(self.dummylink3)==1)
       
    def test_deregister_bynamenotpresent(self):
       'deregister - Deregisters a component from the postman by name'
       self.failUnlessRaises(KeyError, self.pmreg.deregister, name="blah")
     #  print self.pmreg.reversethings.__getitem__((id(self.dummyc1)))
       self.failUnless(self.pmreg.things[str(self.dummyc1name)] is self.dummyc1)
       self.failUnless(self.pmreg.reversethings[id(self.dummyc1)] == self.dummyc1name)
       self.failUnless(self.pmreg.things[str(self.dummyc2name)] is self.dummyc2)
       self.failUnless(self.pmreg.reversethings[id(self.dummyc2)] == self.dummyc2name)
       self.failUnless(self.pmreg.linkages.count(self.dummylink1)==1)
       self.failUnless(self.pmreg.linkages.count(self.dummylink2)==2)
       self.failUnless(self.pmreg.linkages.count(self.dummylink3)==1)
       
    def test_deregister_bycomponentnotpresent(self):
       'deregister - Deregisters a component from the postman by name'
       self.failUnlessRaises(KeyError, self.pmreg.deregister,component=self.dummyc3)
     #  print self.pmreg.reversethings.__getitem__((id(self.dummyc1)))
       self.failUnless(self.pmreg.things[str(self.dummyc1name)] is self.dummyc1)
       self.failUnless(self.pmreg.reversethings[id(self.dummyc1)] == self.dummyc1name)
       self.failUnless(self.pmreg.things[str(self.dummyc2name)] is self.dummyc2)
       self.failUnless(self.pmreg.reversethings[id(self.dummyc2)] == self.dummyc2name)
       self.failUnless(self.pmreg.linkages.count(self.dummylink1)==1)
       self.failUnless(self.pmreg.linkages.count(self.dummylink2)==2)
       self.failUnless(self.pmreg.linkages.count(self.dummylink3)==1)
       
    def test_registerlinkage(self):
       'registerlinkage - Registers a linkage with the Postman'
       dummylinkage = "linkage"
       dummylinkage2 = "linkage2"
       self.pm.registerlinkage(dummylinkage)
       self.pm.registerlinkage(dummylinkage2)
       self.failUnless(self.pm.islinkageregistered(dummylinkage))
       self.failUnless(self.pm.islinkageregistered(dummylinkage2))
       
    def test_deregisterlinkage_component(self):
       'Tests the deregistration of linkages by component'
       self.pmreg.deregisterlinkage(thecomponent=self.dummyc1)
       self.failUnless(self.pmreg.linkages.count(self.dummylink1)==1)
       self.failUnless(self.pmreg.linkages.count(self.dummylink2)==0)
       self.failUnless(self.pmreg.linkages.count(self.dummylink3)==0)
    
    def test_deregisterlinkage_linkage(self):
       'Tests the deregistration of a specific linkage'
       self.pmreg.deregisterlinkage(thelinkage=self.dummylink2)
       self.failUnless(self.pmreg.linkages.count(self.dummylink1)==1)
       self.failUnless(self.pmreg.linkages.count(self.dummylink2)==0)
       self.failUnless(self.pmreg.linkages.count(self.dummylink3)==1)
    
    def test_deregisterlinkage_badargs(self):
       'Tests the deregistration of a specific linkage'
       self.failUnlessRaises(AxonException, self.pmreg.deregisterlinkage,thecomponent=self.dummyc1, thelinkage=self.dummylink2 )
       self.failUnlessRaises(AxonException, self.pmreg.deregisterlinkage)
       self.failUnless(self.pmreg.linkages.count(self.dummylink1)==1)
       self.failUnless(self.pmreg.linkages.count(self.dummylink2)==2)
       self.failUnless(self.pmreg.linkages.count(self.dummylink3)==1)
       
    def test_deregisterlinkage_synchronouslinkagedeadlock(self):
       'deregisterlinkage - Tests for a deadlock when a postman deregisters a linkage whose sink is limited in size and full'
       posty = postman()
       comp1 = component()
       comp2=component()
       link = linkage(source=comp1, sink=comp2, synchronous = 1)
       comp1.send("ba")
       link.moveData()
       comp1.send("da")
       link.moveData()
       posty.registerlinkage(thelinkage=link)
       posty.deregisterlinkage(thelinkage=link)
#       self.fail("Uncomment deregisterlinkage to run the test.  Failure == infinite loop.") # remove this line when above is uncommented

    def test_deregisterlinkage_synchronouslinkagedeadlockcomponent(self):
       'deregisterlinkage - Tests for a deadlock when a postman deregisters linkages of a component whose sink is limited in size and full'
       posty = postman()
       comp1 = component()
       comp2=component()
       link = linkage(source=comp1, sink=comp2, synchronous = 1)
       comp1.send("ba")
       link.moveData()
       comp1.send("da")
       link.moveData()
       posty.registerlinkage(thelinkage=link)
       posty.deregisterlinkage(thecomponent=comp1)
#       self.fail("Uncomment deregisterlinkage to run the test. Failure == infinite loop") # remove this line when above is uncommented
       
    def test_domessagedelivery_mockobjects(self):
       'domessagedelivery - Checks that linkages with data to move have moveData called.  See the AdvancedMockLinkage classes for details.'
       L1 = AdvancedMockLinkage()
       L2 = AdvancedMockLinkage2()
       self.pm.registerlinkage(L1)
       self.pm.registerlinkage(L2)
       self.pm.domessagedelivery()
       self.pm.domessagedelivery()
       self.failUnless(L1.moveDataCount == 2)
       self.failUnless(L2.moveDataCount == 0)
       
    def test_domessagedelivery_nolinks(self):
       'domessagedelivery - Tests for stability when there are no linkages registered.'
       # This test was written before removing special case that appeared unnecessary.
       self.pm.domessagedelivery()
       self.pm.domessagedelivery()

if __name__=='__main__':
    unittest.main()
