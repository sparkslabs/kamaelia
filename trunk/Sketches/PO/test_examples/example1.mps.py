#!/usr/bin/env python
"""

Example: Producer Testing

This example shows how to test a component that produces messages.
Specifically, we want to test that a particular set of messages is
produced by it in a given order.

The way the test is structured is as follows:

   * Our component under test is called SimpleComponent
   
   * The class SimpleComponentTestCase is a class that contains the
     tests for this component.
     
     * Individual tests within this class are contained in
       methods named test*

     * This class only contains one such class.


The original "documentation" for this file says this:
    It will call suite() and execute that TestSuite

I can't see (from this file) where that happens, so I can't document that.

""" 

import Axon
from Axon.Ipc import producerFinished


#
# We need to import KamTestCase so that we can use it...
#
# It currently lives in Kamaelia.Testing.KamTestCase, which is not in the
# standard tree, and this location has not been discussed with others. As a
# result this import line is subject to change since the location and naming
# may change in future.
#
# ISSUE: In order for this line to work, you must be using Kamaelia
# ISSUE: from <UNDOCUMENTED>
#
# ISSUE: This should probably be in Axon.* really
#
import Kamaelia.Testing.KamTestCase as KamTestCase


class SimpleComponent(Axon.Component.component):
    
    """
    This is our producer under test. It currently just sends out 3 messages,
    yielding after sending each message. Once it's done, it sends a
    producerFinished message to it's signal outbox.
    
    It's an entirely artificial example.
    """
    
    def main(self): 
        """Sends 3 messages, yielding after each, then producerFinished,
        then exits."""
        
        self.send('msg1', 'outbox') ; yield 1
        
        self.send('msg2', 'outbox') ; yield 1
        
        self.send('msg3', 'outbox') ; yield 1
        
        self.send(producerFinished(self), 'signal') ; yield 1


########################################################################
#
# This is a TestCase. A TestCase contains multiple tests, and might contain
# some shared code for initialization and cleaning resources
#

class SimpleComponentTestCase(KamTestCase.KamTestCase):
    """"
    This testcase tests SimpleComponent
    
    It contains one test that *attempts* to do the following:
    
        * Waits for messages to be recieved from the component, and confirms
          that the messages recieved are "msg1", "msg2", "msg3" (all in the
          producers "outbox"), followed by a producerFinished message.
          
    ISSUE: it doesn't test what the tests think they test... (doesn't reflect real world usage)
    """

    def setUp(self):
        """        
        This method sets up a clean/base environment for the tests to run in. 
        This method is called before each and every test. If you want to
        initialisation which is global to all tests before this, you should
        do this <UNDOCUMENTED>.
        
        This method is not required. If you do not provide it, <UNDOCUMENTED>.
            
        In this particular test case, we always create a new SimpleComponent
        and store it in self.simpleComponent, and then we initialise the
        test case, but calling initializeSystem, which <UNDOCUMENTED>.

        ISSUE: core details about setUp are undocumented
        
        ISSUE: generator vs non-generator. Pre-initializeSystem vs
        ISSUE: Post-initialization. (some tests require setup of an active
        ISSUE: environment beyond this simplistic view
        
        """
        self.simpleComponent = SimpleComponent()
        self.initializeSystem(self.simpleComponent)

    def tearDown(self):
        """
        
        This method is the logical opposite of setUp. If setUp is called
        before each and every test case, tearDown is called after each and
        every testcase. A key reason here for this is releasing resources.

        This method is not required. If you do not provide it, <UNDOCUMENTED>.

        In this particular example, it doesn't do anything - since no
        resources are used. 

        ISSUE: Doesn't deal with kamaelia based services/resources at all.
        """
        pass
    
        
    ########################################################################
    #
    # Now, the tests. Every test is a method which starts by "test"
    #
    def testRightBehaviour(self): # ISSUE: *TERRIBLE NAME*

        # Let's wait for a message received from outbox, for a second
        # Now, since this is the first message, it must be 'msg1'
        
        # Wait for the first message. We use a ".get" method with a timeout
        # of "1"

        # ISSUE: It's undocumented where the .get method sits, I presume
        # it's *defined* in KamTestCase.  if it's blocking or how long "1"
        # refers to. Is it one cycle through the scheduler? Is it one 1
        # millisecond? Is it one second? Why is 1 second "enough" or "too
        # long"
        
        dataReceived = self.get('outbox', timeout=1)
        self.assertEquals('msg1', dataReceived)


        # Wait for and check the second message. This time with a timeout of 2.
        # This is because <UNDOCUMENTED>        
        dataReceived = self.get('outbox', timeout=2)
        self.assertEquals('msg2', dataReceived)
        

        # Wait for and check the third message.
        # Since this has no timeout, this means we expect the result <UNDOCUMENTED TIMEFRAME>
        
        dataReceived = self.get('outbox')
        self.assertEquals('msg3', dataReceived)
        
        
        # Next check that the component sends a producerFinished finished to the signal outbox.
        #
        # It's worth noting that we're not checking whether this is recieved
        # before or after any of the other messages listed above.
        #
        
        dataReceived = self.get('signal')
        self.assertTrue(isinstance(dataReceived, producerFinished))
        
        #
        # Finally check that nothing else is coming ?
        #
        # ISSUE: How is this ascertained? This appears to just check the
        # ISSUE: outbox is empty. Do we also check the component has stopped
        # ISSUE: running ?
        
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

    # ISSUE: this line simply invokes "Magic". I see *nowhere* in this that
    # ISSUE: causes the code to run the code in this file.

    KamTestCase.main(defaultTest='suite')




