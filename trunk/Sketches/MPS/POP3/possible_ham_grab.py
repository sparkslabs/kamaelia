#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import time
import Axon
import sys
from Axon.Ipc import producerFinished, WaitComplete, shutdownMicroprocess
from Kamaelia.IPC import socketShutdown

from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Backplane import *


class basicPop3Client(Axon.Component.component):
    Inboxes = {
                "client_inbox" : "Data from client wanting to control pop3 connection",
                "inbox" : "Data from connection",
                "control" : "Where we recieve shutdown messages",
    }
    Outboxes = {
                "client_outbox": "Data we pass up to client wanting to control pop3 connection",
                "outbox": "Data we send to the socket",
                "signal": "Where we tell the socket to shutdown",
    }
    username = None
    password = None
    def logging_recv_connection(self):
        self.line = self.recv("inbox")

    def getline(self):
        control_message = ""
        while 1:
            while not self.anyReady():
                self.pause();
                yield 1
            while self.dataReady("control"):
                control_message = self.recv("control")
                if isinstance(control_message, socketShutdown):
                    self.client_connected = False
            if self.dataReady("inbox"):
                self.logging_recv_connection()
                return
            else:
                pass
            yield 1

    def sendCommand(self, command):
#        print "SENDING: ", command
        self.send(command + "\r\n", "outbox")

    def waitForBanner(self):
        yield WaitComplete(self.getline(), tag="_getline1")
#        print "SERVER RESPONSE", self.line
        self.banner = self.line.strip()
        
#        print repr(self.banner)
        if self.banner[:3] == "+OK":
            self.connectionSuccess = True
        else:
            self.connectionSuccess = False

    def doLogin(self, username, password):
        self.sendCommand("USER "+username)
        yield WaitComplete(self.getline(), tag="_getline2")
#        print "SERVER RESPONSE", self.line
        if self.line[:3] == "+OK":
            self.sendCommand("PASS "+ password)
            yield WaitComplete(self.getline(), tag="_getline3")
#            print "SERVER RESPONSE", self.line
            if self.line[:3] == "+OK":
                self.loggedIn = True

    def shutdown(self):
        if not self.dataReady("control"):
            return False

        self.control_message = self.recv("control")

        msg = self.control_message # alias to make next line clearer
        if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
            return True

        return False

    def headerlinesToDict(self, headers):
        headers = headers[:]
        L = []
        HEADERS = {}
        for line in headers:
           if len(line) == 0:
               continue

           if (line[0] == "\t") or (line[0]==" "):
               L.append(line.lstrip()) # add extra value
               continue
           if L != []:
               if len(L)>1:
                   HEADERS[L[0]] = L[1:]
               colonPos = line.find(":")
               header = line[:colonPos]
               value = line[colonPos+2:]
               L = [header, value]

        if len(L)>1:
            HEADERS[L[0]] = L[1:]

        return HEADERS
    

    def handleCommand(self, command):
        if command[0] == "STAT":
            self.sendCommand("STAT")
            yield WaitComplete(self.getline(), tag="_getline4")
#            print "SERVER RESPONSE", self.line
            ok, emails, boxsize = self.line.split()
            emails = int(emails)
            boxsize = int(boxsize)
            self.send( (emails, boxsize), "client_outbox")

        if command[0] == "DELE":
            net_command = "DELE %d" % (command[1],)
            self.sendCommand(net_command)
            yield WaitComplete(self.getline(), tag="_getline4")
#            print "SERVER RESPONSE", self.line
            self.send( self.line, "client_outbox")

        if command[0] == "TOP":
            net_command = "TOP %d %d" % (command[1], command[2])
            self.sendCommand(net_command)
            end_of_headers = False
            lines = []
            while not end_of_headers:
                yield WaitComplete(self.getline(), tag="_getline4")
#                print "SERVER RESPONSE", repr(self.line), "--EOL--"
                self.line = self.line.lower()
                lines.append(self.line)
                
                if "".join(lines)[-5:] == "\r\n.\r\n":
                   end_of_headers = True
            lines = ("".join(lines)).split("\r\n")
            
            headers = self.headerlinesToDict(lines[:][1:])
            self.send( headers, "client_outbox")

        if command[0] == "RETR":
            net_command = "RETR %d" % (command[1], )
            self.sendCommand(net_command)
            end_of_headers = False
            lines = []
            while not end_of_headers:
                yield WaitComplete(self.getline(), tag="_getline4")
