from Axon.Component import component
from Kamaelia.Util.Backplane import Backplane,  SubscribeTo, PublishTo
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
            while self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, (shutdownMicroprocess)):
                    not_done = False
                    self.shutdown(msg)

            if self.dataReady('inbox'):
                file = open(self.logname, 'a')
                while self.dataReady('inbox'):
                    msg = self.recv('inbox')
                   # print 'received %s!' % (msg)
                    file.write(self.wrapper(msg))
                file.close()

            if not_done:
                self.pause()
                yield 1

        if self.dataReady('inbox'):
            file = open(self.logname, 'a')
            while self.dataReady('inbox'):
                msg = self.recv('inbox')
             #   print 'received %s!' % (msg)
                file.write(self.wrapper(msg))
            file.close()

    def shutdown(self, msg):
        """
        Sends shutdown message to signal box and removes children.
        """
        self.send(msg, 'signal')
        self.removeChild(self.bplane)
        self.removeChild(self.subscriber)

    def collectable(self, name):
        return True

def connectToLogger(component, logger_name, log_box='log'):
    """
    This method is used to connect a method with a log outbox to a logger via a
    PublishTo component.
    """
    component.LoggerName = logger_name

    publisher = PublishTo('LOG_' + logger_name)
    graph = Graphline( COMPONENT = component,
                       PUBLISHER = publisher,
                       linkages = {
                            ('COMPONENT', log_box) : ('PUBLISHER', 'inbox'),
                            ('COMPONENT', 'signal') : ('PUBLISHER', 'control'),
                        })
    graph.activate()
    component.addChildren(publisher, graph)

def createLogger(logger_name, component, signal_box_name='signal', wrapper=wrapMessage):
    """
    This is a convenience method used to create a logger, activate it, add it as
    a child to an existing component, and link its control box to the existing
    component's signal box.

    -logger_name - the name of the Logger to make
    -component - the component to connect to
    -signal_box_name - the name of component's signal box
    -wrapper - a method object that wraps a log message.
    """
    log = Logger(logger_name, wrapper)
    component.addChildren(log)
    component.link((component, signal_box_name), (log, 'control'))
    log.activate()

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
            i = 0
            while not_done:
                i += 1

                self.send(str(i), 'log')
                print 'sent %s' % (str(i))
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
