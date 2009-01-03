#! /usr/bin/env python
from Axon.Component import component
from Axon.Ipc import WaitComplete, shutdownMicroprocess

"""\
This component waits for messages and sends the appropriate response. Each incoming message
is processed into the format (type, body), where "type" is associated with a response. The appropriate
response is pulled out from an internal dictionary and sent out through "outbox".

The response is stored in the form of a function and a response-type. The function transforms "body".
Then a generic function takes "response-type" and the result of the first function and returns the
final form of the reply, which is sent out to "outbox".

Responder supports a "sendout" method, which takes as mandatory arguments a key and a body. It
runs the key and body through the aforementioned generic function, and sends the result off to "outbox".
"""
class Responder(component):
    def __init__(self, parseMsg, makeMsg):
        super(Responder, self).__init__()
        self.parseMsg = parseMsg
        self.makeMsg = makeMsg
        self.waiting = {}
        debugSections = {"Responder.main" : 5,
                         }
        self.debugger.addDebug(**debugSections)

    def main(self):
        """stub method, to be overwritten"""
        pass

    def sendout(self, key, body, waitForKey=None, replyKey=None, replyBody=None):
        toSend = self.makeMsg(key, body)
        self.send(toSend)
        if waitForKey:
            self.putwait(waitForKey, replyKey, replyBody)

    def putwait(self, key, replyKey, replyBody=(lambda self, x: None)):
        self.waiting[key] = (replyKey, replyBody)

    def handleMessage(self, msg):
        """when a SNAC from OSCARProtocol is received, this method checks to see if the
        SNAC is one we have been waiting for. If so, we then apply the stored method to the response.
        Then we check if we should send a reply back to the server. If so, then we SNACify the
        result of the postrecv function and send it back to the server. """
        key, body = self.parseMsg(msg)
        sendbackData = self.waiting.get(key)
        if sendbackData:
            sendback, postrecv = sendbackData
            reply_body = postrecv(self, body)
            if sendback:
                self.send(self.makeMsg(sendback, reply_body))
            del(self.waiting[key])

class SimpleResponder(Responder):
    def main(self):
        yield 1
        genericResponse = (lambda self, recvdbody: "received " + str(recvdbody))
        self.sendout("a", "a",
                     waitForKey = 1,
                     replyKey = "key1",
                     replyBody = genericResponse
                     )
        self.sendout("b", "b",
                     waitForKey = 2,
                     replyKey = "key2",
                     replyBody = genericResponse
                     )
        self.sendout("c", "c",
                     waitForKey = 3,
                     replyKey = "key3",
                     replyBody = genericResponse
                     )
        self.sendout("d", "d",
                     waitForKey = 4,
                     replyKey = "key4",
                     replyBody = genericResponse
                     )
        while True:
            yield 1
            if self.dataReady():
                self.handleMessage(self.recv())

                
class ServerEmulator(component):
    def main(self):
        for i in range(10):
            yield 1
            self.send(i)
                     
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer
Pipeline(ServerEmulator(),
         SimpleResponder((lambda x: (x, x)), (lambda a, b: "%s %s" % (str(a), str(b)))),
         ConsoleEchoer()).run()
