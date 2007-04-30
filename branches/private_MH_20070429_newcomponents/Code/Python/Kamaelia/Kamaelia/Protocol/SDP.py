#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
"""\
==========================================
Session Description Protocol (SDP) Support
==========================================

The SDPParser component parses Session Description Protocol (see `RFC 4566`_) data
sent to it as individual lines of text (not multiline strings) and outputs a
dictionary containing the parsed session description.

.. _`RFC 4566`: http://tools.ietf.org/html/rfc4566


Example Usage
-------------

Fetch SDP data from a URL, parse it, and display the output::

    Pipeline( OneShot("http://www.mysite.com/sessiondescription.sdp"),
              SimpleHTTPClient(),
              chunks_to_lines(),
              SDPParser(),
              ConsoleEchoer(),
            ).run()

If the session description at the URL provided is this::

    v=0
    o=jdoe 2890844526 2890842807 IN IP4 10.47.16.5
    s=SDP Seminar
    i=A Seminar on the session description protocol
    u=http://www.example.com/seminars/sdp.pdf
    e=j.doe@example.com (Jane Doe)
    c=IN IP4 224.2.17.12/127
    t=2873397496 2873404696
    a=recvonly
    m=audio 49170 RTP/AVP 0
    m=video 51372 RTP/AVP 99
    a=rtpmap:99 h263-1998/90000


Then parsing will return this dictionary::

    { 'protocol_version': 0,
      'origin'     : ('jdoe', 2890844526, 2890842807, 'IN', 'IP4', '10.47.16.5'),
      'sessionname': 'SDP Seminar',
      'information': 'A Seminar on the session description protocol',
      'connection' : ('IN', 'IP4', '224.2.17.12', '127', 1),
      'time'       : [(2873397496L, 2873404696L, [])],
      'URI'        : 'http://www.example.com/seminars/sdp.pdf',
      'email'      : 'j.doe@example.com (Jane Doe)',
      'attribute'  : ['recvonly'],
      'media':
          [ { 'media'     : ('audio', 49170, 1, 'RTP/AVP', '0'),
              'connection': ('IN', 'IP4', '224.2.17.12', '127', 1)
            },
            { 'media'     : ('video', 51372, 1, 'RTP/AVP', '99'),
              'connection': ('IN', 'IP4', '224.2.17.12', '127', 1),
              'attribute' : ['rtpmap:99 h263-1998/90000']
            }
          ],
    }


    
Behaviour
---------

Send individual lines as strings to SDPParser's "inbox" inbox. SDPParser cannot
handle multiple lines in the same string.

When SDPParser receives a producerFinished() message on its "control" inbox, or
if it encounter another "v=" line then it knows it has reached the end of the
SDP data and will output the parsed data as a dictionary to its "outbox" outbox.

The SDP format does *not* contain any kind of marker to signify the end of a
session description - so SDPParser only deduces this by being told that the
producer/data source has finished, or if it encounters a "v=" line indicating
the start of another session description.

SDPParser can parse more than one session description, one after the other.

If the SDP data is malformed AssertionError, or other exceptions, may be raised.
SDPParser does not rigorously test for exact compliance - it just complains if
there are glaring problems, such as fields appearing in the wrong sections!

If a producerFinished or shutdownMicroprocess message is received on the
"control" inbox then, once any pending data at the "inbox" inbox has been
processed, this component will terminate. It will send the message on out of
its "signal" outbox.

Only if the message is a producerFinished message will it output the session
description is has been parsing. A shutdownMicroprocess message will not result
in it being output.



Format of parsed output
-----------------------

The result of parsing SDP data is a dictionary mapping descriptive names of
types to values:

 ======  ======================  ======================================================================
 Session Description
 ------------------------------------------------------------------------------------------------------
 Type    Dictionary key          Format of the value
 ======  ======================  ======================================================================
 v       "protocol_version"      version_number
 o       "origin"                ("user", session_id, session_version, "net_type", "addr_type", "addr")
 s       "sessionname"           "session name"
 t & r   "time"                  (starttime, stoptime, [repeat,repeat, ...])
                                    where repeat = (interval,duration,[offset,offset, ...])
 a       "attribute"             "value of attribute"
 b       "bandwidth"             (mode, bitspersecond)
 i       "information"           "value"
 e       "email"                 "email-address"
 u       "URI"                   "uri"
 p       "phone"                 "phone-number"
 c       "connection"            ("net_type", "addr_type", "addr", ttl, groupsize)
 z       "timezone adjustments"  [(adj-time,offset), (adj-time,offset), ...]
 k       "encryption"            ("method","value")
 m       "media"                 [media-description, media-description, ... ]
                                     see next table for media description structure
 ======  ======================  ======================================================================

Note that 't' and 'r' lines are combined in the dictionary into a single
"time" key containing both the start and end times specified in the 't' line
and a list of any repeats specified in any 'r' lines present.

The "media" key contains a list of media descriptions. Like for the overall
session description, each is parsed into a dictionary, that will contain some
or all of the following:

 ======  ======================  ======================================================================
 Media Descriptions
 ------------------------------------------------------------------------------------------------------
 Type    Dictionary key          Format of the value
 ======  ======================  ======================================================================
 m       "media"                 ("media-type", port-number, number-of-ports, "protocol", "format")
 c       "connection"            ("net_type", "addr_type", "addr", ttl, groupsize)
 b       "bandwidth"             (mode, bitspersecond)
 i       "information"           "value"
 k       "encryption"            ("method","value")
 a       "attribute"             "value of attribute"
 ======  ======================  ======================================================================

Some lines are optional in SDP. If they are not included, then the parsed output
will not contain the corresponding key.
 
The formats of values are left unchanged by the parsing. For example, integers
representing times are simply converted to integers, but the units used remain
unchanged (ie. they will not be converted to unix time units).

"""

