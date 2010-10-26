#! /usr/bin/python
# -*- coding: utf-8 -*-

# Interface to Twitter streaming API
# - Grabs JSON data based on chosen keywords
# - Currently also relays PIDs - this really needs moving elsewhere
# TODO: Add watching for in-stream rate limiting / error messages
# - Doesn't currently honour tweet deletion messages (TODO)

import time
import urllib2
import urllib
import sys
from datetime import datetime
#import os
#import cjson
import socket
from Axon.Ipc import producerFinished, shutdownMicroprocess
from threading import Timer
import Axon
import httplib

#import oauth2 as oauth # TODO - Not fully implemented: Returns 401 unauthorised at the moment
#import urlparse

from Axon.ThreadedComponent import threadedcomponent

class TwitterStream(threadedcomponent):
    Inboxes = {
        "inbox" : "Receives lists containing keywords and PIDs - [[pid,pid],[keyword,keyword,keyword]]", # This docstring looks the wrong way round based on code...
        "control" : ""
    }
    Outboxes = {
        "outbox" : "Sends out received tweets in the format [tweetjson,[pid,pid]]",
        "signal" : "",
    }

    def __init__(self, username, password, proxy = False, reconnect = False, timeout = 120):
        super(TwitterStream, self).__init__()
        self.proxy = proxy
        self.username = username
        self.password = password
        # Reconnect on failure?
        self.reconnect = reconnect
        # In theory this won't matter, but add a timeout to be safe anyway
        self.timeout = timeout
        socket.setdefaulttimeout(self.timeout)
        self.backofftime = 1

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

    def main(self):
        twitterurl = "http://stream.twitter.com/1/statuses/filter.json"

        # Configure authentication for Twitter - temporary until OAuth implemented
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, twitterurl, self.username, self.password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)

        # Configure proxy and opener
        if self.proxy:
            proxyhandler = urllib2.ProxyHandler({"http" : self.proxy})
            twitopener = urllib2.build_opener(proxyhandler, authhandler)
        else:
            twitopener = urllib2.build_opener(authhandler)

        while not self.finished():
            if self.dataReady("inbox"):

                # Receive keywords and PIDs
                recvdata = self.recv("inbox")
                keywords = recvdata[0]

                # Abide by Twitter's keyword limit of 400
                if len(keywords) > 400:
                    sys.stderr.write('TwitterStream keyword list too long - sending shortened list')
                    keywords = keywords[0:400:1]
                    
                pids = recvdata[1]

                # Create POST data
                data = urllib.urlencode({"track": ",".join(keywords)})
                print ("Got keywords: " + data)

                # If using firehose, filtering based on keywords will be carried out AFTER grabbing data
                # This will be done here rather than by Twitter

                # Get ready to grab Twitter data
                urllib2.install_opener(twitopener)
                
                # Identify the client and add a keep alive message using the same timeout assigned to the socket
                headers = {'User-Agent' : "BBC R&D Grabber", "Keep-Alive" : self.timeout, "Connection" : "Keep-Alive"}

                # Connect to Twitter
                try:
                    req = urllib2.Request(twitterurl,data,headers)
                    conn1 = urllib2.urlopen(req,None,self.timeout)
                    self.backofftime = 1 # Reset the backoff time
                    print (str(datetime.utcnow()) + " Connected to twitter stream. Awaiting data...")
                except httplib.BadStatusLine, e:
                    sys.stderr.write('TwitterStream BadStatusLine error: ' + str(e) + '\n')
                    # General network error assumed - short backoff
                    self.backofftime += 1
                    if self.backofftime > 16:
                        self.backofftime = 16
                    conn1 = False
                except urllib2.HTTPError, e:
                    sys.stderr.write('TwitterStream HTTP error: ' + str(e.code) + '\n')
                    sys.stderr.write('TwitterStream HTTP error: See http://dev.twitter.com/pages/streaming_api_response_codes \n')
                    # Major error assumed - long backoff
                    if e.code > 200:
                        if self.backofftime == 1:
                            self.backofftime = 10
                        else:
                            self.backofftime *= 2
                        if self.backofftime > 240:
                            self.backofftime = 240
                    conn1 = False
                except urllib2.URLError, e:
                    sys.stderr.write('TwitterStream URL error: ' + str(e.reason) + '\n')
                    # General network error assumed - short backoff
                    self.backofftime += 1
                    if self.backofftime > 16:
                        self.backofftime = 16
                    conn1 = False
                except socket.timeout, e:
                    sys.stderr.write('TwitterStream socket timeout: ' + str(e) + '\n')
                    # General network error assumed - short backoff
                    self.backofftime += 1
                    if self.backofftime > 16:
                        self.backofftime = 16
                    conn1 = False

                if conn1:
                    # While no new keywords have been passed in...
                    while not self.dataReady("inbox"):
                        # Collect data from the streaming API as it arrives - separated by carriage returns.
                        try:
                            content = ""
                            # Timer attempt to fix connection hanging
                            # Could possibly force this to generate an exception otherwise - can't be sure if that will stop the read though
                            readtimer = Timer(self.timeout,conn1.close)
                            readtimer.start()
                            while not "\r\n" in content: # Twitter specified watch characters - readline doesn't catch this properly
                                content += conn1.read(1)
                            readtimer.cancel()
                            # Below modified to ensure reconnection is attempted if the timer expires
                            if "\r\n" in content:
                                self.send([content,pids],"outbox") # Send to data collector / analyser rather than back to requester
                                failed = False
                            else:
                                failed = True
                        except IOError, e:
                            sys.stderr.write('TwitterStream IO error: ' + str(e) + '\n')
                            failed = True
                        except Axon.AxonExceptions.noSpaceInBox, e:
                            # Ignore data - no space to send out
                            sys.stderr.write('TwitterStream no space in box error: ' + str(e) + '\n')
                            failed = True
                        except socket.timeout, e:
                            sys.stderr.write('TwitterStream socket timeout: ' + str(e) + '\n')
                            # General network error assumed - short backoff
                            self.backofftime += 1
                            if self.backofftime > 16:
                                self.backofftime = 16
                            failed = True
                        except TypeError, e:
                            # This pretty much means the connection failed - so let's deal with it
                            sys.stderr.write('TwitterStream TypeError - conn1 failure: ' + str(e) + '\n')
                            failed = True
                        if failed == True and self.reconnect == True:
                            # Reconnection procedure
                            print (str(datetime.utcnow()) + " Streaming API connection failed.")
                            conn1.close()
                            if self.backofftime > 1:
                                print ("Backing off for " + str(self.backofftime) + " seconds.")
                            time.sleep(self.backofftime)
                            print (str(datetime.utcnow()) + " Attempting reconnection...")
                            try:
                                urllib2.install_opener(twitopener)
                                req = urllib2.Request(twitterurl,data,headers)
                                conn1 = urllib2.urlopen(req,None,self.timeout)
                                self.backofftime = 1
                                print (str(datetime.utcnow()) + " Connected to twitter stream. Awaiting data...")
                            except httplib.BadStatusLine, e:
                                sys.stderr.write('TwitterStream BadStatusLine error: ' + str(e) + '\n')
                                # General network error assumed - short backoff
                                self.backofftime += 1
                                if self.backofftime > 16:
                                    self.backofftime = 16
                                conn1 = False
                                # Reconnection failed - must break out and wait for new keywords
                                break
                            except urllib2.HTTPError, e:
                                sys.stderr.write('TwitterStream HTTP error: ' + str(e.code) + '\n')
                                sys.stderr.write('TwitterStream HTTP error: See http://dev.twitter.com/pages/streaming_api_response_codes \n')
                                # Major error assumed - long backoff
                                if e.code > 200:
                                    if self.backofftime == 1:
                                        self.backofftime = 10
                                    else:
                                        self.backofftime *= 2
                                    if self.backofftime > 240:
                                        self.backofftime = 240
                                conn1 = False
                                # Reconnection failed - must break out and wait for new keywords
                                break
                            except urllib2.URLError, e:
                                sys.stderr.write('TwitterStream URL error: ' + str(e.reason) + '\n')
                                # General network error assumed - short backoff
                                self.backofftime += 1
                                if self.backofftime > 16:
                                    self.backofftime = 16
                                conn1 = False
                                # Reconnection failed - must break out and wait for new keywords
                                break
                            except socket.timeout, e:
                                sys.stderr.write('TwitterStream socket timeout: ' + str(e) + '\n')
                                # General network error assumed - short backoff
                                self.backofftime += 1
                                if self.backofftime > 16:
                                    self.backofftime = 16
                                conn1 = False
                                # Reconnection failed - must break out and wait for new keywords
                                break
                    print (str(datetime.utcnow()) + " Disconnecting from twitter stream.")
                    if conn1:
                        conn1.close()
                    if self.backofftime > 1:
                        print ("Backing off for " + str(self.backofftime) + " seconds.")
                        time.sleep(self.backofftime)

