import Kamaelia.Util.Log as Log
from Kamaelia.Util.Backplane import PublishTo
from Axon.Component import component
import Axon.Ipc as Ipc

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
        self.write_buffer = []

        Log.connectToLogger(self, log_name)

    def write(self, str):
        lines = str.splitlines(True)  #keep newlines on end of each line
        self.write_buffer.extend(lines)

    def writelines(self, seq):
        self.write_buffer.extend(seq)

    def flush(self):
        for line in self.write_buffer:
            self.send(self.write_buffer.pop(0), 'log')

    def main(self):
        not_done = True
        while not_done:
            while self.dataReady('control'):
                msg = self.recv('control')
                self.send(msg, 'signal')
                if isinstance(msg, Ipc.shutdownMicroprocess):
                    not_done = False
            yield 1

            self.flush()



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
