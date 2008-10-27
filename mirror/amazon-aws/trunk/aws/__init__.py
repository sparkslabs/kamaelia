class DebugMethodMixin(object):
    """A Mixin for debuging methods
    
    Also has a shortcut for checking wether shutdown is recieved on control
    """
    
    def debug(self, msg):
        """Send a debug message"""
        self.send(('debug', msg), "log")
        
    def info(self, msg):
        """Send an info message"""
        self.send(('info', msg), "log")
        
    def error(self, msg):
        """Send an error message"""
        self.send(('error', msg), "log")
        
    def shutdown(self):
        """Check for a shutdown message on control
        
        .. warning:: Don't use this if you have any other stuff coming in on
            the "control" inbox
        """
        while self.dataReady("control"):
            data = self.recv("control")
            if isinstance(data, producerFinished) or \
               isinstance(data, shutdownMicroprocess):
                self.send(data,"signal")
                return True
        return 0