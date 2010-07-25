#! /usr/bin/env python
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
from Axon.Ipc import shutdownMicroprocess, producerFinished
import time
#A component that sends the 'NEXT' message upon receiving any messages in its inbox.


class Signaler(component):
    #Inboxes: inbox, control
    #Outboxes: outbox, signal
    def __init__(self):
        super(Signaler, self).__init__()        
    def main(self):
        while True:
            yield 1
            if self.dataReady('inbox'):
                print 'received', self.recv('inbox') #clear that message from inbox
                self.send('NEXT', 'outbox')
        

class SignalPusher(component):
    n = 0
    def __init__(self):
        super(SignalPusher, self).__init__()
        
    def main(self):
        while self.n < 20:
            time.sleep(0.5)
            print "SignalPusher sending"
            self.send('NEXT', 'outbox')
            self.n += 1
            yield 1
        self.send(shutdownMicroprocess(), 'signal')
        
        
if __name__ == '__main__':
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    from Kamaelia.Chassis.Pipeline import Pipeline
    from sequencer import *

    Pipeline(SignalPusher(), sequencer(), ConsoleEchoer()).run()
