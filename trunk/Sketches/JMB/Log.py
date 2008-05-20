from Axon.Component import component
from Kamaelia.Util.Backplane import Backplane,  SubscribeTo
from Axon.Ipc import newComponent, producerFinished, shutdownMicroprocess
from Kamaelia.Chassis.Pipeline import Pipeline

class Logger(component):
    Inboxes = { 'inbox' : 'Receive a tuple containing the filename and message to log',
                'control' : 'Receive shutdown messages',}
    Outboxes = {'outbox' : 'NOT USED',
                'signal' : 'Send shutdown messages',}
    
    def __init__(self,  logname):
        super(Logger,  self).__init__()
        self.logname = logname
        self.bplane = Backplane(logname)
        self.subscriber = SubscribeTo(logname)
        
        self.bplane.activate()
        self.subscriber.activate()

        #add the components as children
        self.addChildren(self.subscriber, self.bplane)

        self.link((self.subscriber,  'outbox'),  (self,  'inbox'))

    def main(self):
        not_done = True
        while not_done:
            while self.dataReady('inbox'):
                msg = self.recv('inbox')
                print "received %s" % (msg)
                
                file = open(self.logname, 'a')
                file.write(msg)
                file.close()
                
            while self.dataReady('control'):
                msg = self.recv('control')
                self.send(msg, 'signal')
                if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                    not_done = False
            
            if not_done:
                self.pause()
                yield 1
        
            
if __name__ == '__main__':
    from Kamaelia.Util.Backplane import PublishTo
    
    class Producer(component):
        def __init__(self, message):
            super(Producer, self).__init__()
            self.message = message
            
        def main(self):
            for i in xrange(50):
                self.send(self.message, 'outbox')
                print 'sent %s' % (self.message)
                yield 1
            
            self.send(shutdownMicroprocess(), 'signal')
            
    log = Logger('blah.log')
    log.activate()
    
    Pipeline(Producer('hello\n'), PublishTo('blah.log')).run()