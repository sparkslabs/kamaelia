#! /usr/bin/env python
##
## (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
##     All Rights Reserved.
##
## You may only modify and redistribute this under the terms of any of the
## following licenses(2): Mozilla Public License, V1.1, GNU General
## Public License, V2.0, GNU Lesser General Public License, V2.1
##
## (1) Kamaelia Contributors are listed in the AUTHORS file and at
##     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
##     not this notice.
## (2) Reproduced in the COPYING file, and at:
##     http://kamaelia.sourceforge.net/COPYING
## Under section 3.5 of the MPL, we are using this text since we deem the MPL
## notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
## notice is prohibited.
##
## Please contact us via: kamaelia-list-owner@lists.sourceforge.net
## to discuss alternative licensing.
## -------------------------------------------------------------------------

"""\
========================
Kamaelia OSCAR interface
========================
NOTE: These components implement the OSCAR protocol at the lowest level and
require a fairly good knowledge of OSCAR to use them. For a high-level
interface, see AIMHarness.py.

-   The OSCARProtocol component provides a Kamaelia interface for the FLAP level
    of OSCAR protocol. You should not be linking to OSCARProtocol directly, but
    to OSCARClient. 

-   The OSCARClient prefab returns an OSCARProtocol component wired up to a
    TCPClient.

-   SNACExchanger is the base class for all components that deal with the SNAC layer
    of OSCAR protocol. 



Explanation of Terms
------------------------
NOTE: A "byte" in the following documentation refers to an ASCII char, an
unsigned char in C.

OSCAR messages are transmitted in discrete units called FLAPs, which take the
following form::

    -------------------------------------------
    |FLAP-header                              |
    |   message start character (*) -- 1 byte |
    |   channel -- 1 byte                     |
    |   sequence number -- 2 bytes            |
    |   length of following data -- 2 bytes   |
    |-----------------------------------------|
    | ------------                            |
    ||FLAP payload|                           |
    | ------------                            |
    -------------------------------------------

The sequence number is incremented with every FLAP sent. AOL is very strict
about in-order sequence numbers and servers may even disconnect a client for not
sending the right sequence numbers. 

The majority of FLAP payloads (everything except new connection notifications,
really serious errors, shutdown notifications, and keepalives) are units called
SNACs and are transmitted over channel 2.

The structure of a SNAC::

    --------------------------
    |SNAC-header             |
    |  family -- 2 bytes     |
    |  subtype -- 2 bytes    |
    |  request ID -- 2 bytes |
    |  flags -- 4 bytes      |
    |------------------------
    |  --------------        |
    | | SNAC payload |       |
    |  --------------        |
    --------------------------

    
All SNAC payloads must follow a prescribed format unique to the particular type
of SNAC, but all SNAC headers must follow the format described above. Each
different (family, subtype) performs a different function. For example, SNAC
(04, 07) (meaning family 0x04, subtype 0x07) carries AIM messages from the server
to the client, SNAC (01, 11) reports client idle times to the server, and
(04, 06) carries a message from one user to another. 

Yet another type of OSCAR datatype is a type-length-value (TLV) unit.

The structure of a TLV::

    ------------------------------------------
    |TLV-header                              |
    |   type -- 2 bytes                      |
    |   length of following data -- 2 bytes  |
    |----------------------------------------|
    |  ---------                             |
    | |TLV data |                            |
    |  ---------                             |
    -----------------------------------------

TLVs may appear inside SNACs or just inside FLAPs. 



How does it work?
-----------------
OSCARProtocol receives messages on its "talk" inbox in (channel, flap body)
format and retransmits them to "outbox" as true FLAPs. It receives FLAPs on its
"inbox" inbox and retransmits them to its "heard" outbox in the format
(channel, flap body). It also keeps track of sequence numbers.

OSCARClient returns a Graphline with an OSCARProtocol component's inbox/outbox
connected to a TCPClient's outbox/inbox. The Graphline's inbox and outbox are l
inked to the OSCARProtocol component's "talk" and "heard" boxes, respectively.
Send (channel, flap body) tuples to its inbox and receive (channel, flap body)
tuples from the outbox.

SNACExchanger provides specialized methods for dealing with SNACs. You must
subclass it, as it does not have a main method. 



Example Usage
-------------
To get an MD5 key from the authorization server during login::

    class LoginHandler(SNACExchanger):
        def main(self):
            self.send((CHANNEL_NEWCONNECTION,
                       struct.pack('!i', 1)))
            while not self.dataReady():
                yield 1
            reply = self.recv() # server ack of new connection
            zero = struct.pack('!H', 0)
            request = TLV(0x01, "kamaelia1") + TLV(0x4b, zero) + TLV(0x5a, zero)
            self.sendSnac(0x17, 0x06, request)
            for reply in self.waitSnac(0x17, 0x07): yield 1
            md5key = reply[2:]
            print ("%02x " * len(md5key)) % unpackSingles(md5key)

    Graphline(osc = OSCARClient('login.oscar.aol.com', 5190),
              login = LoginHandler(),
              linkages = {("login", "outbox") : ("osc", "inbox"),
                          ("osc", "outbox") : ("login", "inbox"),
                          }
              ).run()

For a more complete example, see LoginHandler.py
"""
                  
          
import struct
from OscarUtil import *
from OscarUtil2 import *
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Internet.TCPClient import TCPClient


