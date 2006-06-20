from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess, shutdown

class DataSource(component):
    def __init__(self, messages):
        super(DataSource, self).__init__()
        self.messages = messages
        
    def main(self):
        while len(self.messages) > 0:
            yield 1
            self.send(self.messages.pop(0), "outbox")
        self.send(producerFinished(), "signal")
