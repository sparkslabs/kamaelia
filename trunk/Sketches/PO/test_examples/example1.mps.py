#!/usr/bin/env python
"""
This example only checks the output from a simple component

It will call suite() and execute that TestSuite

This is a very simple sample. In order to keep it simple, I write it
all in the same file.
""" 

import Axon
from Axon.Ipc import producerFinished

class SimpleComponent(Axon.Component.component):
    def main(self):
        self.send('msg1', 'outbox')
        yield 1
        self.send('msg2', 'outbox')
        yield 1
        self.send('msg3', 'outbox')
        yield 1
        self.send(producerFinished(self), 'signal')
        yield 1



########################################################################
#
# Import KamTestCase (this is subject to change)
#

import Kamaelia.Testing.KamTestCase as KamTestCase



########################################################################
#
# This is a TestCase. A TestCase contains multiple tests, and might contain
# some shared code for initialization and cleaning resources
#

class SimpleComponentTestCase(KamTestCase.KamTestCase):
    """ This code will be executed BEFORE EACH test
        It's not required, but it's very useful to initialize the component
    """
    def setUp(self):
        """Instanciate the component under test. Initialize the system"""
        self.simpleComponent = SimpleComponent()
        self.initializeSystem(self.simpleComponent)
    
    def tearDown(self):
        """This code will be executed AFTER EACH test
        It's also not required, but it's useful to release resources
        """
        pass
    
        
    ########################################################################
    #
    # Now, the tests. Every test is a method which starts by "test"
    #
    def testRightBehaviour(self):

        # Let's wait for a message received from outbox, for a second
        # Now, since this is the first message, it must be 'msg1'
        dataReceived = self.get('outbox', timeout=1)
        self.assertEquals('msg1', dataReceived)
        
        # Let's wait for a message received from outbox, for two seconds
        # It must be 'msg2'
        dataReceived = self.get('outbox', timeout=2)
        self.assertEquals('msg2', dataReceived)
        
        # Let's wait for a message received from outbox, during the standard time
        # It must be 'msg3'
        dataReceived = self.get('outbox')
        self.assertEquals('msg3', dataReceived)
        
        # Let's wait for the signal
        # It must inherit from Axon.IPC.producerFinished
        dataReceived = self.get('signal')
        self.assertTrue(isinstance(dataReceived, producerFinished))
        
        # We check that nothing else is coming
        self.assertOutboxEmpty('control')
        self.assertOutboxEmpty('outbox')


########################################################################
#
#
def suite():
    """
    This method is not required, but it's useful to build a unittest-compatible
    TestSuite

    This is a classmethod which is present in all the KamTestCases.
    
    The method returns a unittest-compatible TestCase, that will behave as
    explained above, but through the standard unittest API.
    
    Thanks to this, these tests can be integrated in any framework which
    relies on unittest, so it may be easily integrated into software as
    apycot or CruiseControl, etc.
    """

    unittestCompatibleTestCase = SimpleComponentTestCase.getTestCase()
    return KamTestCase.makeSuite(unittestCompatibleTestCase)

if __name__ == '__main__':
    KamTestCase.main(defaultTest='suite')




