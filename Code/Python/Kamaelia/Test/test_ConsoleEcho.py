#!/usr/bin/env python2.3
#
# Full coverage testing of the NullPayloadRTP module.
#

# Test the module loads
import unittest
import sys ; sys.path.append("..")
import ConsoleEcho

class ConsoleEcho_Test(unittest.TestCase):
   def test_init_minArgs(self):
       """Smoke test with minimal arguments"""
       P = ConsoleEcho.consoleEchoer()
       self.assertEqual(P.__class__, ConsoleEcho.consoleEchoer, "Correctly initialised value created")
       self.assert_(not P.forwarder, "This is not a forwarder")
       self.assert_(P.init)

   def test_init_forwarder(self):
       """Smoke test creating a forwarder"""
       P = ConsoleEcho.consoleEchoer(forwarder=True)
       self.assertEqual(P.__class__, ConsoleEcho.consoleEchoer, "Correctly initialised value created")
       self.assert_(P.forwarder, "This is a forwarder")
       self.assert_(P.init)

   def test_mainBody_NonForwarder(self):
       """Basic test of a mainBody on a non-forwarder"""
       P = ConsoleEcho.consoleEchoer()
       self.assertEqual(P.mainBody(), 3, "With no data waiting the system should just loop")

       P._deliver("junk", "inbox")
       self.assertEqual(len(P.inboxes["inbox"]), 1, "Data ready to collect")
       self.assertEqual(P.mainBody(), 2, "The data waiting will be collected and displayed")
       self.assertEqual(len(P.inboxes["inbox"]), 0, "The data was collected")

       P._deliver(("some", {"structured": "junk"}) , "inbox")
       self.assertEqual(len(P.inboxes["inbox"]), 1, "Data ready to collect")
       self.assertEqual(P.mainBody(), 2, "The data waiting will be collected and displayed")
       self.assertEqual(len(P.inboxes["inbox"]), 0, "The data was collected")

       P._deliver(("some", {"structured": "junk"}) , "inbox")
       P._deliver(("some", "more", {"structured": "junk"}) , "inbox")
       self.assertEqual(len(P.inboxes["inbox"]), 2, "Data ready to collect")
       self.assertEqual(P.mainBody(), 2, "A piece of data waiting will be collected and displayed")
       self.assertEqual(len(P.inboxes["inbox"]), 1, "The data was collected")
       self.assertEqual(P.mainBody(), 2, "A piece of data waiting will be collected and displayed")
       self.assertEqual(len(P.inboxes["inbox"]), 0, "All data has been collected")

   def test_mainBody_Forwarder(self):
       """Test of the mainbody of a forwarder console echoer component."""
       P = ConsoleEcho.consoleEchoer(forwarder=True)
       self.assertEqual(P.mainBody(), 3, "With no data waiting the system should just loop")

       P._deliver("junk", "inbox")
       self.assertEqual(len(P.inboxes["inbox"]), 1, "Data ready to collect")
       self.assertEqual(P.mainBody(), 1, "The data waiting will be collected, displayed and forwarded")
       self.assertEqual(len(P.inboxes["inbox"]), 0, "The data was collected")
       self.assertEqual(len(P.outboxes["outbox"]), 1, "Data has been forwarded to the outbox")

       P._deliver(("some", {"structured": "junk"}) , "inbox")
       self.assertEqual(len(P.inboxes["inbox"]), 1, "Data ready to collect")
       self.assertEqual(P.mainBody(), 1, "The data waiting will be collected, displayed and forwarded")
       self.assertEqual(len(P.inboxes["inbox"]), 0, "The data was collected")
       self.assertEqual(len(P.outboxes["outbox"]), 2, "Data has been forwarded to the outbox")

       P._deliver(("some", {"structured": "junk"}) , "inbox")
       P._deliver(("some", "more", {"structured": "junk"}) , "inbox")
       self.assertEqual(len(P.inboxes["inbox"]), 2, "Data ready to collect")
       self.assertEqual(P.mainBody(), 1, "A piece of data waiting was collected, displayed and forwarded")
       self.assertEqual(len(P.inboxes["inbox"]), 1, "The data was collected")
       self.assertEqual(len(P.outboxes["outbox"]), 3, "Data has been forwarded to the outbox")

       self.assertEqual(P.mainBody(), 1, "All data waiting has be collected, displayed and forwarded")
       self.assertEqual(len(P.inboxes["inbox"]), 0, "All data has been collected")
       self.assertEqual(len(P.outboxes["outbox"]), 4, "Data has been forwarded to the outbox")

if __name__=="__main__":
   unittest.main()
