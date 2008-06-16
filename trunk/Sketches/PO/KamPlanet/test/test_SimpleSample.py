from Axon.Ipc import producerFinished
import kamtest.KamTestCase as KamTestCase
import kamtest.KamExpectMatcher as KamExpectMatcher
from SimpleSample import SimpleComponent

class SimpleSampleTestCase(KamTestCase.KamTestCase):
    def setUp(self):
        self.simpleSample = SimpleComponent()
        self.initializeSystem(self.simpleSample)
        
    def testForwardsNumbers(self):
        self.put(5, 'numbers')
        self.put(6, 'numbers')
        self.putYield(10)
        self.put(producerFinished(), 'control')
        self.assertStopping()
        self.assertEquals('5', self.get('outbox'))
        self.assertEquals('6', self.get('outbox'))
        self.assertOutboxEmpty('outbox')
        self.assertTrue(isinstance(self.get('signal'), producerFinished))
        self.assertOutboxEmpty('signal')
        
    def testForwardsNumbers(self):
        self.put(5, 'numbers')
        self.put(6, 'numbers')
        self.put(7, 'numbers')
        self.put(producerFinished(), 'control')
        self.expect(KamExpectMatcher.RegexpMatcher('^6$'), 'outbox')
        self.assertEquals('7', self.get('outbox'))
        self.assertOutboxEmpty('outbox')
        self.assertTrue(isinstance(self.get('signal'), producerFinished))
        self.assertOutboxEmpty('signal')

def suite():
    return KamTestCase.makeSuite(
            SimpleSampleTestCase.getTestCase()
        )
        
if __name__ == '__main__':
    KamTestCase.main(defaultTest='suite')