# Basic Parser for SDP data, as defined in RFC 4566
#
# assuming the data is already split into lines
#
# ignores attribute lines to simplify parsing


from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess

import re

class SDPParser(component):
    """\
    SDPParser() -> new SDPParser component.

    Parses Session Description Protocol data (see RFC 4566) sent to its "inbox"
    inbox as individual strings for each line of the SDP data. Outputs a dict
    containing the parsed data from its "outbox" outbox.
    """

    Inboxes = { "inbox"   : "SDP data in strings, each containing a single line",
                "control" : "Shutdown signalling",
              }
    Outboxes = { "outbox" : "Parsed SDP data in a dictionary",
                 "signal" : "Shutdown signalling",
               }

    def handleControl(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg,producerFinished):
                self.shutdownMsg = msg
                raise "DONE"
            elif isinstance(msg,shutdownMicroprocess):
                self.shutdownMsg = msg
                raise "STOP"
            else:
                self.send(msg,"signal")

    def readline(self):
        while 1:
            if self.dataReady("inbox"):
                line = self.recv("inbox")
                if line != "":
                    yield line
                    return
                
            self.handleControl()
            
            self.pause()
            yield None
        

    def main(self):
        self.shutdownMsg = None

        session = {}
        mandatory = "XXX"
        try:
            for line in self.readline(): yield 1
            # self.readline() generator complete ... line now contains a line with something on it
            type,key,value = _parseline(line)

            while 1:
                # begin by parsing the session section
                session = {}
                mandatory = "vost"
                multiple_allowed = "abtr"
                single_allowed = "vosiuepcbzk"
                most_recent_t = None

                while type != "m":

                    # check to see if we've been getting SDP data, then another 'v' has come along
                    # signifying the start of a new one
                    if type=="v" and "v" not in mandatory:
                        break
                    
                    mandatory=mandatory.replace(type,"")
                    assert((type in single_allowed) or (type in multiple_allowed))
                    single_allowed=single_allowed.replace(type,"")

                    if type in multiple_allowed:
                        if type=="r":
                            assert(most_recent_t is not None)
                            most_recent_t[2].append(value)     # tag repeats into list on end of time field
                        else:
                            session[key] = session.get(key,[])
                            session[key].append(value)
                    else:
                        session[key] = value
                
                    for line in self.readline(): yield 1
                    # self.readline() generator complete ... line now contains a line with something on it
                    type,key,value = _parseline(line)

                # we've hit an 'm' so its the end of the session section
                assert(mandatory=="")
                    
                # now move onto media sections
                
                mandatory_additional=""
                if "c" in single_allowed:
                    mandatory_additional+="c"
                    
                session['media'] = []

                # do a media section
                while type=="m":
                    mandatory = "" + mandatory_additional
                    multiple_allowed = "a"
                    single_allowed = "icbk"
                    
                    media={key:value}
                    session['media'].append(media)
                    
                    for line in self.readline(): yield 1
                    # self.readline() generator complete ... line now contains a line with something on it
                    type,key,value = _parseline(line)
                    
                    while type != "m" and type != "v":
                        mandatory=mandatory.replace(type,"")
                        assert((type in single_allowed) or (type in multiple_allowed))
                        single_allowed=single_allowed.replace(type,"")
                        
                        if type in multiple_allowed:
                            media[key] = media.get(key,[])
                            media[key].append(value)
                        else:
                            media[key] = value
                    
                        for line in self.readline(): yield 1
                        # self.readline() generator complete ... line now contains a line with something on it
                        type,key,value = _parseline(line)

                    # end of media section
                    assert(mandatory=="")
                    
                # end of complete SDP file (we've hit another 'v' signifying the start of a new one)
                self.sendOutParsedSDP(session)
            
        except "DONE":
            if mandatory=="":
                self.sendOutParsedSDP(session)
            
            yield 1

        except "STOP":
            pass

        if self.shutdownMsg is None:
            self.shutdownMsg = producerFinished()

        self.send(self.shutdownMsg,"signal")

    def sendOutParsedSDP(self,session):
        # normalise it a bit first
        if "connection" in session:
            for media in session['media']:
                media['connection'] = session['connection']
                
        self.send(session,"outbox")

        