#                print "SERVER RESPONSE", repr(self.line), "--EOL--"
#                self.line = self.line.lower()
                lines.append(self.line)
                
                if "".join(lines)[-5:] == "\r\n.\r\n":
                   end_of_headers = True
            FULLMAIL = "".join(lines)
            
            self.send( FULLMAIL, "client_outbox")


    def main(self):
        self.control_message = None
        self.connectionSuccess = False
        self.loggedIn = False

        yield WaitComplete(self.waitForBanner())

        if self.connectionSuccess:
            yield WaitComplete( self.doLogin(self.username, self.password))

            if self.loggedIn:
                run = True
                while run:
                    while not self.anyReady():
                        self.pause()
                        yield 1
                    while self.dataReady("client_inbox"):
                        command = self.recv("client_inbox")
                        yield WaitComplete(self.handleCommand(command))
                        if command[0] == "QUIT":
                           run = False

                self.sendCommand("QUIT")        
                yield WaitComplete(self.getline(), tag="_getline5")
#                print "SERVER RESPONSE", self.line

        if self.shutdown() or self.control_message:
            self.send( self.control_message, "signal") # Pass on
        else:
            self.send(shutdownMicroprocess(), "signal")
        yield 1

import pprint

class NewPop3Client(Axon.Component.component):
    phrases = [
          "list of strings that will be subject lines that are spam",
          "pass these over as a named parameter phrases=<some list>",
          "The phrases should not have carriage returns in",
    ]
    possible_ham_store = "POSSIBLEHAMSTORE"
    possible_ham_store_meta = "POSSIBLEHAMSTORE/.meta"
    def __init__(self, *argv, **argd):
        super(NewPop3Client, self).__init__(*argv, **argd)
        self.stat = ()
        self.stat_mails = 0
        self.stat_size = 0

    def getMailStats(self):
        def local():
            self.send(["STAT"], "outbox")
            while not self.dataReady("inbox"):
                self.pause()
                yield 1
            self.stat = self.recv("inbox")
            self.stat_mails, self.stat_size = self.stat
        return WaitComplete(local())

    def deleteMessage(self, messageid):
        def local():
            print "WARNING, you missed this!"
            return # just in case we accidentally missed something
            self.send(["DELE",messageid], "outbox")
            while not self.dataReady("inbox"):
                self.pause()
                yield 1
            self.result = self.recv("inbox")
        return WaitComplete(local())

    def grabStoreHam(self, messageid):
        def local():
            self.send(["RETR",messageid], "outbox")
            while not self.dataReady("inbox"):
                self.pause()
                yield 1
            self.result = self.recv("inbox")
            filename = str(self.hamcount)
            full_filename = os.path.join(self.possible_ham_store,filename)
            F = open(full_filename, "wb")
            F.write(self.result)
            F.close()
#            print "STORED SPAM IN", full_filename

        return WaitComplete(local())

    def getHamStoreMeta(self):
            F = open(self.possible_ham_store_meta, "r")
            lines = F.read()
            F.close()
            G = eval("".join(lines))
#            print "SPAMSTORE META", G
            return G

    def storeHamStoreMeta(self, meta):
            F = open(self.possible_ham_store_meta, "w")
            F.write(str(meta))
            F.close()
#            print "SPAMSTORE META", meta, "STORED"

    def getMessageHeaders(self, messageID):
        def local():
            self.send(["TOP",messageID,0], "outbox")
            while not self.dataReady("inbox"):
                self.pause()
                yield 1

            self.headers = self.recv("inbox")
        return WaitComplete(local())

    def main(self):

        yield self.getMailStats()
        

        print "Number of emails waiting for us:", self.stat_mails
        print "Size of inbox", self.stat_size
        
        self.hamcount = self.getHamStoreMeta()
    
        lower = self.stat_mails
        
        while lower > 1:
            possible_ham = []
            higher = lower
            lower = max(1, lower-300)