from Axon.Component import component
import Axon

class HTTPClientRequest(component):
    url = "/Components.html"
    host = "www.kamaelia.org"
    method = "GET"
    postbody = None
    headers = {}
    proto = "1.0" # Since we only accept 1.0 style responses properly
    def netPrintln(self, line):
        self.send(line + "\r\n", "outbox")
    def main(self):
        headers = dict(self.headers)
        self.netPrintln("%s %s HTTP/%s" % (self.method, self.url, self.proto))
        if self.postbody:
            headers["Content-Length"] = len(self.postbody)
        if self.host:
            headers["Host"] = self.host
        for header in headers:
            self.netPrintln("%s: %s" % (header, headers[header]) )
        self.netPrintln("")
        if self.postbody:
            self.send(self.postbody, "outbox")
        yield 1
        self.send(Axon.Ipc.producerFinished(), "signal")

class ShutdownNow(Exception):
    pass

class HTTPClientResponseHandler(component):
    suppress_header = False
    def get_line(self, raw_buffers):
        for chunk in self.Inbox("inbox"):
            raw_buffers.append(chunk)

        if raw_buffers:
            eol = "\r\n"
            len_eol = len(eol)
            line_buffer = []
            i = 0
            found_line = True
            for raw_buffer in raw_buffers:
                if eol not in raw_buffer:
                    line_buffer.append(raw_buffer)
                else:
                    where = raw_buffer.find(eol)
                    line = raw_buffer[:where]
                    rest = raw_buffer[where+len_eol:]
                    line_buffer.append(line)
                    if rest:
                        raw_buffers[i] = rest
                        break
                    else:
                        i += 1
                        break
                i += 1
            else:
                found_line = False

            if not found_line:
                line = None
            else:
                raw_buffers =  raw_buffers[i:]
                line = "".join(line_buffer)

            return line, raw_buffers
        else:
            return None, raw_buffers

    def checkControl(self):
        if self.dataReady("control"):
            self.control_message = self.recv("control")
            if isinstance(self.control_message, Axon.Ipc.shutdownMicroprocess):
                raise Exception("ShutdownNow")
            return self.control_message

    def main(self):
        self.control_message = None
        try:
            input_buffer = []
            line_buffer = None
            line = None
            while not line:
                if not self.anyReady():
                    self.pause()
                yield 1
                line, input_buffer = self.get_line(input_buffer) # Flushes Inbox
                self.checkControl()

            if self.control_message and input_buffer == [] and not self.dataReady("inbox"):
                raise ShutdownNow

            if line:
                split_response = line.split()
                if len(split_response) == 3:
                    proto_ver, status_code, status_message = split_response
                    proto, ver = proto_ver.split("/")
                else:
                    raise Exception("Broken Web Server")

                if status_code != "200":
                    raise Exception("Failure Status",status_code,status_message)

                header = {}

                while True:
                    yield 1
                    header_line, input_buffer = self.get_line(input_buffer)
                    if header_line is not None:
                        if header_line == "":
                            break
                        w = header_line.find(":")
                        header_field = header_line[:w]
                        header_value = header_line[w+2:]
                        try:
                            header[header_field].append(header_value)
                        except KeyError:
                            header[header_field]= [header_value]

                header["HTTPSTATUSCODE"] = status_code
                header["HTTPSTATUSMESSAGE"] = status_message
                header["HTTP_SERVER_VERSION"] = ver
                header["HTTP_PROTOCOL"] = proto

                if not self.suppress_header:
                    self.send(("header", header), "outbox")

                if self.control_message and input_buffer == [] and not self.dataReady("inbox"):
                    raise ShutdownNow

            while True:
                yield 1
                for chunk in input_buffer:
                    if not self.suppress_header:
                        self.send(("body", chunk), "outbox")
                    else:
                        self.send(chunk, "outbox")

                input_buffer = []

                for chunk in self.Inbox():
                    if not self.suppress_header:
                        self.send(("body", chunk), "outbox")
                    else:
                        self.send(chunk, "outbox")

                    if not self.suppress_header:
                        self.send(("body", chunk), "outbox")
                    else:
                        self.send(chunk, "outbox")

                self.checkControl()
                if self.control_message:
                    break
                
        except ShutdownNow:
            pass

        if self.control_message:
            self.send(self.control_message, "signal")
        else:
            self.send(Axon.Ipc.producerFinished(), "signal")

