#!/usr/bin/env python

from Axon.Component import component
from Axon.ThreadedComponent import threadedcomponent

class OutboxBundle(component):
    Inboxes = {}
    Outboxes = ['outbox', 'signal']
    
class Producer(component):
    bundle=None
    message='Hello from Producer'
    def main(self):
        self.bundle.send(self.message, 'outbox')
        yield 1
        
class Consumer(component):
    def main(self):
        while not self.dataReady('inbox'):
            yield 1
            
        print self.recv('inbox'), ' received by Consumer'
        
class ThreadedConsumer(threadedcomponent):
    def main(self):
        while not self.dataReady('inbox'):
            pass
        
        print self.recv('inbox'), ' received by ThreadedConsumer'
        
class ThreadedProducer(threadedcomponent):
    message='Hello from ThreadedProducer'
    bundle = None
    def main(self):
        self.bundle.send(self.message, 'outbox')
        

def relink(bundle, to_component):
    bundle.unlink(bundle)
    bundle.link((bundle, 'outbox'), (to_component, 'inbox'))

bundle = OutboxBundle()
consumer = Consumer()
producer = Producer(bundle=bundle)

bundle.link((bundle, 'outbox'), (consumer, 'inbox'))

consumer.activate()
producer.run()

threaded_cons = ThreadedConsumer()
producer = Producer(bundle=bundle)

relink(bundle, threaded_cons)

threaded_cons.activate()
producer.run()

threaded_prod = ThreadedProducer(bundle=bundle)
threaded_cons = ThreadedConsumer()

relink(bundle, threaded_cons)

threaded_cons.activate()
threaded_prod.run()

threaded_prod = ThreadedProducer(bundle=bundle)
consumer = Consumer()

relink(bundle, consumer)

threaded_prod.activate()
consumer.run()


