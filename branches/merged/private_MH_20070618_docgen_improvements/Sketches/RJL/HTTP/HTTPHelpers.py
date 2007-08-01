# Helper classes for HTTP

from Axon.Component import component

"""HTTPMakePostRequest is used to turn messages into HTTP POST requests
for SimpleHTTPClient.
"""

class HTTPMakePostRequest(component):
    def __init__(self, uploadurl):
        super(HTTPMakePostRequest, self).__init__()
        self.uploadurl = uploadurl
        
    def main(self):
        while 1:
            yield 1
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                msg = { "url" : self.uploadurl, "postbody" : msg }
                self.send(msg, "outbox")
            
            self.pause()
