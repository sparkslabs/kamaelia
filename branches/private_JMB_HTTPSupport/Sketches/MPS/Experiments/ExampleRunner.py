#!/usr/bin/python

from Kamaelia.File.UnixProcess import UnixProcess

import Axon

class ExampleRunner(Axon.Component.component): # This is a good usecase for allowing mixins to mixin extra inboxes
    Inboxes = {
        "inbox": "-",
        "control": "-",
        "_unixprocessdone": "-",
    }

    def Inline(self, X, outbox="outbox", signal="signal", inbox="inbox", control="control"):
        def Y(X, outbox,signal,inbox,control):
            L1 = self.link((X, signal), (self, control))
            L2 = self.link((X, outbox), (self, inbox))
            X.activate()
            yield 1
            while not self.dataReady(control):
                yield 1
            self.recv(control)
            self.unlink(L1)
            self.unlink(L2)
            del X

        return Axon.Ipc.WaitComplete(Y(X,outbox,signal,inbox,control))
    
    def system(self, command):
        return self.Inline( UnixProcess(command+";sleep 0.2"), control="_unixprocessdone" )

    def main(self):
        yield self.system("ls")
        for i in self.Inbox("inbox"):
           print i

        yield self.system("fortune")
        for i in self.Inbox("inbox"):
           print i

        yield self.system("ls")
        for i in self.Inbox("inbox"):
           print i
        yield 1

if __name__ == "__main__":
    ExampleRunner().run()
