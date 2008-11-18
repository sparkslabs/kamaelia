from Axon.Component import component
from Axon.Ipc import producerFinished

class Killer(component):
    def main(self):
        yield 1
        self.send(producerFinished(self), 'signal')
        yield 1
        
class Killee(component):
    def main(self):
        not_done = True
        while not_done:
            for msg in self.Inbox('control'):
                if isinstance(msg, producerFinished):
                    not_done = False
                    print 'Killee dying!'
                
            if not self.anyReady() and not_done:
                self.pause()
                    
            yield 1
                    
if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import Pipeline
    
    Pipeline(Killer(), Killee()).run()