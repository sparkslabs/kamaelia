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
        self.currentOption = None
      
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
                    # Choose a default one initially
                    if self.currentOption is None:
                        self.currentOption = option.keys()[0]
                        data = option[self.currentOption]
                        for item in data:
                            self.send(item, "outbox")
                    
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                # If new selection is the same with current one, ignore it
                if msg and msg!=self.currentOption:
                    try:
                        data = self.options[msg]
                        self.currentOption = msg
                    except KeyError:
                        continue
                    for item in data:
                        self.send(item, "outbox")

            done = self.shutdown()


__kamaelia_components__  = ( DictChooser, )