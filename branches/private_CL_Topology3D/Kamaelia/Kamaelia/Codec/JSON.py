"""\
=========================
JSON serialisation coder
=========================

This component encode data to serialisable JSON format and 
decode serialised JSON data.
"""

import cjson

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class JSONEncoder(component):
    """ Kamaelia component to encode data using JSON coding """
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
                data = self.recv("inbox")
                if data: # Ignore empty data
                    serialisedData = cjson.encode(data)
                    self.send(serialisedData, "outbox")
            
            yield 1
            
        self.send(self.shutdown_mess,"signal")
        
        
#===============================================================================
# if __name__ == "__main__":
#    from Kamaelia.Util.DataSource import DataSource
#    from Kamaelia.Util.Console import ConsoleReader,ConsoleEchoer
#    from Kamaelia.Chassis.Graphline import Graphline
#    
#    # Data can be from both DataSource and console inputs
#    Graphline(
#        CONSOLEREADER = ConsoleReader('>>>'),
#        DATASOURCE = DataSource(["['foo', {'bar': ('baz', None, 1.0, 2)}]"]),
#        JSONENCODER = JSONEncoder(),
#        CONSOLEECHOER = ConsoleEchoer(),
#    linkages = {
#        ("CONSOLEREADER","outbox") : ("JSONENCODER","inbox"),
#        ("DATASOURCE","outbox") : ("JSONENCODER","inbox"),   
#        ("JSONENCODER","outbox")  : ("CONSOLEECHOER","inbox"),     
#    }
# ).run()
#===============================================================================



class JSONDecoder(component):
    """ Kamaelia component to decode data encoded by JSON coding """
    def __init__(self):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(JSONDecoder, self).__init__()
        
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
                serialisedData = self.recv("inbox").strip()
                if serialisedData: # Ignore empty data
                    data = cjson.decode(serialisedData)
                    self.send(data, "outbox")
            
            yield 1
            
        self.send(self.shutdown_mess,"signal")

__kamaelia_components__ = ( JSONEncoder, JSONDecoder )        

        
if __name__ == "__main__":
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Util.Console import ConsoleReader,ConsoleEchoer
    from Kamaelia.Chassis.Graphline import Graphline
    
    # Data can be from both DataSource and console inputs
    Graphline(
        CONSOLEREADER = ConsoleReader('>>>'),
        DATASOURCE = DataSource([['foo', {'bar': ('baz', None, 1.0, 2)}]]),
        JSONENCODER = JSONEncoder(),
        JSONDECODER = JSONDecoder(),
        CONSOLEECHOER = ConsoleEchoer(),
    linkages = {
        ("CONSOLEREADER","outbox") : ("JSONENCODER","inbox"),
        ("DATASOURCE","outbox") : ("JSONENCODER","inbox"),
        ("JSONENCODER","outbox")  : ("JSONDECODER","inbox"), 
        ("JSONDECODER","outbox")  : ("CONSOLEECHOER","inbox"),     
    }
).run()