#!/usr/bin/env python
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
# Full coverage testing of the Adaptive Comms Component
#

# Test the module loads
import unittest
import Axon.AdaptiveCommsComponent as AdaptiveCommsComponent
import Axon.Component as Component

class AdaptiveCommsComponent_Test(unittest.TestCase):
   def test_SmokeTest_NoArguments(self):
      "__init__ - Called with no arguments is expected, results in component superconstructor being called. performs no local initialisation"
      a=AdaptiveCommsComponent.AdaptiveCommsComponent()
      self.assert_( isinstance(a,AdaptiveCommsComponent.AdaptiveCommsComponent), "Right Type")
      self.assert_( isinstance(a,Component.component), "Right Base Type")
      self.assert_( 0==len(a.inboxes['control']) and 0==len(a.inboxes['inbox']) and 2==len(a.inboxes), "Correct Basic inboxes")
      self.assert_( 0==len(a.outboxes['signal']) and 0==len(a.outboxes['outbox']) and 2==len(a.outboxes), "Correct Basic outboxes")

   def test_SmokeTest_Arguments(self):
      "__init__ - Called with with arguments does not cause problems"
      AdaptiveCommsComponent.AdaptiveCommsComponent("hello","world")

   def test_addInbox_newName(self):
      "addInbox - adding an inbox with a completely new name results in that inbox being created/added"
      a=AdaptiveCommsComponent.AdaptiveCommsComponent()
      name=a.addInbox("name")
      self.assertEqual("name",name,"Inbox was added with the name we requested")
      inboxNames = list(a.inboxes)
      self.assert_( name in inboxNames, "Inbox was added")
      self.assert_( len(a.inboxes[name])==0, "Inbox created is empty")

   def test_addInbox_existingName(self):
      "addInbox - adding an inbox with an existing name results in an inbox being created/added with a similar name - same name with a suffix"
      import re
      a=AdaptiveCommsComponent.AdaptiveCommsComponent()
      name=a.addInbox("name")
      name=a.addInbox("name") # Attempt to create second box with existing name
      self.assertNotEqual("name",name,"Inbox was added with the name we requested")
      self.assert_(re.match("name",name), "Inbox created has a simlar name (same start)")

   def test_addOutbox_newName(self):
      "addOutbox - adding an outbox with a completely new name results in that outbox being created/added"
      a=AdaptiveCommsComponent.AdaptiveCommsComponent()
      name=a.addOutbox("name")
      self.assertEqual("name",name,"Inbox was added with the name we requested")
      outboxNames = list(a.outboxes)
      self.assert_( name in outboxNames, "Outbox was added")
      self.assert_( len(a.outboxes[name])==0, "Outbox created was empty")

   def test_addOutbox_existingName(self):
      "addOutbox - adding an outbox with an existing name results in an outbox being created/added with a similar name - same name with a suffix"
      import re
      a=AdaptiveCommsComponent.AdaptiveCommsComponent()
      name=a.addOutbox("name")
      name=a.addOutbox("name") # Attempt to create second box with existing name
      self.assertNotEqual("name",name,"Inbox was added with the name we requested")
      self.assert_(re.match("name",name), "Inbox created has a simlar name (same start)")

   def test_InboxModification(self):
      "-Acceptance Test - Check Addition and Deletion of Inboxes"
      a=AdaptiveCommsComponent.AdaptiveCommsComponent()
      addedNames = []
      for i in [1,2,3,4]:
         inboxNames = list(a.inboxes)
         name=a.addInbox("name")
         self.assert_( name not in inboxNames, "Inbox added had a new name")
         inboxNames = list(a.inboxes)
         self.assert_( name in inboxNames, "Inbox was added")
         addedNames.append(name)
         self.assert_( len(a.inboxes[name])==0, "Inbox created was empty")
      #
      for name in addedNames:
         a.deleteInbox(name)
         self.assert_( name not in a.inboxes, "Inbox was deleted")
      #
      self.assert_( 0==len(a.inboxes['control']) and 0==len(a.inboxes['inbox']) and 2==len(a.inboxes), "Only have default inboxes left")
      #
   def test_OutboxModification(self):
      "-Acceptance Test - Check Addition and Deletion of Outboxes"
      a=AdaptiveCommsComponent.AdaptiveCommsComponent()
      addedNames = []
      for i in [1,2,3,4]:
         outboxNames = list(a.outboxes)
         name=a.addOutbox("name")
         self.assert_( name not in outboxNames, "Outbox added had a new name")
         outboxNames = list(a.outboxes)
         self.assert_( name in outboxNames, "Outbox was added")
         addedNames.append(name)
         self.assert_( len(a.outboxes[name])==0, "Outbox created was empty")
      #
      for name in addedNames:
         a.deleteOutbox(name)
         self.assert_( name not in a.outboxes, "Outbox was deleted")
      #
      self.assert_( 0==len(a.outboxes['signal']) and 0==len(a.outboxes['outbox']) and 2==len(a.outboxes), "Only have one outbox left")

   def test_deleteInbox_invalidInbox(self):
      "deleteInbox - KeyError exception raised if you try to delete an inbox that does not exist  - this includes the case of an already deleted Inbox"
      a=AdaptiveCommsComponent.AdaptiveCommsComponent()
      self.assertRaises(KeyError, a.deleteInbox,"NonExistantInbox")

   def test_deleteInbox_validInbox(self):
      "deleteInbox - Deletes the named inbox"
      import random
      a=AdaptiveCommsComponent.AdaptiveCommsComponent()
      # Pick a random inbox to delete
      inboxNames=list(a.inboxes)
      inboxNames.sort()
      box=inboxNames[random.randint(0,len(inboxNames)-1)]

      a.deleteInbox(box)
      newinboxNames=list(a.inboxes)
      newinboxNames.sort()
      self.assertNotEqual(inboxNames,newinboxNames,"Inboxes were changed")
      self.assert_(box not in newinboxNames, "Inbox "+box+"was deleted")

   def test_deleteOutbox_invalidOutbox(self):
      "deleteOutbox - KeyError exception raised if you try to delete an outbox that does not exist - this includes the case of an already deleted Outbox"
      a=AdaptiveCommsComponent.AdaptiveCommsComponent()
      self.assertRaises(KeyError, a.deleteOutbox,"NonExistantInbox")

   def test_deleteOutbox_validOutbox(self):
      "deleteOutbox - Deletes the named outbox"
      import random
      a=AdaptiveCommsComponent.AdaptiveCommsComponent()
      # Pick a random inbox to delete
      outboxNames=list(a.outboxes)
      outboxNames.sort()
      box=outboxNames[random.randint(0,len(outboxNames)-1)]

      a.deleteOutbox(box)
      newoutboxNames=list(a.outboxes)
      newoutboxNames.sort()
      self.assertNotEqual(outboxNames,newoutboxNames,"Outboxes were changed")
      self.assert_(box not in newoutboxNames, "Outbox "+box+"was deleted")

   def test_trackResource_validDefaultInbox(self):
      "trackResource,retrieveTrackedResource - Adds to & retrieves from the mapping of inbox -> resource to a local store. This allows retrieval of the resource based on which inbox messages arrive on. Whilst designed for custom inboxes, it should work with the 'default' inboxes for a component"
      a=AdaptiveCommsComponent.AdaptiveCommsComponent()
      resource = "resource"
      inboxResourceAssociatedWith = "inbox"
      a.trackResource(resource, inboxResourceAssociatedWith)
      storedResource=a.retrieveTrackedResource(inboxResourceAssociatedWith)
      self.assertEqual(resource, storedResource, "The resource was correctly stored")

   def test_trackResource_validDynamicInbox(self):
      "trackResource,retrieveTrackedResource - Tracking resources using a custom dynamic inbox name should work."
      a=AdaptiveCommsComponent.AdaptiveCommsComponent()
      resource = "resource"
      inboxResourceAssociatedWith = a.addInbox("dynamic")
      a.trackResource(resource, inboxResourceAssociatedWith)
      storedResource=a.retrieveTrackedResource(inboxResourceAssociatedWith)
      self.assertEqual(resource, storedResource, "The resource was correctly stored")

   def test_trackResource_invalidInbox(self):
      "trackResource,retrieveTrackedResource - Tracking resources using an invalid inbox name should fail."
      import time
      a=AdaptiveCommsComponent.AdaptiveCommsComponent()
      resource = "resource"
      inboxResourceAssociatedWith = a.addInbox("name")+str(time.time()) # Ensure non-existant
      self.assertRaises(KeyError, a.trackResource, resource, inboxResourceAssociatedWith)

   def test_trackResourceInformation_validDefaultBoxes(self):
      "trackResourceInformation, retrieveTrackedResourceInformation - Associates communication & user aspects related to a resource. Associating default in/out boxes with a resource is valid"
      a=AdaptiveCommsComponent.AdaptiveCommsComponent()
      inboxes=list(a.inboxes)
      outboxes=list(a.outboxes)
      arbitraryInformation="qwertyuiopasdfghjklzxcvbnm"
      resource = "resource"
      a.trackResourceInformation(resource,inboxes,outboxes,arbitraryInformation)
      storedInboxes, storedOutboxes, storedInformation = a.retrieveTrackedResourceInformation(resource)
      self.assertEqual(inboxes, storedInboxes, "We can retrieve the right set of inboxes")
      self.assertEqual(outboxes, storedOutboxes, "We can retrieve the right set of outboxes")
      self.assertEqual(arbitraryInformation, storedInformation, "We can retrieve the right arbitrary information")

   def test_trackResourceInformation_validDynamicBoxes(self):
      "trackResourceInformation, retrieveTrackedResourceInformation - Associates communication & user aspects related to a resource. Associating dynamically created in/out boxes with a resource is the default"
      a=AdaptiveCommsComponent.AdaptiveCommsComponent()

      inboxes = [ a.addInbox("dynamic"),a.addInbox("dynamic"),a.addInbox("dynamic") ]
      outboxes = [ a.addOutbox("dynamic"),a.addOutbox("dynamic"),a.addOutbox("dynamic") ]
      arbitraryInformation="qwertyuiopasdfghjklzxcvbnm"
      resource = "resource"
      a.trackResourceInformation(resource,inboxes,outboxes,arbitraryInformation)
      storedInboxes, storedOutboxes, storedInformation = a.retrieveTrackedResourceInformation(resource)
      self.assertEqual(inboxes, storedInboxes, "We can retrieve the right set of inboxes")
      self.assertEqual(outboxes, storedOutboxes, "We can retrieve the right set of outboxes")
      self.assertEqual(arbitraryInformation, storedInformation, "We can retrieve the right arbitrary information")

   def test_trackResourceInformation_invalidInboxes(self):
      "trackResourceInformation, retrieveTrackedResourceInformation - Tracking invalid inboxes using a resource fails."
      import time
      a=AdaptiveCommsComponent.AdaptiveCommsComponent()

      inboxes = [ a.addInbox("name")+str(time.time()) ] # This list of inboxes is "guaranteed" not to exist
      outboxes = [ a.addOutbox("dynamic") ] # List of "guaranteed" valid  outboxes
      arbitraryInformation="qwertyuiopasdfghjklzxcvbnm"
      resource = "resource"
      self.assertRaises(KeyError, a.trackResourceInformation, resource,inboxes,outboxes,arbitraryInformation)

   def test_trackResourceInformation_invalidOutboxes(self):
      "trackResourceInformation, retrieveTrackedResourceInformation - Tracking invalid outboxes using a resource fails."
      import time
      a=AdaptiveCommsComponent.AdaptiveCommsComponent()

      inboxes = [ a.addInbox("dynamic") ] # List of "guaranteed" valid  outboxes
      outboxes = [ a.addOutbox("name")+str(time.time()) ] # This list of inboxes is "guaranteed" not to exist
      arbitraryInformation="qwertyuiopasdfghjklzxcvbnm"
      resource = "resource"
      self.assertRaises(KeyError, a.trackResourceInformation, resource,inboxes,outboxes,arbitraryInformation)


   def _test_Notes(self):
      "-XXXXX mps 29/5/3- Check that subclasses operate correctly (Needs writing)"
      pass
#      print "Not written"

if __name__=="__main__":
   unittest.main()
