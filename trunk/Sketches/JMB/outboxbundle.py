#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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