#            lower = max(1, lower-200)
            l = 0
            for mailid in range(lower, higher+1):
                l +=1
                if (l % 100) == 0: print
                sys.stdout.write(".")
                sys.stdout.flush()
    #            print "Retrieving HEADERS of mail", mailid
                yield self.getMessageHeaders(mailid)

    #            print "-------- HEADERS RECEIVED --------"
                probable_spam = False
                for sender in self.headers["from"]:
                    if "mail delivery subsystem" in sender:
                        probable_spam = True
                    if "system administrator" in sender:
                        if "undeliverable" in self.headers["subject"][0]:
                            probable_spam = True

                    for phrase in self.phrases: # hideously inefficient, but works
                        if phrase in self.headers["subject"][0]:
                            probable_spam = True
                    if not probable_spam:
                        print self.headers["subject"][0]

#                if delete:
#                    deletions.append( (mailid, self.headers["from"], self.headers) )
                if not probable_spam:
                    possible_ham.append( (mailid, self.headers["from"], self.headers) )

            print 
            print "============ CANDIDATES AS BEING HAM ============"
            pprint.pprint( [ (ID, FROM, HEADERS["subject"]) for (ID, FROM, HEADERS) in possible_ham ])
            print "TOTAL Suggested", len(possible_ham)
            
            print "To grab these as ham (left on server = ham == training data), don't type 'quit'"

            X = raw_input()
            if X.lower() == "quit":
               break
            if X.lower() != "skip":
                for deletion in possible_ham:
                    ID, FROM, HEADERS = deletion
                    sys.stdout.write(".")
                    sys.stdout.flush()
                    yield self.grabStoreHam(ID)
                    f = str(self.hamcount)
                    self.hamcount +=1
                    self.storeHamStoreMeta(self.hamcount)
                    print "Grabbing COPY of (possible) ham. Mail",ID,"here", self.possible_ham_store+"/"+f

                print "Grabbed possible ham"
                print "To grab more, don't type 'quit'"
                X = raw_input()
                if X.lower() == "quit":
                   break
            else:
                print "skipping, moving on"
                possible_ham = []
        
        print "Done, call again"
        self.send(["QUIT"], "outbox")


if __name__ == "__main__":
    from Kamaelia.File.UnixProcess import UnixProcess

    if len(sys.argv) < 5:
        print "Need username, password, server & port number..."
        print "Usage:"
        print
        print sys.argv[0], "username password server port"
    else:

        getFile = False
        if not os.path.exists("phrases.txt"):
            getFile = True
        else:
            local_filetime = os.path.getmtime("phrases.txt")
            import urllib
            F = urllib.urlopen("http://thwackety.com/phrases.txt")
            remote_time = time.mktime(time.strptime(F.headers["last-modified"],"%a, %d %b %Y %H:%M:%S %Z"))
            F.close()
            if remote_time > local_filetime:
                getFile = True
            else:
               print "remote_time", time.asctime(time.localtime(remote_time))
               print "local_filetime", time.asctime(time.localtime(local_filetime))

        if getFile:
            print "Getting blockfile!"
            UnixProcess('lynx -dump -source >phrases.txt http://thwackety.com/phrases.txt').run()
            print "Got it!"

        f = open("phrases.txt")
        phrases = [ line.strip() for line in f]
        f.close()
        pprint.pprint(phrases)
        username = sys.argv[1]
        password = sys.argv[2]
        server = sys.argv[3]
        port = int(sys.argv[4])
        print "username =", username
        print "password =", password
        print "server =", server
        print "port =", repr(port)

        if 1:
            Graphline(
               RAWCLIENT = basicPop3Client(username=username, password=password),
               CLIENT = NewPop3Client(phrases=phrases),
               
               SERVER = TCPClient(server, port),
               linkages = {
                  ("CLIENT", "outbox") : ("RAWCLIENT", "client_inbox"),
                  ("RAWCLIENT", "client_outbox") : ("CLIENT", "inbox"),

                  ("RAWCLIENT", "outbox") : ("SERVER", "inbox"),
                  ("SERVER", "outbox") : ("RAWCLIENT", "inbox"),
                  ("RAWCLIENT", "signal") : ("SERVER", "control"),
                  ("SERVER", "signal") : ("RAWCLIENT", "control"),
               }
            ).run()
