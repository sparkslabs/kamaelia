from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer

class Select(component):
    text = "SELECT %s"
    def __init__(self, *params, **argd):
        self.template = self.text % (', '.join(params))
        super(Select, self).__init__(**argd)
    def main(self):
        not_done = True
        while not_done:
            for msg in self.Inbox('inbox'):
                out = self.template % msg
                self.send(out, 'outbox')
            for msg in self.Inbox('control'):
                if isinstance(msg, shutdownMicroprocess):
                    not_done = False
                    
            if not self.anyReady() and not_done:
                self.pause()
            yield 1
                
                
if __name__ == '__main__':
    class inputter(component):
        def main(self):
            self.send({'foo' : 'bar'}, 'outbox')
            yield 1
            self.send(shutdownMicroprocess(), 'signal')
            
    Pipeline(inputter(), Select('%(foo)s'), ConsoleEchoer()).run()