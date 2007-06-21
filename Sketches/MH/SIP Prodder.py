#!/usr/bin/env python

# a little test program for prodding an asterisk (www.asterisk.org)
# SIP VoIP server to find out if it is prepared to support using the G722
# audio codec over RTP
#
# built to do a one off test on a temporary server on a fixed IP
# address, using a specially set up user ID on that asterisk server.


from Kamaelia.Chassis.Graphline import Graphline
from Axon.Component import component
from Kamaelia.Internet.UDP import SimplePeer
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Util.Console import ConsoleReader
import re


ADDR="172.29.144.116"
PORT="1500"
ADDR_PORT=ADDR+":"+PORT

SDP="""\
v=0
o=- 2 2 IN IP4 """+ADDR+"""
s=CounterPath eyeBeam 1.5
c=IN IP4 """+ADDR+"""
t=0 0
m=audio 27292 RTP/AVP 9 101
a=alt:1 1 : DARVMgfJ oS7HY1YQ """+ADDR+""" 27292
a=fmtp:101 0-15
a=rtpmap:9 g722/8000
a=rtpmap:101 telephone-event/8000
a=sendrecv
a=x-rtp-session-id:4E814640C4CB4CA8BAF7EF3925E286C7
"""


def indent(string, indent=16):
    return " "*indent + string.replace("\n","\n"+" "*indent)

from md5 import md5 as md5

def auth_response(FAILEDMSG,who=""):
    METHOD = re.search(r"^CSeq: +\d+ +(.+)$",FAILEDMSG, re.M).groups()[0]
    NONCE  = re.search(r'^[^-]+-Authenticate:.* nonce="([^"]+)".*$',FAILEDMSG, re.M).groups()[0]
    if who:
        WHO=who+"@"
    else:
        WHO=""
    
    while METHOD[-1] in "\n \r":
        METHOD=METHOD[:-1]

    print "***",METHOD,"***",len(METHOD)
    print "***",NONCE,"***",len(NONCE)
    print "***",WHO,"***"
    
    HA1=md5("1002:asterisk:2345").hexdigest()
    HA2=md5( METHOD+":sip:"+WHO+"r44116.rd.bbc.co.uk:5060").hexdigest()
    KD =md5( HA1 + ":"+NONCE+":" + HA2).hexdigest()

    print "***",KD,"***",len(KD)
    return KD,NONCE


