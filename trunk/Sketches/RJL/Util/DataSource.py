from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown
from PureTransformer import PureTransformer

"""\
=================
Data Source component
=================

This component outputs messages specified at its creation one after another.

Example Usage
-------------

To output "hello" then "world":
pipeline(
    DataSource(["hello", "world"]),
    ConsoleEchoer()
).run()

=================
Triggered Source component
=================

Whenever this component receives a message on inbox, it outputs a certain message.

Example Usage
-------------

To output "wibble" each time a line is entered to the console.
pipeline(
    ConsoleReader(),
    TriggeredSource("wibble"),
    ConsoleEchoer()
).run()

"""

class DataSource(component):
    def __init__(self, messages):
        super(DataSource, self).__init__()
        self.messages = messages
        
    def main(self):
        while len(self.messages) > 0:
            yield 1
            self.send(self.messages.pop(0), "outbox")
        yield 1
        self.send(producerFinished(self), "signal")
        return

TriggeredSource = lambda msg : PureTransformer(lambda r : msg)

if __name__ == "__main__":
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

    pipeline(
        DataSource( ["hello", " ", "there", " ", "how", " ", "are", " ", "you", " ", "today\r\n", "?", "!"] ),
        ConsoleEchoer()
    ).run()
