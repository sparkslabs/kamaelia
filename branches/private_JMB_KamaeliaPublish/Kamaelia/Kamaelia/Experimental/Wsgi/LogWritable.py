import Kamaelia.Util.Log as Log
from Kamaelia.Util.Backplane import PublishTo
from Axon.Component import component
import Axon.Ipc as Ipc

def GetLogWritable(log_name, component, signal_box_name = 'signal'):
    """
    This method is used to get a WsgiLogWritable that is automatically linked to
    the given signal outbox so that it can easily be shut down.

    - log_name - the name of the Kamaelia.Util.Log.Logger object to publish to
    - component - the component to control the execution of the WsgiLogWritable
    - signal_box_name - the name of the outbox of component to send shutdown
      messages from
    """
    write = WsgiLogWritable(log_name)
    component.link((component, signal_box_name), (write, 'control'))
    write.activate()
    return write

class WsgiLogWritable(component):
    """
    This component is meant to be passed to a WSGI application to be used as a
    wsgi.errrors writable.  All input that is written to it will be sent to a log
    component that will write the input to file.
    """
    Inboxes = {'inbox' : 'NOT USED',
                'control' : 'receive shutdown messages',}
    Outboxes = {'outbox' : 'NOT USED',
                'log' : 'post messages to the log',
                'signal' : 'send shutdown messages',}
    def __init__(self, log_name):
        super(WsgiLogWritable, self).__init__()
        self.write_buffer = ""
        self.log_name = log_name

    def write(self, str):
        self.write_buffer += str

    def writelines(self, seq):
        self.write_buffer += '\n'.join(seq)
        self.write_buffer += '\n'

    def flush(self):
        self.send(self.write_buffer, 'log')
        self.write_buffer = ''

    def main(self):
        Log.connectToLogger(self, self.log_name)

        not_done = True
        while not_done:
            while self.dataReady('control'):
                msg = self.recv('control')
                self.send(msg, 'signal')
                if isinstance(msg, Ipc.shutdownMicroprocess):
                    not_done = False

            if self.write_buffer:
                self.flush()

            if not_done:
                self.pause()
                yield 1

    def collectable(self, name):
        return True



if __name__ == '__main__':
    class Caller(component):
        Inboxes = {'inbox' : 'NOT USED',
                   'control' : 'NOT USED', }
        Outboxes = {'outbox' : 'NOT USED',
                    'signal' : 'send shutdown signals',
                    'signal-logger' : 'send shutdown signals to the logger'}

        def __init__(self, log_name):
            super(Caller, self).__init__()
            self.log = WsgiLogWritable(log_name)
            self.link((self, 'signal'),  (self.log, 'control'))

        def main(self):
            not_done = True
            i = 0
            ilist = []
            while not_done:
                i += 1
                print str(i)
                if not i % 3:
                    ilist.append(str(i))
                    self.log.writelines(ilist)
                    ilist = []
                else:
                    ilist.append(str(i))
                if i == 50:
                    self.log.writelines(ilist)
                    self.log.flush()
                    not_done = False
                yield 1
            self.send(Ipc.shutdownMicroprocess(), 'signal')
            self.send(Ipc.shutdownMicroprocess(), 'signal-logger')

    log_name = 'blah.log'

    logger = Log.Logger(log_name, wrapper=Log.nullWrapper)
    logger.activate()

    call = Caller(log_name)
    call.link((call, 'signal-logger'), (logger, 'control'))
    call.run()