__kamaelia_components__ = (Graphline, TCPClient)

class OSCARProtocol(component):
    """\
    OSCARProtocol() -> new OSCARProtocol component.

    Provides a Kamaelia interface to the lowest level of OSCAR protocol, the
    FLAP level.

    For more information on FLAPs, see module level docs. 
    """
    Inboxes = {"inbox" : "receives binary data from the AIM server",
               "control" : "shutdown handling",
               "talk" : "receives messages in the format (channel, FLAP payload)",
               }

    Outboxes = {"outbox" : "sends binary data to the AIM server.",
                "signal" : "shutdown handling", 
                "heard" : "resends messages from 'outbox' in the form (channel, FLAP payload)",
                }
    
    def __init__(self):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(OSCARProtocol, self).__init__()
        self.seqnum = 0
        self.done = False
        self.buffer = ""
        debugSections = {"OSCARProtocol.main" : 0,
                         "OSCARProtocol.checkBoxes" : 0,
                         "OSCARProtocol.handleinbox": 0,
                         }
        self.debugger.addDebug(**debugSections)

    def main(self):
        """main loop"""
        while not self.done:
            yield 1
            self.checkBoxes()

    def checkBoxes(self):
        """checks for data in all our boxes, and if there is data, then call the
        appropriate function to handle it."""
        for box in self.Inboxes:
            if self.dataReady(box):
                cmd = "self.handle%s()" % box
                exec(cmd)

    def handleinbox(self):
        """receives data coming in through the wire, reformats it into a
        Python-friendly form, and retransmits it to its "heard" outbox."""
        data = self.recv("inbox")
        head = '!cBHH'
        while data:
            a, chan, seqnum, datalen = struct.unpack(head, data[:FLAP_HEADER_LEN])
            if len(data) < 6+datalen:
                assert self.debugger.note("OSCARProtocol.handleinbox", 1,
                                          "FLAP shorter than specified length! " +\
                                          str(datalen) + " " + str(len(data)))
                flapbody = data[FLAP_HEADER_LEN:]
                data = ""
##                self.send((chan, flapbody), "heard")
            else:
                flapbody = data[FLAP_HEADER_LEN:FLAP_HEADER_LEN+datalen]
                self.send((chan, flapbody), "heard")  
                data = data[FLAP_HEADER_LEN+datalen:]

    def handlecontrol(self):
        data = self.recv("control")
        self.done = True
        self.send(shutdownMicroprocess(), "signal")

    def handletalk(self):
        """checks that incoming messages from the "talk" inbox are in a
        (channel, flap data) tuple. If not, exceptions are raised. If so,
        OSCARProtocol.sendFLAP is called. """
        data = self.recv("talk")
        assert len(data) == 2 #we want to call this to the developer's attention if the format of things coming into "talk" isn't right.
        assert type(data[0]) == type(1)
        self.sendFLAP(data[1], data[0])

    #most of method definition from Twisted's oscar.py
    def sendFLAP(self,data,channel = 0x02):
        """constructs FLAPs and sends them"""
        header="!cBHH"
        self.seqnum=(self.seqnum+1)%0x10000
        seqnum=self.seqnum
        head=struct.pack(header,'*', channel,
                         seqnum, len(data))
        self.send(head+str(data))


