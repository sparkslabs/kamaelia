#!/usr/bin/python

import Axon
class PureFilter(Axon.Component.component):
    def __init__(self, filterfunc=None,**argd):
        super(PureFilter, self).__init__(**argd)
        if filterfunc is None:
            self.filterfunc = self.filtertest
        else:
            self.filterfunc = filterfunc

    def filtertest(self,item):
        return True

    def main(self):
        filterfunc = self.filterfunc # cache function, and makes usage clearer
        while True:
            if not self.anyReady():
                self.pause()
            yield 1
            for item in self.Inbox("inbox"):
                if filterfunc(item):
                    self.send(item, "outbox")
            if self.dataReady("control"):
                self.send(self.recv("control"), "signal")
                break

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline 
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Util.PureTransformer import PureTransformer

    Pipeline(
        DataSource([1,2,3,4,5,6]),
        PureFilter(lambda x: (x%2) == 0),
        PureTransformer(lambda x: str(x) + "\n"),
        ConsoleEchoer(),
    ).run()