class SIPEmulator(component):

    def put(self,msg):
        print
        print "SENDING:"
        print msg
        self.send(msg,"outbox")

    def get(self,*mustBegin):
        stillWaiting=True
        while stillWaiting:
            while not self.dataReady("inbox"): yield 1
            (reply,sender)=self.recv("inbox")
            print
            print indent( "RECEIVED - from "+str(sender)+" :" )
            print indent( reply )
            yield reply
            if not mustBegin:
                stillWaiting=False
            else:
                for begins in mustBegin:
                    if reply[:len(begins)] == begins:
                        stillWaiting=False
                        break
                

    def main(self):
        self.put("""\
REGISTER sip:r44116.rd.bbc.co.uk:5060 SIP/2.0
Via: SIP/2.0/UDP """+ADDR_PORT+""";branch=z9hG4bK-d87543-0e3cd74c49533619-1--d87543-;rport
Max-Forwards: 70
Contact: <sip:1002@"""+ADDR_PORT+""";rinstance=5903158cc79e5ab1>
To: "Matt Hammond"<sip:1002@r44116.rd.bbc.co.uk:5060>
From: "Matt Hammond"<sip:1002@r44116.rd.bbc.co.uk:5060>;tag=b15b6015
Call-ID: 1519ef58b26aaf77NTkyNzk0Y2ViOWFhZGZiNjI1NjkwMDE1ZjBkMmEwZDU.
CSeq: 1 REGISTER
Expires: 3600
Allow: INVITE, ACK, CANCEL, OPTIONS, BYE, REFER, NOTIFY, MESSAGE, SUBSCRIBE, INFO
User-Agent: X-Lite release 1003l stamp 30942
Content-Length: 0
""")
        #hopefully received a 401 Unauthorized
        for reply in self.get("SIP/2.0 401"): yield reply
        KD,NONCE = auth_response(reply)

        # so we now reply with the correct authorisation
        self.put("""\
REGISTER sip:r44116.rd.bbc.co.uk:5060 SIP/2.0
Via: SIP/2.0/UDP """+ADDR_PORT+""";branch=z9hG4bK-d87543-7b33fe5d6f3e5925-1--d87543-;rport
Max-Forwards: 70
Contact: <sip:1002@"""+ADDR_PORT+""";rinstance=5903158cc79e5ab1>
To: "Matt Hammond"<sip:1002@r44116.rd.bbc.co.uk:5060>
From: "Matt Hammond"<sip:1002@r44116.rd.bbc.co.uk:5060>;tag=b15b6015
Call-ID: 1519ef58b26aaf77NTkyNzk0Y2ViOWFhZGZiNjI1NjkwMDE1ZjBkMmEwZDU.
CSeq: 2 REGISTER
Expires: 3600
Allow: INVITE, ACK, CANCEL, OPTIONS, BYE, REFER, NOTIFY, MESSAGE, SUBSCRIBE, INFO
User-Agent: X-Lite release 1003l stamp 30942
Authorization: Digest username="1002",realm="asterisk",nonce="""+'"'+NONCE+'"'+""",uri="sip:r44116.rd.bbc.co.uk:5060",response="""+'"'+KD+'"'+""",algorithm=MD5
Content-Length: 0
""")

        #hopefully received a 200 OK message
        for reply in self.get("SIP/2.0 200"): yield reply

        # ok, lets try intiating a call
        self.put("""\
INVITE sip:1001@r44116.rd.bbc.co.uk:5060 SIP/2.0
Via: SIP/2.0/UDP """+ADDR_PORT+""";branch=z9hG4bK-d87543-3f1d437ac00d357c-1--d87543-;rport
Max-Forwards: 70
Contact: <sip:1002@"""+ADDR_PORT+""">
To: "1001"<sip:1001@r44116.rd.bbc.co.uk:5060>
From: "Matt Hammond"<sip:1002@r44116.rd.bbc.co.uk:5060>;tag=b009cd16
Call-ID: c94ccf3d3219c868NTkyNzk0Y2ViOWFhZGZiNjI1NjkwMDE1ZjBkMmEwZDU.
CSeq: 1 INVITE
Allow: INVITE, ACK, CANCEL, OPTIONS, BYE, REFER, NOTIFY, MESSAGE, SUBSCRIBE, INFO
Content-Type: application/sdp
User-Agent: X-Lite release 1003l stamp 30942
Content-Length: """+str(len(SDP))+"\n\n"+SDP)

        #hopefully received a 401 Unauthorized
        for reply in self.get("SIP/2.0 401"): yield reply
        KD,NONCE = auth_response(reply,"1001")

        #acknowledge the call rejection
        self.put("""\
ACK sip:1001@r44116.rd.bbc.co.uk:5060 SIP/2.0
Via: SIP/2.0/UDP """+ADDR_PORT+""";branch=z9hG4bK-d87543-d4668c1ccb7b5f2c-1--d87543-;rport
To: "1001"<sip:1001@r44116.rd.bbc.co.uk:5060>;tag=as26a25f7f
From: "Matt Hammond"<sip:1002@r44116.rd.bbc.co.uk:5060>;tag=b009cd16
Call-ID: c94ccf3d3219c868NTkyNzk0Y2ViOWFhZGZiNjI1NjkwMDE1ZjBkMmEwZDU.
CSeq: 1 ACK
Content-Length: 0
""")

        # try again with authorisation
        self.put("""\
INVITE sip:1001@r44116.rd.bbc.co.uk:5060 SIP/2.0
Via: SIP/2.0/UDP """+ADDR_PORT+""";branch=z9hG4bK-d87543-3f1d437ac00d357c-1--d87543-;rport
Max-Forwards: 70
Contact: <sip:1002@"""+ADDR_PORT+""">
To: "1001"<sip:1001@r44116.rd.bbc.co.uk:5060>
From: "Matt Hammond"<sip:1002@r44116.rd.bbc.co.uk:5060>;tag=b009cd16
Call-ID: c94ccf3d3219c868NTkyNzk0Y2ViOWFhZGZiNjI1NjkwMDE1ZjBkMmEwZDU.
CSeq: 2 INVITE
Allow: INVITE, ACK, CANCEL, OPTIONS, BYE, REFER, NOTIFY, MESSAGE, SUBSCRIBE, INFO
Content-Type: application/sdp
User-Agent: X-Lite release 1003l stamp 30942
Authorization: Digest username="1002",realm="asterisk",nonce="""+'"'+NONCE+'"'+""",uri="sip:1001@r44116.rd.bbc.co.uk:5060",response="""+'"'+KD+'"'+""",algorithm=MD5
Content-Length: """+str(len(SDP))+"\n\n"+SDP)
        
        # and lets see what teh OK response is
        #hopefully received a 200 OK message
        for reply in self.get("SIP/2.0 200","SIP/2.0 488","SIP/2.0 503"): yield reply



        def NONO():
            raise StopIteration
        for _naughty_ in self.scheduler.listAllThreads():
            if _naughty_ != self:
                _naughty_.next = NONO
        print "**************** DONE *****************"
        

Graphline( SIP = SIPEmulator(),
           UDP = SimplePeer( localaddr=ADDR, localport=int(PORT),
                             receiver_addr="r44116.rd.bbc.co.uk", receiver_port=5060
                           ),
           linkages = {
                ("SIP","outbox") : ("UDP","inbox"),
                ("UDP","outbox") : ("SIP","inbox"),
                ("SIP","signal") : ("UDP", "control"),
           }
         ).run()


