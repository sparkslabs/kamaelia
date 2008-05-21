from Axon.Component import component
from Kamaelia.Util.Backplane import Backplane,  SubscribeTo
from Axon.Ipc import newComponent, producerFinished, shutdownMicroprocess
from Kamaelia.Chassis.Graphline import Graphline
import datetime

def wrapMessage(message):
    """
    This function is intended to be the default message wrapper.  It returns
    the given message with the date/time in isoformat at the beginning and a
    newline at the end.
    """
    dt = datetime.datetime.now().isoformat()
    return '%s: %s\n' % (dt, message)

def nullWrapper(message):
    """
    This method returns the message that was sent to it.  It is used in situations
    where you just want to post the raw text to the log.
    """
    return message


class Logger(component):
    """
    This component is used to write messages to file.  Upon instantiation, the
    a backplane is registered with the name LOG_ + logname, so that a log named
    'foo.bar' would be registered under 'LOG_foo.bar'.

    Please note that the Logger will not be shut down automatically.  It must be
    sent a shutdown message via its control box.  Typically this component is to
    be used by a Chassis or some other Parent component to provide a log for its
    children.
    """
    Inboxes = { 'inbox' : 'Receive a tuple containing the filename and message to log',
                'control' : 'Receive shutdown messages',}
    Outboxes = {'outbox' : 'NOT USED',
                'signal' : 'Send shutdown messages',}

    def __init__(self,  logname, wrapper = wrapMessage):
        """
        Initializes a new Logger.

        -logname - the name of the log to write to
        -wrapper - a method that takes a message as an argument and returns a
            formatted string to put in the log.
        """
        super(Logger,  self).__init__()
        self.logname = logname
        self.bplane = Backplane('LOG_' + logname)
        self.subscriber = SubscribeTo('LOG_' + logname)
        self.wrapper = wrapper

        #add the components as children
        self.addChildren(self.subscriber, self.bplane)
        self.link((self.subscriber,  'outbox'),  (self,  'inbox'))
        self.link((self, 'signal'), (self.bplane, 'control'))


    def main(self):
        self.bplane.activate()
        self.subscriber.activate()
        self.first_run = False

        not_done = True
        while not_done:
            if self.dataReady('inbox'):
                file = open(self.logname, 'a')
                while self.dataReady('inbox'):
                    msg = self.recv('inbox')
                    file.write(self.wrapper(msg))
                file.close()

            while self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, (shutdownMicroprocess)):
                    not_done = False
                    self.shutdown(msg)
            if not_done:
                self.pause()
                yield 1

    def shutdown(self, msg):
        """
        Sends shutdown message to signal box and removes children.
        """
        self.send(msg, 'signal')
        self.removeChild(self.bplane)
        self.removeChild(self.subscriber)

def connectToLogger(component, logger_name):
    """
    This method is used to connect a method with a log outbox to a logger.
    """
    component.LoggerName = logger_name

    publisher = PublishTo('LOG_' + logger_name)
    graph = Graphline( COMPONENT = component,
                       PUBLISHER = publisher,
                       linkages = {
                            ('COMPONENT', 'log') : ('PUBLISHER', 'inbox'),
                            ('COMPONENT', 'signal') : ('PUBLISHER', 'control'),
                        })
    graph.activate()
    component.addChildren(publisher, graph)

if __name__ == '__main__':
    from Kamaelia.Util.Backplane import PublishTo

    class Producer(component):
        """
        A simple component to repeatedly output message.
        """
        Inboxes = {'inbox' : 'NOT USED',
                    'control' : 'receive shutdown messages',}
        Outboxes = {'outbox' : 'push data out',
                    'signal' : 'send shutdown messages',
                    'log' : 'post messages to the log'}
        def __init__(self, message):
            super(Producer, self).__init__()
            self.message = message

        def main(self):
            not_done = True
            while not_done:
                self.send(self.message, 'log')
                print 'sent %s' % (self.message)
                while self.dataReady('control'):
                    msg = self.recv('control')
                    self.send(msg, 'signal')
                    if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                        not_done = False
                        print 'Producer shutting down!'
                yield 1

            self.send(producerFinished(), 'signal')

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
            connectToLogger(self.Producer, self.logname)
            i = 0

            while i < 50:
                print 'i = ' + str(i)
                i += 1
                yield 1

            print 'SomeChassis shutting down!'
            self.send(shutdownMicroprocess(), 'signal-logger')
            self.send(shutdownMicroprocess(), 'signal-producer')


    SomeChassis(Producer = Producer('blah'), logname = 'blah.log').run()