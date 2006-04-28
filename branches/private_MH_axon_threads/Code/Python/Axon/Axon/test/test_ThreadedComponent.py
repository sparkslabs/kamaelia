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

# Test the module loads
import unittest
import sys ; sys.path.append(".") ; sys.path.append("..")

from ThreadedComponent import threadedcomponent, threadedadaptivecommscomponent

class threadedcomponent_Test(unittest.TestCase):
    
    def test_smoketest_init(self):
        """__init__ - class constructor is called with no arguments."""
        c = threadedcomponent()
        
        self.assert_(len(c.inboxes.keys()) == 2, "by default, has 2 inboxes")
        self.assert_("inbox" in c.inboxes.keys(), "by default, has 'inbox' inbox")
        self.assert_("control" in c.inboxes.keys(), "by default, has 'control' inbox")
        
        self.assert_(len(c.outboxes.keys()) == 2, "by default, has 2 outboxes")
        self.assert_("outbox" in c.outboxes.keys(), "by default, has 'outbox' outbox")
        self.assert_("signal" in c.outboxes.keys(), "by default, has 'signal' outbox")
    
    
    
class threadedadaptivecommscomponent_Test(unittest.TestCase):
    
    def test_smoketest_init(self):
        """__init__ - class constructor is called with no arguments."""
        c = threadedadaptivecommscomponent()
        
        self.assert_(len(c.inboxes.keys()) == 2, "by default, has 2 inboxes")
        self.assert_("inbox" in c.inboxes.keys(), "by default, has 'inbox' inbox")
        self.assert_("control" in c.inboxes.keys(), "by default, has 'control' inbox")
        
        self.assert_(len(c.outboxes.keys()) == 2, "by default, has 2 outboxes")
        self.assert_("outbox" in c.outboxes.keys(), "by default, has 'outbox' outbox")
        self.assert_("signal" in c.outboxes.keys(), "by default, has 'signal' outbox")
    
if __name__ == "__main__":
    unittest.main()