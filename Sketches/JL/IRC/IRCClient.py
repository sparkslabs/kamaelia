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

"""
==================
Kamaelia IRC Interface
==================

IRC_Client provides an IRC interface for Kamaelia components. To send a command, send a tuple
to its "talk" inbox in the form ('cmd', [arg1] [,arg2] [,arg3...]). E.g. ('JOIN', '#kamaelia'),
('QUIT'), ('PRIVMSG', '#kamtest', 'hey, how's it going?'). IRC_Client will put the command into
a form IRC servers understand, and send the data to its "outbox".

IRC_Client's "inbox" takes messages from an IRC server and retransmits them to its "heard" outbox in
tuple format. Currently each tuple has fields (command, sender, receiver, rest). This method has
worked well so far.

To stop IRC_Client, send a shutdownMicroprocess or a producerFinished to its "control" box.
The higher-level client must send a login itself. Neither IRC_Client nor SimpleIRCClientPrefab
will log in to the server. 

SimpleIRCClientPrefab is a handy prefab that links IRC_Client and TCPClient to each other and
IRC_Client's "talk" and "heard" boxes to the prefab's "inbox" and "outbox" boxes, respectively.
SimpleIRCClientPrefab does not terminate. 


Example Usage
-------------

To link IRCClient to the web::

client = Graphline(irc = IRC_Client(),
              tcp = TCPClient(host, port),
              linkages = {("self", "inbox") : ("irc" , "talk"),
                          ("irc", "outbox") : ("tcp" , "inbox"),
                          ("tcp", "outbox") : ("irc", "inbox"),
                          ("irc", "heard") : ("self", "outbox"),
                          })
Pipeline(ConsoleReader(), PureTransformer(informat), client, PureTransformer(outformat),
         ConsoleEchoer()).run()

or

Pipeline(ConsoleReader(), SimpleIRCClientPrefab(), ConsoleEchoer()).run()

         
Known Issues
-----------
SimpleIRCClientPrefab does not terminate.
Sometimes messages from the server are split up. IRC_Client does not recognize these messages
and flags them as errors. 


"""

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
      self.done = False #does not do anything so far

      debugSections = {"IRCClient.main" : 0,
                       "IRCClient.handleInput" : 0,
                       "IRCClient.parseIRCMessage" : 0,
                       "IRCClient.handleMessage" : 0,
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
            if len(tokens) > 2 :
               body = self.extractBody(tokens[2:])
               if body and 'ACTION' in body.split()[0]: #in case "body" is an empty string
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
               assert self.debugger.note('IRCClient.handleInput', 10, "added : to %s" % param)
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


def informat(text,defaultChannel='#kamtest'):
    if text[0] != '/' or text.split()[0] == '/': #in case we were passed "/ word words", or simply "/"
        return ('PRIVMSG', defaultChannel, text)
    words = text.split()
    tag = words[0]
    tag = tag.lstrip('/').upper()
    if tag == 'MSG':
        tag = 'PRIVMSG'
    try:
        if tag == 'QUIT' and len(words) >= 2:
            return (tag, string.join(words[1:]))
        elif tag in ('PRIVMSG', 'MSG', 'NOTICE', 'KILL', 'TOPIC', 'SQUERY') and len(words) >= 3:
            return (tag, words[1], string.join(words[2:]))
        elif tag == 'KICK' and len(words) >= 4:
            return (tag, words[1], words[2], string.join(words[3:]))
        elif tag == 'USER':
            return (tag, words[1], words[2], words[3], string.join(words[4:]))
        elif tag == 'ME' and len(words) >= 2:
            return (tag, defaultChannel, string.join(words[1:]))
        else: 
            words[0] = tag
            if tag: #only false if we were passed "/" as text
                return words
    except IndexError:
        words[0] = tag
        return words


def outformat(data, defaultChannel='#kamtest'):
    msgtype, sender, recipient, body = data
    end = '\n'
    if msgtype == 'PRIVMSG':
        if body[0:5] == '[off]': #we don't want to log lines prefixed by "[off]"
            return
        text = '<%s> %s' % (sender, body)
    elif msgtype == 'JOIN' :
        text = '*** %s has joined %s' % (sender, recipient)
    elif msgtype == 'PART' :
        text = '*** %s has parted %s' % (sender, recipient)
    elif msgtype == 'NICK':
        text = '*** %s is now known as %s' % (sender, recipient)
    elif msgtype == 'ACTION':
        text = '*** %s %s' % (sender, body)
    elif msgtype == 'TOPIC':
        text = '*** %s changed the topic to %s' % (sender, body)
    elif msgtype == 'QUIT': #test this, channel to outbox, not system
        text = '*** %s has quit IRC' % (sender)
    elif msgtype == 'MODE' and recipient == defaultChannel:
        text = '*** %s has set channel mode: %s' % (sender, body) 
    elif msgtype > '000' and msgtype < '400':
        text = 'Reply %s from %s to %s: %s' % data
    elif msgtype >= '400' and msgtype < '600':
        text = 'Error! %s %s %s %s' % data
    elif msgtype >= '600' and msgtype < '1000':
        text = 'Unknown numeric reply: %s %s %s %s' % data
    else:
        text = '%s from %s: %s' % (msgtype, sender, body)
    return text + end

def channelOutformat(channel):
    return (lambda data: outformat(data, defaultChannel=channel))

def channelInformat(channel):
    return (lambda text: informat(text, defaultChannel=channel))

from Kamaelia.Chassis.Pipeline import Pipeline
def SimpleIRCClientPrefab(channel='#kamtest', host='irc.freenode.net', port=6667):
    client = Graphline(irc = IRC_Client(),
                  tcp = TCPClient(host, port),
                  linkages = {("self", "inbox") : ("irc" , "talk"),
                              ("irc", "outbox") : ("tcp" , "inbox"),
                              ("tcp", "outbox") : ("irc", "inbox"),
                              ("irc", "heard") : ("self", "outbox"),
                              }
                  )

    return Pipeline(PureTransformer(channelInformat(channel)),
                    client,
                    PureTransformer(channelOutformat(channel)))

if __name__ == '__main__':
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    Pipeline(ConsoleReader(), SimpleIRCClientPrefab(), ConsoleEchoer()).run()
