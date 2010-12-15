#! /usr/bin/python

'''
Interface to Twitter streaming API
- Grabs JSON data based on chosen keywords
- Also relays the PIDs related to the JSON responses to ensure they match up
TODO: Add watching for in-stream rate limiting / error messages
- Doesn't currently honour tweet deletion messages (TODO)
'''

import time
import urllib
import sys
import socket
from Axon.Ipc import producerFinished, shutdownMicroprocess
import Axon

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

            # First of all get wrapping HTTP response line
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

            # Then parse the HTTP response line
            if line:
                split_response = line.split(" ",2)
                if len(split_response) == 3:
                    proto_ver, status_code, status_message = split_response
                    proto, ver = proto_ver.split("/")
                else:
                    # Had less than 2 spaces in, so bust.
                    raise Exception("Broken Web Server", line)

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

            for chunk in input_buffer:
                if not self.suppress_header:
                    self.send(("body", chunk), "outbox")
                else:
                    self.send(chunk, "outbox")

            input_buffer = []
            while True:
                yield 1
                for chunk in self.Inbox():
                    if not self.suppress_header:
                        self.send(("body", chunk), "outbox")
                    else:
                        self.send(chunk, "outbox")

                self.checkControl()
                if self.control_message:
                    break

        except ShutdownNow:
            pass
        except Exception:
            pass # Trying this to ensure the program doesn't crash as easily - just encountered ('Failure Status', '504', 'Gateway Time-out')

        if self.control_message:
            self.send(self.control_message, "signal")
        else:
            self.send(Axon.Ipc.producerFinished(), "signal")

class LineFilter(component):
    eol = "\n"
    includeeol = False
    def __init__(self,**argd):
        super(LineFilter,self).__init__(**argd)
        self.input_buffer = []
        self.line_buffer = []

    def get_line(self):
        for chunk in self.Inbox("inbox"):
            self.input_buffer.append(chunk)

        if len(self.input_buffer) == 0:
            return None

        if len(self.line_buffer) > 0:
            edgecase = self.line_buffer[-1][-5:] + self.input_buffer[0][:5]
            if self.eol in edgecase:
                rawline = self.line_buffer[-1]+self.input_buffer[0]
                where = rawline.find(self.eol)
                if self.includeeol:
                    line = rawline[:where+len(self.eol)]
                else:
                    line = rawline[:where]
                rest = rawline[where+len(self.eol):]
                self.input_buffer[0] = rest
                del self.line_buffer[-1]
                result = "".join(self.line_buffer) + line
                self.line_buffer = []
                return result

        if self.eol in self.input_buffer[0]:
            where = self.input_buffer[0].find(self.eol)
            if self.includeeol:
                line = self.input_buffer[0][:where+len(self.eol)]
            else:
                line = self.input_buffer[0][:where]
            rest = self.input_buffer[0][where+len(self.eol):]
            if rest:
                self.input_buffer[0] = rest
            else:
                del self.input_buffer[0]
            result = "".join(self.line_buffer) + line
            self.line_buffer = []
            return result

        self.line_buffer.append(self.input_buffer.pop(0))
        return None

    def main(self):
        self.control_message = None
        try:
            while True:
                yield 1
                line = True
                while line:
                    line = self.get_line()
                    if line:
                        self.send(line, "outbox")

                self.checkControl()
                if self.control_message and self.input_buffer == [] and not self.dataReady("inbox"):
                    # No more data to read, etc, so shutdown
                    raise ShutdownNow

        except ShutdownNow:
            pass
        if self.control_message:
            self.send(self.control_message, "signal")
        else:
            self.send(Axon.Ipc.producerFinished(), "signal")

    def checkControl(self):
        if self.dataReady("control"):
            self.control_message = self.recv("control")
            if isinstance(self.control_message, Axon.Ipc.shutdownMicroprocess):
                raise Exception("ShutdownNow")
            return self.control_message


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

