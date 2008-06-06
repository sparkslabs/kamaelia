import inspect
import re

#
# Reuseable IShards
#

def ShutdownHandler(self):
    while self.dataReady("control"):
        cmsg = self.recv("control")
        if isinstance(cmsg, Axon.Ipc.producerFinished) or \
           isinstance(cmsg, Axon.Ipc.shutdownMicroprocess):
            self.send(cmsg, "signal")
            done = True

def LoopOverPygameEvents(self):
    while self.dataReady("inbox"):
        for event in self.recv("inbox"):
            if event.type == pygame.MOUSEBUTTONDOWN:
                exec self.getIShard("MOUSEBUTTONDOWN")
            elif event.type == pygame.MOUSEBUTTONUP:
                exec self.getIShard("MOUSEBUTTONUP")
            elif event.type == pygame.MOUSEMOTION:
                exec self.getIShard("MOUSEMOTION")

def RequestDisplay(self):
    displayservice = PygameDisplay.getDisplayService()
    self.link((self,"display_signal"), displayservice)
    self.send( self.disprequest, "display_signal")

def GrabDisplay(self):
    self.display = self.recv("callback")