class LineFilter(component):
    eol = "\n"
    def checkControl(self):
        if self.dataReady("control"):
            self.control_message = self.recv("control")
            if isinstance(self.control_message, Axon.Ipc.shutdownMicroprocess):
                raise Exception("ShutdownNow")
            return self.control_message
        
    def get_line(self, raw_buffers):
        for chunk in self.Inbox("inbox"):
            raw_buffers.append(chunk)

        if raw_buffers:
            eol = self.eol
            len_eol = len(eol)
            line_buffer = []
            i = 0
            found_line = True
            for raw_buffer in raw_buffers:
                if eol not in raw_buffer:
                    line_buffer.append(raw_buffer)
                else:
                    where = raw_buffer.find(eol)
                    line = raw_buffer[:where]
                    rest = raw_buffer[where+len_eol:]
                    line_buffer.append(line)
                    if rest:
                        raw_buffers[i] = rest
                        break
                    else:
                        i += 1
                        break
                i += 1
            else:
                found_line = False

            if not found_line:
                line = None
            else:
                raw_buffers =  raw_buffers[i:]
                line = "".join(line_buffer)

            return line, raw_buffers
        else:
            return None, raw_buffers

    def main(self):
        self.control_message = None
        input_buffer = []
        try:
            while True:
                yield 1
                line = True
                while line:
                    line, input_buffer = self.get_line(input_buffer)
                    if line:
                        self.send(line, "outbox")

                self.checkControl()
                if self.control_message and input_buffer == [] and not self.dataReady("inbox"):
                    # No more data to read, etc, so shutdown
                    raise ShutdownNow

        except ShutdownNow:
            pass
        if self.control_message:
            self.send(self.control_message, "signal")
        else:
            self.send(Axon.Ipc.producerFinished(), "signal")

