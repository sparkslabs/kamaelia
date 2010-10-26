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
        self.netPrintln("%s %s HTTP/%s" % (self.method, self.url, self.url))
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

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Util.PureTransformer import PureTransformer
    from Kamaelia.Internet.TCPClient import TCPClient
    import pprint
    
    if 1:
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
raw_buffers = ["hello", "world", "this\nis a", "line and this", "s another\n"]
line, raw_buffers = get_line(raw_buffers)
print line


i
line_buffer
raw_buffers
"""

