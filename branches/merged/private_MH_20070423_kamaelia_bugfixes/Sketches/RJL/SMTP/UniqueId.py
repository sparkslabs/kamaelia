from Axon.Component import component
import os

class UniqueId(component):
    Outboxes = ["msgid"]
    def main(self):
        # unique id takes the form X.Y
        # X is the number of times this program has been shutdown/crashed or whatever + 1 (the epoch)
        # Y is the number of message ids given this epoch so far (including that one)
        
        if os.path.isfile("epoch"):
            f = open("epoch", "r")
            epoch = int(f.read())
            f.close()
        else:
            epoch = 0
            
        epoch += 1
        f = open("epoch", "w")
        f.write(str(epoch))
        f.close()
        
        strepoch = str(epoch)
        messagecount = 0
        
        while 1:
            yield 1
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                # msg should be a component instance
                self.link((self, "msgid"), (msg, "msgid"))
    
                messagecount += 1
                self.send(strepoch + "." + str(messagecount), "msgid")
                self.unlink((self, "msgid"), (msg, "msgid"))
            self.pause()