import base64
def http_basic_auth_header(username, password):
    userpass = "%s:%s" % (username, password)
    base64_userpass = base64.b64encode(userpass )
    auth_value = "Basic %s" % base64_userpass
    return ("Authorization", auth_value)

def parse_url(fullurl):
    p = fullurl.find(":")
    proto = fullurl[:p]
    if proto.lower() != "http":
         raise ValueError("Can only handle http urls. You provided"+fullurl)
    if fullurl[p+1:p+3] != "//":
         raise ValueError("Invalid HTTP URL."+fullurl)
    fullurl = fullurl[p+3:]

    p = fullurl.find("/")
    if p == -1:
        server = fullurl
        path = "/"
    else:
        server = fullurl[:p]
        path = fullurl[p:]

    p = server.find(":")
    if p == -1:
        host = server
        port = 80
    else:
        host = server[:p]
        port = int(server[p+1:])

    return proto, host, port, path

from Kamaelia.Util.Console import ConsoleEchoer
def HTTPDataStreamingClient(fullurl, method="GET", body=None, headers={}, username=None, password=None, proxy=None):
    # NOTE: username not supported yet
    # NOTE: password not supported yet
 
    headers = dict(headers)
    proto, host, port, path = parse_url(fullurl)
    if username is not None and password is not None:
        (header_field, header_value) = http_basic_auth_header(username, password)
        headers[header_field] = header_value

    if proxy != None:
        request = fullurl
        _, req_host , req_port, _ = parse_url(proxy)
    else:
        request = path
        req_host , req_port = host, port

    return Pipeline(
                    HTTPClientRequest(url=request, host=host, method=method, postbody=body, headers=headers),
                    TCPClient(req_host, req_port, wait_for_serverclose=True),
                    HTTPClientResponseHandler(suppress_header = True),
                   )

