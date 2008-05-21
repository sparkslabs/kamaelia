from Axon.Component import component
from Kamaelia.Util.Backplane import Backplane,  SubscribeTo
from Axon.Ipc import newComponent, producerFinished, shutdownMicroprocess
from Kamaelia.Chassis.Pipeline import Pipeline

class Logger(component):
    """
    This component is used to write messages to file.  Upon instantiation, the
    a backplane is registered with the name LOG_ + logname, so that a log named
    'foo.bar' would be registered under 'LOG_foo.bar'.

    Please note that the Logger will not be shut down automatically.  It must be
    sent a shutdown message via its control box.
    """
    Inboxes = { 'inbox' : 'Receive a tuple containing the filename and message to log',
                'control' : 'Receive shutdown messages',}
    Outboxes = {'outbox' : 'NOT USED',
                'signal' : 'Send shutdown messages',}

    def __init__(self,  logname):
        super(Logger,  self).__init__()
        self.logname = logname
        self.bplane = Backplane('LOG_' + logname)
        self.subscriber = SubscribeTo(logname)

        #add the components as children
        self.addChildren(self.subscriber, self.bplane)
        self.link((self.subscriber,  'outbox'),  (self,  'inbox'))
        self.link((self, 'signal'), (self.bplane, 'control'))

        self.first_run = True

    def main(self):
        if self.first_run:
            self.bplane.activate()
            self.subscriber.activate()
            self.first_run = False

        not_done = True
        while not_done:
            while self.dataReady('inbox'):
                msg = self.recv('inbox')
                print "received %s" % (msg)

                file = open(self.logname, 'a')
                file.write(msg)
                file.close()

            while self.dataReady('control'):
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
        """
        A simple component to repeatedly output message.
        """
        Inboxes = {'inbox' : 'NOT USED',
                    'control' : 'receive shutdown messages',}
        Outboxes = {'outbox' : 'push data out',
                    'signal' : 'send shutdown messages',}
        def __init__(self, message):
            super(Producer, self).__init__()
            self.message = message

        def main(self):
            not_done = True
            while not_done:
                self.send(self.message, 'outbox')
                print 'sent %s' % (self.message)
                while self.dataReady('control'):
                    msg = self.recv('control')
                    self.send(msg, 'signal')
                    if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                        not_done = False
                yield 1

            self.send(producerFinished(), 'signal')
            self.send(producerFinished(), 'logger-signal')

    class SomeChassis(component):
        """
        A toy example of a chassis of some kind.  This will run each component 50
        times and then send each one a shutdown message.
        """
        Inboxes = {'inbox' : 'NOT USED',
                    'control' : 'NOT USED',}
        Outboxes = {'outbox' : 'NOT USED',
                    'signal-logger' : 'send shutdown signals to the logger',
                    'signal-producer' : 'send shutdown signals to the producer',}
        def __init__(self, Producer, logname):
            super(SomeChassis, self).__init__()

            self.Logger = Logger(logname)
            self.logname = logname
            self.Producer = Producer
            self.link((self, 'signal-logger'), (self.Logger, 'control'))
            self.link((self, 'signal-producer'), (self.Producer, 'control'))

        def main(self):
            self.Logger.activate()
            Pipeline(self.Producer, PublishTo('LOG_' + self.logname)).activate()
            i = 0

            while i < 50:
                print 'i = ' + str(i)
                i += 1
                yield 1

            self.send(shutdownMicroprocess(), 'signal-logger')
            self.send(shutdownMicroprocess(), 'signal-producer')


SomeChassis(Producer = Producer('blah'), logname = 'blah.log').run()