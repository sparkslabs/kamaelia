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
# This is the base version.
# The purpose of this version is to see if a general sendCommand statement would
#  work, and to improve display support for messages other than PRIVMSGs. 
# The purpose of this version is to try out the IF model of message parsing.
# The purpose of this version is to try out a more general IF model -- one
#  general path for messages via IRC and one general path for messages received
#  from the local user. It relays all received data to its "heard" outbox,
#  in the form (msgtype, sender, recipient, body)

import Axon as _Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Chassis.Graphline import Graphline
import string

class channel(object):
   """\
      This is an ugly hack - the send here is one helluvahack. 
      (works with a socket and a component. It's deliberate but
      ugly as hell""" 
   # Sock here is currently a component, and default inbox
   def __init__(self, sock, channel):
      self.sock = sock
      self.channel = channel
   def join(self):
      self.sock.send ( 'JOIN %s\r\n' % self.channel)
   def say(self, message):
      self.sock.send ( 'PRIVMSG %s :%s\r\n' % (self.channel, message))
   def leave(self):
      self.sock.send("PART %s\r\n" % self.channel)
   def topic(self, newTopic):
       self.sock.send("TOPIC %s :%s\r\n" % (self.channel, newTopic))

class IRC_Client(_Axon.Component.component):
   """\
      This is the base client. It is broken in the same was as
      the earliest internet handling code was. In many respects this
      is the logical counterpart to a TCPServer which upon connection
      should spawn the equivalent of a Connected Socket Adaptor. 

      Specifically - consider that in order to make this work "properly"
      it needs to handle the chat session multiplexing that happens by
      default in IRC. There are MANY ways this could be achieved.
   """
   Inboxes = {"inbox":"", "control":"", "talk":"", "topic":""}
   Outboxes = {"outbox":"",
               "signal":"",
               "heard" : "messages from the server"}
   
   def __init__(self, nick="kamaeliabot",
                      nickinfo="Kamaelia",
                      defaultChannel="#kamaeliatest"):
      self.__super.__init__()
      self.nick = nick
      self.nickinfo = nickinfo
      self.defaultChannel = defaultChannel
      self.channels = {}
      self.done = False
      self.debugger = _Axon.debug.debug()
      self.debugger.useConfig()
      self.debugger.addDebugSection("IRCClient.main", 5)
      
   def login(self, nick, nickinfo, password = None, username=None):
      """Should be abstracted out as far as possible.
         Protocol can be abstracted into the following kinds of items:
             - The independent atoms of the transactions in the protocol
             - The orchestration of the molecules of the atoms of
               transactions of the protocol.
             - The higher level abstractions for handling the protocol
      """
      self.send ( 'NICK %s\r\n' % nick )
      if password:
          self.send('PASS %s\r\n' % password )
      if not username:
          username = nick
      self.send ( 'USER %s %s %s :%s\r\n' % (username,nick,nick, nickinfo))

   def join(self, someChannel):
      chan = channel(self,someChannel)
      chan.join()
      return chan

   def main(self):
      "Handling here is still in progress. :)"
      self.login(self.nick, self.nickinfo)
      self.channels[self.defaultChannel] = self.join(self.defaultChannel)
      
      while not self.shutdown():
         data=""
         if self.dataReady("talk"):
            data = self.recv("talk")
            assert self.debugger.note('IRCClient.main', 5, 'received talk ' + data)
            self.handleInput(data)
         if self.dataReady("inbox"): #if received messages 
             self.handleMessage(self.recv("inbox"))
                    
         if not self.anyReady(): # Axon 1.1.3 (See CVS)
            self.pause() # Wait for response :-)
         yield 1
         
      self.channels[self.defaultChannel].leave()
      # print self.nick + "... is leaving\n" # Check with and IRC client instead.

   def handleMessage(self, lines):
        """handles incoming messages from the server"""
        if "\r" in lines:
            lines.replace("\r","\n")
        lines = lines.split("\n")
        for one_line in lines:
            if self.parseable(one_line):
                data = self.parseIRCMessage(one_line)
            elif len(one_line) > 0:
                self.send(("CLIENT ERROR", 'client', '', one_line), 'heard')
                
            if data:
                (msgtype, sender, recipient, body) = data
                #reply to pings
                if msgtype == 'PING':
                    reply = ("PONG " + sender)
                    self.send(reply + '\r\n')
                    assert self.debugger.note('IRCClient.main', 1, 'PONG response to ' + one_line)
                elif (msgtype == 'PRIVMSG' or msgtype == 'NOTICE') and 'PING ' in body:
                    #must be 'PING ' because 'PING' matches things like CASEMAPPING=ascii
                    reply = ("PONG " + body[body.find("PING")+4:])
                    self.send(reply + '\r\n')
                    assert self.debugger.note('IRCClient.main', 1, 'PONG response to ' + one_line)
                self.send(data, 'heard')
                
   def parseable(self, line):
        if len(line) > 0 and len(line.split()) <= 1 and line[0] == ':':
            return False
        return len(line) > 0
       
   def parseIRCMessage(self, line):
        """Assumes most lines in the format of :nick!username MSGTYPE recipient :message.
           Returns a tuple (message type, sender, recipient, other params)."""
        tokens = line.split()
        sender = ""
        recipient = ""
        body = ""
        try:
            if tokens[0][0] == ':':
               sender = self.extractSender(tokens[0])
               tokens = tokens[1:]
               
            msgtype = tokens[0]
            recipient = tokens[1]
            if len(tokens) > 2:
               body = self.extractBody(tokens[2:])
            if msgtype == 'PING':
                sender =  recipient
                recipient = ""
            return (msgtype, sender, recipient, body)
        except IndexError:
            print "Malformed or unaccounted-for message:", line

   def extractSender(self, token):
        if '!' in token:
            return token[1:token.find('!')]
        else:
            return token[1:]

   def extractBody(self, tokens):
        body =  string.join(tokens, ' ')
        if body[0] == ':':
            return body[1:]
        else:
            return body

   def handleInput(self, lines):
        if "\r" in lines:
            lines.replace("\r","\n")
        lines = lines.split("\n")
        for one_line in lines:
            if one_line: #we don't want to deal with empty lines
                tokens = one_line.split()
                command = "PRIVMSG"
                target = ""
                body = ""
                try: 
                    if one_line[0] == '/':
                        command = tokens[0][1:].upper()
                        del(tokens[0])
                        if command == 'MSG':
                            command = 'PRIVMSG'
                        if command == 'QUIT':
                            self.done = True
                    if len(tokens) > 0:
                        target = tokens[0]
                    if len(tokens) > 1:
                        body = ':' + string.join(tokens[1:])
                    send = '%s %s %s \r\n' % (command, target, body) 
                    self.send(send)
                    assert self.debugger.note('IRCClient.main', 5, send)
                except IndexError:
                    print "Malformed message:", one_line
                    #/ hello world
                    

   def shutdown(self):
       while self.dataReady("control"):
           msg = self.recv("control")
           if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
               return True
       return False

      
