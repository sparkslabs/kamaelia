#!/usr/bin/env python

########################################################################
#
# This is a very simple sample. In order to keep it simple, I write it
# all in the same file.
#
########################################################################
# This example interacts with a component and shows how to mock an
# internal component. This is, there are components that use resources 
# such as networking/files/etc., which make it difficult to test 
# attached components. In "normal" testing frameworks this is sometimes 
# handled through mock objects, which are objects that are easily 
# configured and control the behaviour of the caller objects. For 
# instance, you'll control what methods the caller called, with what 
# parameters, you can control in which order the caller used, what 
# results should the object return to the caller (or which exceptions), 
# etc.
# 
# Here there is a far better explanation about mock objects, and it also 
# explains how to apply it using JMock and EasyMock:
# http://martinfowler.com/articles/mocksArentStubs.html
# 
# For Python, there is, for instance, Python Mocker:
# http://labix.org/mocker
# 
# The testing framework includes a way to create mock Axon.components, as
# exposed below
# 

import Axon
from Axon.Ipc import producerFinished

class ComponentToBeMocked(Axon.Component.component):
    Outboxes = {
        'outbox'  : 'from component', 
        'outbox2' : 'another outbox', 
        'signal'  : 'from component'
    }
    def __init__(self, hostname, port):
        super(ComponentToBeMocked, self).__init__()
        
    def main(self):
        # (just imagine)
        # This component somehow connects to a weird socket etc. 
        # and gather information, etc. and then it starts sending
        # to outbox this information.
        # The idea is that deploying the required infrastructure 
        # may be difficult
        self.send('message1', 'outbox')
        yield 1
        self.send('message2', 'outbox')
        yield 1
        self.send('message3', 'outbox2')
        yield 1

class SimpleComponent(Axon.Component.component):
    Inboxes = {
            '_inbox'  : 'we receive information from ComponentToBeMocked through this inbox', 
            '_inbox2' : 'we receive more information from ComponentToBeMocked through this inbox', 
            'inbox'   : 'we receive tuples as in (hostname,port) through this inbox', 
            'control' : 'From component...', 
        }
    MyResource = ComponentToBeMocked
    def main(self):
        while True:
            while self.dataReady('inbox'):
                hostname, port = self.recv('inbox')
                # Normally someone would write:
                # childComponent = ComponentToBeMocked(hostname, port)
                # In order to make it easily testable, here we use:
                childComponent = self.MyResource(hostname, port)
                
                childComponent.link((childComponent, 'outbox'), (self, '_inbox'))
                childComponent.link((childComponent, 'outbox2'), (self, '_inbox2'))
                
                self.addChildren(childComponent)
                childComponent.activate()
                
            while self.dataReady('_inbox'):
                data = self.recv('_inbox')
                self.send(data, 'outbox')
                
            while self.dataReady('_inbox2'):
                data = self.recv('_inbox2')
                self.send(data, 'outbox')
                
            while self.dataReady('control'):
                data = self.recv('control')
                self.send(data, 'signal')
                return
            yield 1

import Kamaelia.Testing.KamTestCase as KamTestCase

MOCKED = True

if not MOCKED:
    # This would be the "normal way" to test it, deploying the required resources
    class SimpleComponentTestCase(KamTestCase.KamTestCase):
        def setUp(self):
            self.simpleComponent = SimpleComponent()
            self.initializeSystem(self.simpleComponent)
        
        def testRightBehaviour(self):
            # We put one message
            self.put(('127.0.0.1', 8080), 'inbox')
            
            dataReceived = self.get('outbox', timeout=1)
            self.assertEquals('message1', dataReceived)
            dataReceived = self.get('outbox', timeout=1)
            self.assertEquals('message2', dataReceived)
            dataReceived = self.get('outbox', timeout=1)
            self.assertEquals('message3', dataReceived)
            
            # Then kill it
            msg = producerFinished()
            self.put(msg, 'control')
            dataReceived = self.get('signal')
            self.assertEquals(msg, dataReceived)
            
            # And after it... nothing else
            self.assertOutboxEmpty('control')
            self.assertOutboxEmpty('outbox')
else:
    # In this version we don't deal with ComponentToBeMocked, so we don't need to deploy
    # anything to test the SimpleComponent internal logic.
    class SimpleComponentTestCase(KamTestCase.KamTestCase):
        def setUp(self):
            self.simpleComponent = SimpleComponent()
            self.initializeSystem(self.simpleComponent)
        
        def testRightBehaviour(self):
            expectedArgs = ('127.0.0.1', 8080)
            
            # We overide the MyResource element
            self.mockedComponent = self.createMock(ComponentToBeMocked)
            def creator(*args):
                self.assertEqual(expectedArgs, args)
                return self.mockedComponent
            self.simpleComponent.MyResource = creator
            
            # We put the creation arguments message
            self.put(expectedArgs, 'inbox')
            
            # We say what the mocked component could say:
            self.mockedComponent.addMessage('this.is.from.the.mock', 'outbox')
            
            # And we see how SimpleComponent acts consecuentially
            dataReceived = self.get('outbox', timeout=1)
            self.assertEquals('this.is.from.the.mock', dataReceived)

            # With different outboxes (and inboxes) still works
            self.mockedComponent.addMessage('this.is.from.the.mock2', 'outbox2')
            dataReceived = self.get('outbox', timeout=1)
            self.assertEquals('this.is.from.the.mock2', dataReceived)

            # We finish the mock object
            self.mockedComponent.stopMockObject()
            
            # Then kill the tested object
            msg = producerFinished()
            self.put(msg, 'control')
            dataReceived = self.get('signal')
            self.assertEquals(msg, dataReceived)
            
            # And after it... nothing else
            self.assertOutboxEmpty('control')
            self.assertOutboxEmpty('outbox')

def suite():
    return KamTestCase.makeSuite(SimpleComponentTestCase.getTestCase())

if __name__ == '__main__':
    KamTestCase.main(defaultTest='suite')
