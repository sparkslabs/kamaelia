#!/usr/bin/env python


from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess



class Seq(component):

    def __init__(self, *sequence):
        super(Seq,self).__init__()
        self.sequence = sequence

    def main(self):
        for factory in self.sequence:
            
            if isinstance(factory,str):
                print factory
                continue
            
            comp = factory()

            self.addChildren(comp)
            comp.activate()

            linkages = [
                self.link((comp,"outbox"),(self,"outbox"),passthrough=2)
                # not linking signal-control, since we don't want downstream
                # component to terminate prematurely
            ]

            while not self.childrenDone():
                self.pause()
                yield 1

            for linkage in linkages:
                self.unlink(thelinkage=linkage)

        self.send(producerFinished(self),"signal")


    def childrenDone(self):
        """Unplugs any children that have terminated, and returns true if there are no
           running child components left (ie. their microproceses have finished)
        """
        for child in self.childComponents():
            if child._isStopped():
                self.removeChild(child)   # deregisters linkages for us

        return 0==len(self.childComponents())


__kamaelia_components__ = ( Seq, )


if __name__=="__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Misc import OneShot
    from Kamaelia.Util.Console import ConsoleEchoer

    Pipeline( Seq( "BEGIN SEQUENCE",
                   lambda : OneShot("Hello\n"),
                   lambda : OneShot("Doctor\n"),
                   lambda : OneShot("Name\n"),
                   lambda : OneShot("Continue\n"),
                   lambda : OneShot("Yesterday\n"),
                   lambda : OneShot("Tomorrow\n"),
                   "END SEQUENCE",
                 ),
              ConsoleEchoer(),
            ).run()