def SimpleIRCClientPrefab(host="127.0.0.1",
                          port=6667,
                          nick="kamaeliabot",
                          nickinfo="Kamaelia",
                          defaultChannel="#kamaeliatest",
                          IRC_Handler=IRC_Client):
    return Graphline(
        CLIENT = TCPClient(host, port),
        PROTO = IRC_Handler(nick, nickinfo, defaultChannel),
        linkages = {
              ("CLIENT" , "outbox") : ("PROTO" , "inbox"),
              ("PROTO"  , "outbox") : ("CLIENT", "inbox"),
              ("PROTO"  , "heard")  : ("SELF", "outbox"), #SELF refers to the Graphline. Passthrough linkage
              ("SELF"  , "inbox") : ("PROTO" , "talk"), #passthrough
              ("SELF"  , "control") : ("PROTO" , "control"), #passthrough
              ("PROTO"  , "signal") : ("CLIENT", "control"),
              ("CLIENT" , "signal") : ("SELF" , "signal"), #passthrough
              }
        )

if __name__ == '__main__':
    from Kamaelia.Util.Console import ConsoleReader
    from NiceTickerPrefab import NiceTickerPrefab
    from Kamaelia.Chassis.Pipeline import Pipeline
    Pipeline(
        ConsoleReader(),
        SimpleIRCClientPrefab(host="irc.freenode.net", nick="kamaeliabot", defaultChannel="#kamtest"),
        NiceTickerPrefab(render_right = 800,render_bottom = 600),
    ).run()
