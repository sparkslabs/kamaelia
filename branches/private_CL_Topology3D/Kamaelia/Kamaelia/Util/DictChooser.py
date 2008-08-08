import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess

class DictChooser(Axon.Component.component):
    """ Use dictionary to choose different options instead of list in Chooser """
    
    Inboxes = { "inbox"   : "receive commands",
               "option"  : "receive options",
               "control" : "shutdown messages"
             }
    Outboxes = { "outbox" : "emits chosen items",
                "signal" : "shutdown messages"
              }
   
    def __init__(self, options = {}):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(DictChooser, self).__init__()
        self.options = dict(options)
      
    def shutdown(self):
        """
        Returns True if a shutdownMicroprocess message was received.
        """
        if self.dataReady("control"):
            message = self.recv("control")
            if isinstance(message, shutdownMicroprocess):
                self.send(message, "signal")
                return True
        return False
            
    def main(self):
        """Main loop."""
        done = False
        while not done:
            yield 1

            while self.dataReady("option"):
                option = self.recv("option")
                if option:
                    self.options.update(option)
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                if msg:
                    try:
                        data = self.options[msg]
                    except KeyError:
                        continue
                    for item in data:
                        self.send(item, "outbox")

            done = self.shutdown()