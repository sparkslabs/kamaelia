from datetime import datetime, timedelta
import time
from Axon.ThreadedComponent import threadedcomponent

class ConnectionWatcher(threadedcomponent):
    Inboxes = {
        "inbox" : "Receives data stream to watch",
        "control" : ""
    }
    Outboxes = {
        "outbox" : "",
        "signal" : ""
    }

    def __init__(self,handle,watchtime):
        super(ConnectionWatcher, self).__init__()
        self.watchtime = watchtime
        self.handle = handle

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

    def main(self):
        while not self.finished():
            
            while not self.dataReady("inbox"):
                # Wait for connection init
                time.sleep(1)

            lastdatatime = datetime.today()
            killed = False

            while killed == False:
                while self.dataReady("inbox"):
                    self.recv("inbox") # Flush the inbox
                    lastdatatime = datetime.today()
                    print ("data")

                if (lastdatatime + timedelta(seconds=self.watchtime)) < datetime.today():
                    # Execute kill operation
                    print ("killing")
                    self.handle.kill()
                    killed = True
                    
                time.sleep(1)