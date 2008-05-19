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
        yield 1
        self.send(producerFinished(), "signal")
        return

if __name__ == "__main__":
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

    pipeline(
        DataSource( ["hello", " ", "there", " ", "how", " ", "are", " ", "you", " ", "today\r\n", "?", "!"] ),
        ConsoleEchoer()
    ).run()
