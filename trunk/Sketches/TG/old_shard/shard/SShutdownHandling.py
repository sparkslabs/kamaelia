
class ShutdownHandler:
    """
    Code adapted slightly from MagnaDoodle.py and moved into separate module
    Methods added back to ShardMagnaDoodle using shard wrapper function
    """
    def handleShutdown(self):
        while self.dataReady("control"):
            cmsg = self.recv("control")
            if isinstance(cmsg, producerFinished) or isinstance(cmsg, shutdownMicroprocess):
                self.send(cmsg, "signal")
                return True  # done = True