if __name__ == "__main__":

    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Util.PureTransformer import PureTransformer
    from Kamaelia.Internet.TCPClient import TCPClient
    import pprint
    import os

    try:
        proxy = os.environ["http_proxy"]
    except KeyError:
        print "Not using a proxy. If you want to use a proxy, you need to do something like this"
        print "export http_proxy=http://www-cache.your.site.com:3128/"
        proxy = None
    
    try:
        username = os.environ["TWITTERUSERNAME"]
        password =  os.environ["TWITTERPASSWORD"]
    except KeyError:
        username = None
        password =  None

    if 1:
#        URL = "http://www.kamaelia.org/Home.html"
        URL = "http://stream.twitter.com/1/statuses/filter.json"

        headers = {
            "Accept-Encoding": "identity",
            "Keep-Alive": "120",
            "Connection": "close",
            "User-Agent": "BBC R&D Grabber",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        import cjson
        import simplejson

        Pipeline(
            HTTPDataStreamingClient(URL,proxy=proxy,
                                        username=username,
                                        password=password,
                                        headers = headers,
                                        method="POST",
                                        body="track=psychic+octopus%2Cbonfire+night%2Ctimes+paywall"),
#            LineFilter(eol="\r\n"),
#            ConsoleEchoer(forwarder=True, use_repr=True),
#            PureTransformer(lambda x: "TWEET: "+ str(cjson.decode(x))+"\n"), # wierd decode errors ...
#            PureTransformer(lambda x: "TWEET: "+ str(simplejson.loads(x))+"\n"),
            ConsoleEchoer()
        ).run()


    if 0:
        Pipeline(
            HTTPClientRequest(),
            TCPClient("www.kamaelia.org", 80, wait_for_serverclose=True),
            HTTPClientResponseHandler(suppress_header = True),
#            LineFilter(eol="\n"),
#            PureTransformer(lambda x: "=="+x+"\n"),
            ConsoleEchoer()
        ).run()

    if 0:
        Pipeline(
            HTTPClientRequest(),
            TCPClient("www.kamaelia.org", 80, wait_for_serverclose=True),
            HTTPClientResponseHandler(suppress_header = True),
            PureTransformer(lambda x: pprint.pformat(x)+"\n"),
            ConsoleEchoer()
        ).run()

    if 0:
        Pipeline(
            HTTPClientRequest(),
            TCPClient("www.kamaelia.org", 80, wait_for_serverclose=True),
            HTTPClientResponseHandler(),
            PureTransformer(lambda (x,y): repr((x,len(y)))+"\n"),
            ConsoleEchoer()
        ).run()

    if 0:
        Pipeline(
            HTTPClientRequest(),
            TCPClient("www.kamaelia.org", 80, wait_for_serverclose=True),
            ConsoleEchoer()
        ).run()

"""
Extensions still required
     -- Post of a body
     -- Better handling of sending of headers
     -- headers are currently key: value, should be key: [list of values], since HTTP headers may be repeated
     -- UserAgent wrapper
     -- Accept-Encoding header
     
Handles streamed response happily though, so in many respects "minor" details to
handle Needs to handle connecting to a proxy and sending full request there instead,
but that's an element of the prefab function for this anyway.

00000000  50 4f 53 54 20 68 74 74  70 3a 2f 2f 73 74 72 65  |POST http://stre|
00000010  61 6d 2e 74 77 69 74 74  65 72 2e 63 6f 6d 2f 31  |am.twitter.com/1|
00000020  2f 73 74 61 74 75 73 65  73 2f 66 69 6c 74 65 72  |/statuses/filter|
00000030  2e 6a 73 6f 6e 20 48 54  54 50 2f 31 2e 31 0d 0a  |.json HTTP/1.1..|
00000040  41 63 63 65 70 74 2d 45  6e 63 6f 64 69 6e 67 3a  |Accept-Encoding:|
00000050  20 69 64 65 6e 74 69 74  79 0d 0a 43 6f 6e 74 65  | identity..Conte|
00000060  6e 74 2d 4c 65 6e 67 74  68 3a 20 32 33 0d 0a 48  |nt-Length: 23..H|
00000070  6f 73 74 3a 20 73 74 72  65 61 6d 2e 74 77 69 74  |ost: stream.twit|
00000080  74 65 72 2e 63 6f 6d 0d  0a 4b 65 65 70 2d 41 6c  |ter.com..Keep-Al|
00000090  69 76 65 3a 20 31 32 30  0d 0a 43 6f 6e 6e 65 63  |ive: 120..Connec|
000000a0  74 69 6f 6e 3a 20 63 6c  6f 73 65 0d 0a 55 73 65  |tion: close..Use|
000000b0  72 2d 41 67 65 6e 74 3a  20 42 42 43 20 52 26 44  |r-Agent: BBC R&D|
000000c0  20 47 72 61 62 62 65 72  0d 0a 43 6f 6e 74 65 6e  | Grabber..Conten|
000000d0  74 2d 54 79 70 65 3a 20  61 70 70 6c 69 63 61 74  |t-Type: applicat|
000000e0  69 6f 6e 2f 78 2d 77 77  77 2d 66 6f 72 6d 2d 75  |ion/x-www-form-u|
000000f0  72 6c 65 6e 63 6f 64 65  64 0d 0a 41 75 74 68 6f  |rlencoded..Autho|
00000100  72 69 7a 61 74 69 6f 6e  3a 20 42 61 73 69 63 20  |rization: Basic |
00000110  XX XX XX XX XX XX XX XX  XX XX XX XX XX XX XX XX  |XXXXXXXXXXXXXXXX|
00000120  XX XX XX XX XX XX XX XX  0d 0a 0d 0a 74 72 61 63  |XXXXXXXX....trac|
00000130  6b 3d 53 61 72 61 68 2b  4a 61 6e 65 25 32 43 43  |k=Sarah+Jane%2CC|
00000140  42 42 43                                          |BBC|

POST http://stream.twitter.com/1/statuses/filter.json HTTP/1.1
Accept-Encoding: identity
Content-Length: 23
Host: stream.twitter.com
Keep-Alive: 120
Connection: close
User-Agent: BBC R&D Grabber
Content-Type: application/x-www-form-urlencoded
Authorization: Basic XXXXXXXXXXXXXXXXXXXXXXXXXXXx

track=Sarah+Jane%2CCBBC

HTTP/1.0 200 OK
Content-Type: application/json
Server: Jetty(6.1.25)
X-Cache: MISS from www-cache.reith.bbc.co.uk
Via: 1.1 webgw0-rth.thls.bbc.co.uk:80 (squid/2.7.STABLE6)
Connection: close


POST http://stream.twitter.com/1/statuses/filter.json HTTP/1.0
Connection: close
Host: stream.twitter.com
Accept-Encoding: identity
Content-Length: 47
Content-Type: application/x-www-form-urlencoded
Keep-Alive: 120
Authorization: Basic XXXXXXXXXXXXXXXXXXXXXX
User-Agent: BBC R&D Grabber

psychic+octopus%2Cbonfire+night%2Ctimes+paywallHTTP/1.0 406 Not Acceptable
....x....1....x....2....x....3....x....4....x..


POST http://stream.twitter.com/1/statuses/filter.json HTTP/1.1
Accept-Encoding: identity
Content-Length: 23
Host: stream.twitter.com
Keep-Alive: 120
Connection: close
User-Agent: BBC R&D Grabber
Content-Type: application/x-www-form-urlencoded
Authorization: Basic XXXXXXXXXXXXXXXXXXXXXXXXXXXx

track=Sarah+Jane%2CCBBC

POST http://stream.twitter.com/1/statuses/filter.json HTTP/1.0
Connection: close
Host: stream.twitter.com
Accept-Encoding: identity
Content-Length: 47
Content-Type: application/x-www-form-urlencoded
Keep-Alive: 120
Authorization: Basic XXXXXXXXXXXXXXXXXXXXXX
User-Agent: BBC R&D Grabber

psychic+octopus%2Cbonfire+night%2Ctimes+paywallHTTP/1.0 406 Not Acceptable

"""
