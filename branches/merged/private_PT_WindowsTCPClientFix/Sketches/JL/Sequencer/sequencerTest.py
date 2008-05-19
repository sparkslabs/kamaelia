#! /usr/bin/env python
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
