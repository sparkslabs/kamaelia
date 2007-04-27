"""
Sample as to how to add in component for
Kamaelia.Community.MPS.Demo.SomeComponent
"""

import Axon

class SomeComponent(Axon.Component.component):
    def main(self):
        while 1:
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                try:
                    Length = len(data)
                except TypeError:
                    Length = 0
                self.send(Length, "outbox")
            yield 1