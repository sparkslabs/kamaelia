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
from Axon.Ipc import producerFinished, shutdownMicroprocess, WaitComplete
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.PureTransformer import PureTransformer
import string

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
    Inboxes = {"inbox":"incoming message strings from the server",
              "control":"shutdown handling",
              "talk":"takes tuples to be turned into IRC commands ",
              }
   
    Outboxes = {"outbox":"IRC commands to be sent out to the server",
               "signal":"shutdown handling",
               "heard" : "parsed tuples of messages from the server"}
   
    def __init__(self):
      self.__super.__init__()
      self.done = False

      debugSections = {"IRCClient.main" : 5,
                       "IRCClient.handleInput" : 5,
                       }
      self.debugger.addDebug(**debugSections)
      
    def main(self):
        "Handling here is still in progress. :)"
        while not self.shutdown():
           data=""
           if self.dataReady("talk"):
               data = self.recv("talk")
               assert self.debugger.note('IRCClient.main', 5, 'received talk ' + str(data))
               self.handleInput(data)
           if self.dataReady("inbox"):
               data = self.recv("inbox")
               assert self.debugger.note('IRCClient.main', 10, 'received from server ' + str(data))
               self.handleMessage(data)
                    
           if not self.anyReady():
              self.pause()
           yield 1

    def handleMessage(self, lines):
        """handles incoming messages from the server"""
        if "\r" in lines:
            lines.replace("\r","\n")
        lines = lines.split("\n")
        for one_line in lines:
            data = None
            if self.parseable(one_line):
                data = self.parseIRCMessage(one_line)
                self.send(data, "heard")
            elif len(one_line) > 0:
                self.send(("CLIENT ERROR", 'client', '', one_line), 'heard')
                
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
            recipient = tokens[1].lstrip(':')
            if len(tokens) > 2:
               body = self.extractBody(tokens[2:])
               if 'ACTION' in body.split()[0]:
                    msgtype = 'ACTION'
                    body = string.join(body.split()[1:])
            if msgtype == 'PING':
                sender =  recipient
                recipient = ""
            return (msgtype, sender, recipient, body)
        except IndexError:
            return (("CLIENT ERROR", 'client', '', line))

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

    def handleInput(self, command_tuple):
       mod_command = []
       for param in command_tuple:
           if len(param.split()) > 1 or (len(param.split())== 1 and param[0] == ':'):
               mod_command.append(':' + param)
           else:
               mod_command.append(param)
       mod_command[0] = mod_command[0].upper()

       if mod_command[0] == 'ME' and len(mod_command) > 2:
           assert self.debugger.note('IRCClient.handleInput', 10, str(mod_command))
           send = 'PRIVMSG %s :\x01ACTION %s\x01' % (mod_command[1], mod_command[2].lstrip(':'))
       elif mod_command[0] == 'ACTION':
           send = 'PRIVMSG %s :\x01ACTION\x01' % mod_command[1]
       else: send = string.join(mod_command)
       
       assert self.debugger.note('IRCClient.handleInput', 5, send)
       self.send(send + '\r\n')

    def shutdown(self):
       while self.dataReady("control"):
           msg = self.recv("control")
           if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
               return True
       return self.done
