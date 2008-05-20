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
        self.refcount = 0
        
        self.bplane.activate()
        self.subscriber.activate()

        #add the components as children
        self.addChildren(self.subscriber, self.bplane)
        self.link((self.subscriber,  'outbox'),  (self,  'inbox'))
        self.link((self, 'signal'), (self.bplane, 'control'))

    def main(self):
        not_done = True
        while not_done:
            while self.dataReady('inbox'):
                msg = self.recv('inbox')
                print "received %s" % (msg)
                
                file = open(self.logname, 'a')
                file.write(msg)
                file.close()
                
            while self.dataReady('control'):    #TODO:  Move refcounting to the backplane somehow
                msg = self.recv('control')
                if isinstance(msg, (producerFinished)):
                    self.refcount -= 1
                    if not self.refcount:
                        not_done = False
                        self.shutdown(msg)
                if isinstance(msg, (newComponent)):
                    self.refcount += 1
                if isinstance(msg, (shutdownMicroprocess)):
                    not_done = False
                    self.shutdown(msg)
            if not_done:
                self.pause()
                yield 1
        
    def shutdown(self, msg):
        self.send(msg, 'signal')
        print 'shutting down logger!'
        print 'dataReady("inbox") = ' + str(self.dataReady('inbox'))
        self.removeChild(self.bplane)
        self.removeChild(self.subscriber)
if __name__ == '__main__':
    from Kamaelia.Util.Backplane import PublishTo
    
    class Producer(component):
        Inboxes = {'inbox' : 'NOT USED',
                    'control' : 'receive shutdown messages',}
        Outboxes = {'outbox' : 'push data out',
                    'signal' : 'send shutdown messages',
                    'logger-signal' : 'send shutdown messages to the logger',}
        def __init__(self, message, logger, times):
            super(Producer, self).__init__()
            self.message = message
            self.times = times
            self.link((self, 'logger-signal'), (logger, 'control'))
            self.send(newComponent(), 'logger-signal')
            
        def main(self):
            for i in xrange(self.times):
                self.send(self.message, 'outbox')
                print 'sent %s' % (self.message)
                yield 1
            
            self.send(producerFinished(), 'signal')
            self.send(producerFinished(), 'logger-signal')
            
    log = Logger('blah.log')
    log.activate()
    
    Pipeline(Producer('hello\n', log, 50), PublishTo('blah.log')).activate()
    Pipeline(Producer('bye\n', log, 75), PublishTo('blah.log')).run()