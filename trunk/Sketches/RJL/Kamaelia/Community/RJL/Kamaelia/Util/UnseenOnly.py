from PureTransformer import PureTransformer
    
class UnseenOnly(PureTransformer):
    def __init__(self):
        super(UnseenOnly, self).__init__()
        self.seen = {}
        
    def processMessage(self, msg):
        if not self.seen.get(msg, False):
            self.seen[msg] = True
            return msg
