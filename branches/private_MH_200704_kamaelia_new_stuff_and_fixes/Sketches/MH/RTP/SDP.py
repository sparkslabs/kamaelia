#!/usr/bin/env python

# Basic Parser for SDP data, as defined in RFC 4566
#
# assuming the data is already split into lines
#
# ignores attribute lines to simplify parsing


from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess

import re

class SdpParser(component):

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
            type,key,value = parseline(line)

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
                    type,key,value = parseline(line)

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
                    type,key,value = parseline(line)
                    
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
                        type,key,value = parseline(line)

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
        self.send(session,"outbox")

        
def parseline(line):
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
            numports==1
        else:
            numports=int(numports)
        return type, 'media', (media,port,numports,protocol,fmt)

    else:
        return type, 'unknown', value


import sys
sys.path.append("../MobileReframe")
from OneShot import OneShot
from chunks_to_lines import chunks_to_lines
from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.Chassis.Pipeline import Pipeline

    
def GetRTPAddressFromSDP(sdp_url):
    return \
        Pipeline( OneShot(sdp_url),
                  SimpleHTTPClient(),
                  chunks_to_lines(),
                  SdpParser(),
                  PureTransformer(lambda session : \
                      (session["connection"][2], session["media"][0]["media"][1])
                  ),
                )
    


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
o=bbcrd 1140190501 1140190501 IN IP4 132.185.224.80
s=BBC ONE [H.264/AVC]
i=Multicast trial service from BBC Research & Development Copyright (c) 2006 British Broadcasting Corporation
a=x-qt-text-nam:BBC ONE [H.264/AVC]
a=x-qt-text-aut:BBC Research & Development
a=x-qt-text-cpy:Copyright (c) 2006 British Broadcasting Corporation
u=http://www.bbc.co.uk/multicast/
e=Multicast Support <multicast-tech@bbc.co.uk>
t=0 0
c=IN IP4 233.122.227.151/32
m=video 5150 RTP/AVP 33
b=AS:1200000
a=type:broadcast
a=mux:m2t

v=0


""".splitlines()
    
    Pipeline( DataSource(sdp),
              SdpParser(),
              ConsoleEchoer(),
            ).run()

    