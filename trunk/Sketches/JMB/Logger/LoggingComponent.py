from Axon.Component import component
from Kamaelia.Util.Backplane import PublishTo
from Axon.Ipc import newComponent, producerFinished, shutdownMicroprocess
from Axon.Box import makeOutbox

class LoggingComponent(component):
    Inboxes = {'inbox' : 'receive data here',
               'control' : 'receive shutdown signals',}
    Outboxes = {'outbox' : 'send data here',
                'log' : 'post messages to the log here',
                'signal' : 'post shutdown messages',}
    
    def __init__(self, *args, **argd):
        super(LoggingComponent, self).__init__()
        
    def EnableLogging(self, logger_name):
        self.connectToLogger = connectToLogger(self, logger_name)
        
        
def connectToLogger(self, logger_name):
    self.publisher = PublishTo(logger_name)
    self.addChildren(self.publisher)
    
    self.link((self, 'log'), (publisher, 'inbox'))
    
    
if __name__ == '__main__':
    class Producer(LoggingComponent):
        pass
        