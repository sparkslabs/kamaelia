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
# Full coverage testing of the Coordinating Assistant Tracker
#

# Test the module loads
import unittest
from Axon.CoordinatingAssistantTracker import *
from Axon.Component import component
from Axon.AxonExceptions import *

class dummyComponent(component): pass

class CoordinatingAssistantTracker_Test(unittest.TestCase):
   def test_SmokeTest_NoArguments(self):
      "__init__ - Called with no arguments should succeed. "
      cat = coordinatingassistanttracker()
      self.assert_(cat is not None)
      self.assertEqual(cat.servicesRegistered(), [], "Initially the tracker is tracking no services")
      self.assertEqual(cat.informationItemsLogged(), [], "Initially no specific information is being tracked")
      self.assert_(cat._parent is None)
#      try:
#         self.assertEqual("<class 'CoordinatingAssistantTracker.coordinatingassistanttracker'>_5",cat.name,"Cat's name follows standard naming pattern")
#      except:
#         print cat.name
#         raise

   def test_SmokeTest_SingleParent(self):
      "__init__ - Called with a single argument results in it being the parent for the tracker"
      parentcat = coordinatingassistanttracker()
      cat = coordinatingassistanttracker(parentcat)
      self.assertEqual(cat._parent, parentcat, "Parent tracker supplied is being tracked")

   def test_SmokeTest_InvalidSingleParent(self):
      "__init__ - Trying to set a anything other than a coordinated assistant tracker as the parent causes a BadParentTracker exception"
      self.assertRaises(BadParentTracker, coordinatingassistanttracker, "foobar")

   def test_registerService_Add(self):
      "registerService - adds the named component/inbox to the list of named registered services"
      cat = coordinatingassistanttracker()
      aComponent = dummyComponent()
      cat.registerService("someservice", aComponent, "control")
      self.assertEqual(cat.servicesRegistered(),["someservice"])

   def test_registerService_AddExisting(self):
      "registerService - adding a duplicate service fails, even with same arguments"
      cat = coordinatingassistanttracker()
      aComponent = dummyComponent()
      cat.registerService("someservice", aComponent, "control")
      self.assertRaises(ServiceAlreadyExists,cat.registerService,"someservice", aComponent, "control")

   def test_registerService_BadComponent(self):
      "registerService - adding a service but not to as a component fails- raises BadComponent assertion"
      cat = coordinatingassistanttracker()
      aComponent = "dummycomponent"
      self.assertRaises(BadComponent,cat.registerService,"someservice", aComponent, "control")

   def test_registerService_BadInbox(self):
      "registerService - adding a service but to a bad/nonexistant inbox fails - raises BadInbox assertion"
      cat = coordinatingassistanttracker()
      aComponent = dummyComponent()
      self.assertRaises(BadInbox,cat.registerService,"someservice", aComponent, "badinbox")

   def test_retrieveService_basic(self):
      "retrieveService - Retrieving a tracked service should return the component/inbox pair we supplied under a specific name"
      cat = coordinatingassistanttracker()
      aComponent = dummyComponent()
      serviceInbox = "control"
      cat.registerService("someservice", aComponent, serviceInbox)
      (theComponent,theInbox)=cat.retrieveService("someservice")
      self.assertEqual(theComponent, aComponent, "The component we get back should match the service we registered in the first place")
      self.assertEqual(theInbox, serviceInbox, "The inbox we get back should match the service we registered in the first place")

   def test_retrieveService_nonexistantservice(self):
      "retrieveService - Attempting to retrieve a non-tracked service results in KeyError exception being thrown"
      cat = coordinatingassistanttracker()
      self.assertRaises(KeyError, cat.retrieveService,"someservice")

   def test_deRegisterService(self):
      "deRegisterService - allows a component to remove their service from being public"
      cat = coordinatingassistanttracker()
      aComponent = dummyComponent()
      cat.registerService("someservice", aComponent, "control")
      # We know that this is registered now. If we now delete it should be gone.
      cat.deRegisterService("someservice")
      self.assertEqual(cat.servicesRegistered(),[])

   def test_deRegisterService_nonExistantService(self):
      "deRegisterService - deleting a non-existant service raises MultipleServiceDeletion exception"
      cat = coordinatingassistanttracker()
      self.assertRaises(MultipleServiceDeletion, cat.deRegisterService,"someservice")

   def test_trackValue_basic(self):
      "trackValue - Adds the name/value pair to the set of info items logged"
      cat = coordinatingassistanttracker()
      cat.trackValue("stats.pages.hitcount", 5)
      self.assertEqual(cat.informationItemsLogged(), ["stats.pages.hitcount"], "The information to be tracked was added")

   def test_trackValue_addTwice(self):
      "trackValue - Adding a value to be tracked twice raises NamespaceClash"
      cat = coordinatingassistanttracker()
      cat.trackValue("stats.pages.hitcount", 5)
      self.assertRaises(NamespaceClash, cat.trackValue,"stats.pages.hitcount", 6)

   def test_retrieveValue_basic(self):
      "retrieveValue - Retrieving a tracked value should return the value we asked to be tracked"
      cat = coordinatingassistanttracker()
      cat.trackValue("stats.pages.hitcount", 5)
      self.assertEqual(5, cat.retrieveValue("stats.pages.hitcount"))

   def test_retrieveValue_notStored(self):
      "retrieveValue - attempting to retrieve a value we're not tracking should raise AccessToUndeclaredTrackedVariable"
      cat = coordinatingassistanttracker()
      self.assertRaises(AccessToUndeclaredTrackedVariable,cat.retrieveValue,"stats.pages.hitcount")

   def test_updateValue_basic(self):
      "updateValue - Updating a value should result in the value stored being updated"
      cat = coordinatingassistanttracker()
      cat.trackValue("stats.pages.hitcount", 5)
      cat.updateValue("stats.pages.hitcount", 10)
      self.assertEqual(10, cat.retrieveValue("stats.pages.hitcount"))

   def test_updateValue_undeclaredTrackedVariable(self):
      "updateValue - Updating a value not declared as tracked should raise AccessToUndeclaredTrackedVariable"
      cat = coordinatingassistanttracker()
      self.assertRaises(AccessToUndeclaredTrackedVariable, cat.updateValue,"stats.pages.hitcount", 10)

   def test_informationItemsLogged(self):
      "informationItemsLogged - returns the names of pieces of information logged with this tracker"
      cat = coordinatingassistanttracker()
      cat.trackValue("stats.pages.hitcount", 5)
      cat.trackValue("stats.pages.pagecount", 6)
      cat.trackValue("stats.foobar.count", 7)
      items = cat.informationItemsLogged()
      items.sort()
      self.assertEqual(['stats.foobar.count', 'stats.pages.hitcount', 'stats.pages.pagecount'],items,"The 3 items were added correctly")

if __name__=="__main__":
   unittest.main()

