from datetime import datetime, timedelta
import time
from Axon.ThreadedComponent import threadedcomponent

class ConnectionWatcher(threadedcomponent):
    Inboxes = {
        "inbox" : "Receives data stream to watch",
        "messages" : "Receives start and stop signals to identify when to watch connections",
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
        self.started = False

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

    def main(self):
        while not self.finished():
            
            while not self.dataReady("messages") and self.started == False:
                # Wait for connection init
                data = self.recv("messages")
                if data == "start":
                    self.started = True

            lastdatatime = datetime.today()
            killed = False

            while killed == False and self.started == True:
                while self.dataReady("inbox"):
                    self.recv("inbox") # Flush the inbox
                    lastdatatime = datetime.today()
                    print ("data")

                while self.dataReady("messages"):
                    data = self.recv("messages")
                    if data == "stop":
                        self.started = False

                if (lastdatatime + timedelta(seconds=self.watchtime)) < datetime.today() and self.started == True:
                    # Execute kill operation
                    print ("killing")
                    self.handle.kill()
                    killed = True
                    self.started = False

                time.sleep(1)