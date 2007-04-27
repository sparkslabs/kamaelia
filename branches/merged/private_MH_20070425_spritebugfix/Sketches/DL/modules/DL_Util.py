# Some Utilities useful for testing purposes

from Kamaelia.Util.Chargen import Chargen
from Axon import Component
import pickle

class SerialChargen(Chargen):
    """ Generates Hello World0, Hello World1, Hello World2, ....."""

    def main(self):
        """Main loop."""
        count = 0
        while 1:
            self.send("Hello World" + str(count), "outbox")
            count += 1
            yield 1
            

class Pickle(Component.component):

    def main(self):

        while 1:

            if self.dataReady("inbox"):

                data = self.recv("inbox")

                self.send(pickle.dumps(data), "outbox")
            yield 1

class UnPickle(Component.component):

    def main(self):

        while 1:

            if self.dataReady("inbox"):

                data = self.recv("inbox")

                self.send(pickle.loads(data), "outbox")
            yield 1


                
