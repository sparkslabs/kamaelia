from PureTransformer import PureTransformer
    
class LineSplit(PureTransformer):
    def processMessage(self, msg):
        splitmsg = msg.split("\n")
        for line in splitmsg:
            self.send(line, "outbox")