from Kamaelia.Apps.SocialBookmarks.ComponentBoxTracer import ComponentBoxTracer
from Kamaelia.Apps.SocialBookmarks.PureFilter import PureFilter
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.Internet.TCPClient import TCPClient

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

    # Leaving this here for a little while, since it is interesting/useful
    # Worth bearing in mind this next line will never execute

    return Pipeline(
                    HTTPClientRequest(url=request, host=host, method=method, postbody=body, headers=headers),
                    ComponentBoxTracer(
                        TCPClient(req_host, req_port, wait_for_serverclose=True),
                        Pipeline(
                            PureFilter(lambda x: x[0] == "outbox"),           # Only interested in data from the connection
                            PureTransformer(lambda x: x[1]),                  # Just want the data from the wire
                            PureTransformer(lambda x: base64.b64encode(x)+"\n"), # To ensure we capture data as chunked on the way in
                            SimpleFileWriter("tweets.b64.txt"),                # Capture for replay / debug
                        ),
                    ),
                    ComponentBoxTracer(
                        HTTPClientResponseHandler(suppress_header = True),
                        Pipeline(
                            PureFilter(lambda x: x[0] == "outbox"), # Only want the processed data here
                            PureTransformer(lambda x: x[1]), # Only want the raw data
                            SimpleFileWriter("tweets.raw.txt"),
                        ),
                    )
                   )


from Axon.ThreadedComponent import threadedcomponent
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Util.PureTransformer import PureTransformer

class TwitterStream(threadedcomponent):
    Inboxes = {
        "inbox" : "Receives lists containing keywords and PIDs - [[keyword,keyword,keyword],[pid,pid]]",
        "tweetsin" : "Relay for received tweets",
        "control" : ""
    }
    Outboxes = {
        "outbox" : "Sends out received tweets in the format [tweetjson,[pid,pid]]",
        "signal" : "",
    }

    def __init__(self, username, password, proxy = None, reconnect = False, timeout = 120):
        super(TwitterStream, self).__init__()
        self.proxy = proxy
        if self.proxy == False:
            self.proxy = None
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

    def connect(self,args,pids):
        self.datacapture = Graphline(
                        DATA = HTTPDataStreamingClient(self.url,proxy=self.proxy,
                                                    username=self.username,
                                                    password=self.password,
                                                    headers = self.headers,
                                                    method="POST",
                                                    body=args),
                        FILTER = LineFilter(eol="\r\n",includeeol=True), # Including EOL to pass through blank lines and help failure detection
                        TRANSFORMER = PureTransformer(lambda x: [x,pids]),
                        #ECHOER = ConsoleEchoer(),
                        linkages = {("DATA", "outbox") : ("FILTER", "inbox"),
                                    ("FILTER", "outbox") : ("TRANSFORMER", "inbox"),
                                    ("TRANSFORMER", "outbox") : ("self", "outbox"),}
                    ).activate()
        self.link((self.datacapture, "outbox"), (self, "tweetsin"))

    def main(self):
        self.url = "http://stream.twitter.com/1/statuses/filter.json"

        self.headers = {
            "Accept-Encoding": "identity",
            "Keep-Alive": self.timeout,
            "Connection": "close",
            "User-Agent": "BBC R&D Grabber",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        self.datacapture = None
        counter = 0
        blanklinecount = 0

        while not self.finished():
            if self.dataReady("inbox"):
                if self.datacapture != None:
                    self.unlink(self.datacapture)
                    self.datacapture.stop()
                    self.datacapture = None
                recvdata = self.recv("inbox")
                keywords = recvdata[0]
                if len(keywords) > 400:
                    keywords = keywords[0:400:1]

                pids = recvdata[1]

                args = urllib.urlencode({"track": ",".join(keywords)})
                print ("Got keywords:", args)

                self.connect(args,pids)
            while self.dataReady("tweetsin"):
                counter = 0
                tweetdata = self.recv("tweetsin")
                if tweetdata[0] == "\r\n":
                    blanklinkcount += 1
                else:
                    blanklinecount = 0
                self.send(tweetdata,"outbox")
                if self.dataReady("inbox"):
                    break
            if not self.dataReady("tweetsin"):
                time.sleep(1)
                if self.datacapture != None:
                    counter += 1
                else:
                    counter = 0
                # This still isn't great at reducing busy wait CPU usage
                # Blank line count ensures we reconnect if we get 10 successive keepalives with no data - likely an error
            if (counter > self.timeout and self.datacapture != None and self.reconnect) or (blanklinecount >= 10 and self.reconnect):
                blanklinecount = 0
                sys.stderr.write("API Connection Failed: Reconnecting")
                self.unlink(self.datacapture)
                self.datacapture.stop()
                self.datacapture = None
                # Twitter connection has failed
                counter = 0
                self.connect(args,pids)
                