def OSCARClient(server, port):
    """\
    OSCARClient(server, port) -> returns an OSCARProtocol component connected to
    a TCPClient.

    User input goes into OSCARClient's "inbox" in the form (channel, flap body)
    and useable output comes out of "outbox" in the same form. 
    """
    return Graphline(oscar = OSCARProtocol(),
                     tcp = TCPClient(server, port),
                     linkages = {
                         ("oscar", "outbox") : ("tcp", "inbox"),
                         ("tcp", "outbox") : ("oscar", "inbox"),

                         ("oscar", "signal") : ("tcp", "control"),

                         ("self", "inbox") : ("oscar", "talk"),
                         ("oscar", "heard") : ("self", "outbox"),
                         ("self", "control") : ("oscar", "control"),
                         ("tcp", "signal") : ("self", "signal"),
                         }
                     )
    
class SNACExchanger(component):
    """\
    SNACExchanger() -> component that has methods specialized for sending and
    receiving FLAPs over Channel 2 (FLAPs whose payloads are SNACs).

    For a more thorough discussion on SNACs, see module level docs. 

    """
    def __init__(self):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(SNACExchanger, self).__init__()
        debugSections = {"SNACExchanger.recvSnac" : 0,
                         "SNACExchanger.sendSnac" : 0,
                         }
        self.debugger.addDebug(**debugSections)
        
    def sendSnac(self, fam, sub, body):
        """\
        constructs a SNAC by calling self.makeSnac and sends it out the "outbox".
        """
        snac = SNAC(fam, sub, body)
        self.send((CHANNEL_SNAC, snac))
        assert self.debugger.note("SNACExchanger.sendSnac", 5, "sent SNAC " + str((fam, sub)))

    def recvSnac(self):
        """receives FLAPs containing SNACs and parses the SNAC data."""
        recvdflap = self.recv() #supported services snac
        data = readSNAC(recvdflap[1])
        assert len(data) == 2
        header, reply = data
        assert self.debugger.note("SNACExchanger.recvSnac", 5, "received SNAC" + str(header))
        return header, reply

    def waitSnac(self, fam, sub):
        """\
        Yields 1 until a SNAC of the requested family and subtype is received.
        The last value yielded is the payload of the requested SNAC.

        Usage::
            for result in self.waitSnac(family, subtype): yield 1.
            
        The body of the requested SNAC will be assigned to "result". 
        """
        done = False
        while not done:
            while not self.dataReady():
                yield 1
            header, reply = self.recvSnac()
            if header[0] == fam and header[1] == sub:
                yield reply
                done = True


if __name__ == '__main__':
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Util.PureTransformer import PureTransformer
    from Kamaelia.Chassis.Pipeline import Pipeline

    class LoginHandler(SNACExchanger):
        def main(self):
            self.send((CHANNEL_NEWCONNECTION,
                       struct.pack('!i', 1)))
            while not self.dataReady():
                yield 1
            reply = self.recv() # server ack of new connection
            zero = struct.pack('!H', 0)
            request = TLV(0x01, "kamaelia1") + TLV(0x4b, zero) + TLV(0x5a, zero)
            self.sendSnac(0x17, 0x06, request)
            for reply in self.waitSnac(0x17, 0x07): yield 1
            md5key = reply[2:]
            print ("%02x " * len(md5key)) % unpackSingles(md5key)

    Graphline(osc = OSCARClient('login.oscar.aol.com', 5190),
              login = LoginHandler(),
              linkages = {("login", "outbox") : ("osc", "inbox"),
                          ("osc", "outbox") : ("login", "inbox"),
                          }
              ).run()