def _parseline(line):
    match = re.match("^(.)=(.*)",line)
    
    type,value = match.group(1), match.group(2)
    
    if type=="v":
        assert(value=="0")
        return type, 'protocol_version', int(value)
                
    elif type=="o":
        user,sid,ver,ntype,atype,addr = re.match("^ *(\S+) +(\d+) +(\d+) +(IN) +(IP[46]) +(.+)",value).groups()
        return type, 'origin', (user,int(sid),int(ver),ntype,atype,addr)
                
    elif type=="s":
        return type, 'sessionname', value
                
    elif type=="i":
        return type, 'information', value
                    
    elif type=="u":
        return type, 'URI', value
                    
    elif type=="e":
        return type, 'email', value
                    
    elif type=="p":
        return type, 'phone', value
                    
    elif type=="c":
        if re.match("^ *IN +IP4 +.*$",value):
            match = re.match("^ *IN +IP4 +([^/]+)(?:/(\d+)(?:/(\d+))?)? *$",value)
            ntype,atype = "IN","IP4"
            addr,ttl,groupsize = match.groups()
            if ttl is None:
                ttl=127
            if groupsize is None:
                groupsize=1
        elif re.match("^ *IN +IP6 +.*$",value):
            match = re.match("^ *IN +IP6 +([abcdefABCDEF0123456789:.]+)(?:/(\d+))? *$")
            ntype,atype = "IN","IP6"
            addr,groupsize = match.groups()
        else:
            assert(False)
        
        return type, 'connection', (ntype,atype,addr,ttl,groupsize)

    elif type=="b":
        mode,rate = \
        re.match("^ *((?:AS)|(?:CT)|(?:X-[^:]+)):(\d+) *$",value).groups()
        bitspersecond=long(rate)*1000
        return type, 'bandwidth', (mode,bitspersecond)
    
    elif type=="t":
        start,stop = [ long(x) for x in re.match("^ *(\d+) +(\d+) *$",value).groups() ]
        repeats = []
        
        return type, 'time', (start,stop,repeats)

    elif type=="r":
        terms=re.split("\s+",value)
        parsedterms = []
        for term in terms:
            value, unit = re.match("^\d+([dhms])?$").groups()
            value = long(value) * {None:1, "s":1, "m":60, "h":3600, "d":86400}[unit]
            parsedterms.append(value)
        
        interval,duration=parsedterms[0], parsedterms[1]
        offsets=parsedterms[2:]
        return type, 'repeats', (interval,duration,offsets)

    elif type=="z":
        adjustments=[]
        while value.strip() != "":
            adjtime,offset,offsetunit,value = re.match("^ *(\d+) +([+-]?\d+)([dhms])? *?(.*)$",value).groups()
            adjtime=long(adjtime)
            offset=long(offset) * {None:1, "s":1, "m":60, "h":3600, "d":86400}[offsetunit]
            adjustments.append((adjtime,offset))

        return type, 'timezone adjustments', adjustments

    elif type=="k":
        method,value = re.match("^(clear|base64|uri|prompt)(?:[:](.*))?$",value).groups()
        return type, "encryption", (method,value)

    elif type=="a":
        return type, 'attribute', value

    elif type=="m":
        media, port, numports, protocol, fmt = re.match("^(audio|video|text|application|message) +(\d+)(?:[/](\d+))? +([^ ]+) +(.+)$",value).groups()
        port=int(port)
        if numports is None:
            numports=1
        else:
            numports=int(numports)
        return type, 'media', (media,port,numports,protocol,fmt)

    else:
        return type, 'unknown', value


__kamaelia_components__ = ( SDPParser, )


if __name__ == "__main__":
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer

    sdp = """\
v=0
o=jdoe 2890844526 2890842807 IN IP4 10.47.16.5
s=SDP Seminar
i=A Seminar on the session description protocol
u=http://www.example.com/seminars/sdp.pdf
e=j.doe@example.com (Jane Doe)
c=IN IP4 224.2.17.12/127
t=2873397496 2873404696
a=recvonly
m=audio 49170 RTP/AVP 0
m=video 51372 RTP/AVP 99
a=rtpmap:99 h263-1998/90000

v=0
o=bfcrd 1140190501 1140190501 IN IP4 132.185.224.80
s=BFC ONE [H.264/AVC]
i=Multicast trial service from the BBC! Get BFC FLURBLE here!
a=x-qt-text-nam:BFC FLURBLE [H.264/AVC]
a=x-qt-text-aut:BFC Research & Development
a=x-qt-text-cpy:Copyright (c) 2006 British Flurbling Corporation
u=http://www.bbc.co.uk/multicast/
e=Multicast Support <multicast-tech@bfc.co.uk>
t=0 0
c=IN IP4 233.122.227.151/32
m=video 5150 RTP/AVP 33
b=AS:1200000
a=type:broadcast
a=mux:m2t

v=0


""".splitlines()
    
    Pipeline( DataSource(sdp),
              SDPParser(),
              ConsoleEchoer(),
            ).run()

    