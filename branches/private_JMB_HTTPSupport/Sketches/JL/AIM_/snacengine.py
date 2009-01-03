#! /usr/bin/env python

"""\
NOTE: A "byte" in the following documentation refers to an ASCII char, an
unsigned char in C.

OSCAR messages are transmitted in discrete units called FLAPs. Don't ask me what
this stands for -- nobody save AOL really knows. FLAPs take the following form:
|----------------|
|FLAP-header     |
|----------------|
| ------------   |
||FLAP payload|  |
| ------------   |
|----------------|

Many times the payload is a SNAC, which has a structure of its own. Here is the
structure of a SNAC:

|------------------------|
|SNAC-header             |
|  Family -- 2 bytes     |
|  Subtype -- 2 bytes    |
|  Request ID -- 2 bytes |
|  Flags -- 4 bytes      |
|------------------------
|  --------------        |
| | SNAC payload |       |
|  --------------        |
|------------------------|

There are many different SNACs. For example, family 0x04, subtype 0x07
(henceforth referred to as (04, 07)),carries AIM messages from the server
to the client. A client sends SNAC (01, 11) to tell the server its idle time.
All SNAC payloads must follow a prescribed format, a format unique to each
particular type. However all SNAC headers follow the format described above.
All FLAPs containing SNACs are sent through Channel 2. Channels are handled in
the FLAP header. Abstractions exist both to handle the formation of a SNAC and
the formation of a FLAP. However, at times there are long sequences of SNACs
exchanged, and all we are really interested in is the SNAC payload, and maybe
the family and subtype, just so we know which SNACs we are dealing with. Also,
sometimes we have to wait for certain responses from the server, and it gets
unwieldy to keep having to type ::
    while not self.dataReady():
        yield 1
    goOnWithLife()

SNACEngine exists to handle request/response-type SNAC exchanges. It supports a
"sendout" method that, given the family, subtype, and snac body, automatically
handles the making of a SNAC and the channel the SNAC is to be sent on. It also
takes arguments for specifying which SNAC we should be expecting back from the
server, which SNAC we should send back as a reply, and a function that we should
run the server message through to get our reply.

It also supports a "putwait" method that a snac (fam, sub) pair to wait for, a
(fam, sub) response type, and a function to run the server SNAC body through to
obtain the response SNAC body. 

=====================
How to use
=====================

Subclass it and override the main method. An example exists in login.py, in this
directory.

=====================
Future development
=====================
Get rid of sendout. Keep putwait and sendSNAC. 

"""


from oscarutil import *
from Axon.Component import component
from Axon.Ipc import WaitComplete, shutdownMicroprocess
from Kamaelia.Internet.TCPClient import TCPClient

CHANNEL_SNAC = 2

class SNACEngine(component):
    """specialized component for sending sequences of SNACs. Standard inbox/outboxes. Base class.\
    'inbox' is for communicating with AIM, via OSCARClient or OSCARProtocol."""
    def __init__(self):
        super(SNACEngine, self).__init__()
        self.waiting = {}
        self.versionNumber = 1
        self.reqid = 2
        debugSections = {"SNACEngine.main" : 5,
                         "SNACEngine.handleAIMMessage" : 5,
                         "SNACEngine.sendSNAC" : 5,
                         }
        self.debugger.addDebug(**debugSections)

    def main(self):
        """stub method, to be overwritten"""
        pass

    def sendSNAC(self, fam, sub, s_body):
        self.send((CHANNEL_SNAC, SNAC(fam, sub, s_body, id=self.reqid)))
        self.reqid += 1
        assert self.debugger.note("SNACEngine.sendSNAC", 5, "sent (%s, %s)" % (fam, sub))

    def putwait(self, famsub, sendback=None, postrecv=(lambda self, x: None)):
        self.waiting[famsub] = (sendback, postrecv)

    def handleAIMMessage(self, flapbody):
        """when a SNAC from OSCARProtocol is received, this method checks to see if the
        SNAC is one we have been waiting for. If so, we then apply the stored method to the response.
        Then we check if we should send a reply back to the server. If so, then we SNACify the
        result of the postrecv function and send it back to the server. """
        s_header, s_body = readSNAC(flapbody)
        assert self.debugger.note("SNACEngine.handleAIMMessage", 5, "received (%s, %s)" % (s_header[0], s_header[1]))
        sendbackData= self.waiting.get((s_header[0], s_header[1]))
        if sendbackData:
            sendback, postrecv = sendbackData
            reply_s_body = postrecv(self, s_body)
            if sendback:
                self.sendSNAC(sendback[0], sendback[1], reply_s_body)
                assert self.debugger.note("SNACEngine.handleAIMMessage", 5, "sent back (%s, %s)" % sendback)
            del(self.waiting[(s_header[0], s_header[1])])


class ServerEmulator(component):
    def main(self):
        prefix = '/home/jlei/aim/snacs/'
        for name in ['ack1', '0103', '0118', '0113', '0107']:
            yield 1
            data = open(prefix+name).read()
            self.send(data)

