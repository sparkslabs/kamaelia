import cjson

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class JSONEncoder(component):
    def __init__(self):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(JSONEncoder, self).__init__()
        
    def shutdown(self):
        """ shutdown method: define when to shun down"""
        while self.dataReady("control"):
            message = self.recv("control")
            if isinstance(message, producerFinished) or isinstance(message, shutdownMicroprocess):
                self.shutdown_mess = message
                return True
        return False
      
    def main(self):
        """ main method: do stuff """
        
        # Put all codes within the loop, so that others can be run even it doesn't shut down
        while not self.shutdown():
            while not self.anyReady():
                self.pause()
                yield 1
    
            while self.dataReady("inbox"):
                data = self.recv("inbox").strip()
                if data: # Ignore empty data
                    serialisedData = cjson.encode(data)
                    self.send(serialisedData, "outbox")
            
            yield 1
            
        self.send(self.shutdown_mess,"signal")
        
        
if __name__ == "__main__":
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Util.Console import ConsoleReader,ConsoleEchoer
    from Kamaelia.Chassis.Graphline import Graphline
    
    # Data can be from both DataSource and console inputs
    Graphline(
        CONSOLEREADER = ConsoleReader('>>>'),
        DATASOURCE = DataSource(["['foo', {'bar': ('baz', None, 1.0, 2)}]"]),
        JSONENCODER = JSONEncoder(),
        CONSOLEECHOER = ConsoleEchoer(),
    linkages = {
        ("CONSOLEREADER","outbox") : ("JSONENCODER","inbox"),
        ("DATASOURCE","outbox") : ("JSONENCODER","inbox"),   
        ("JSONENCODER","outbox")  : ("CONSOLEECHOER","inbox"),     
    }
).run()