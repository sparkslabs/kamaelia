#!/usr/bin/env python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
#

import Axon as _Axon
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.Graphline import Graphline
from Axon.Ipc import producerFinished, shutdownMicroprocess

    
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
      should spawn the equivalent of a Connected Socket Adaptor. Since
      this could happen in various different ways, please hack on a
      COPY of this file, rather that this file. (Keeps this file
      relatively simple)

      Specifically - consider that in order to make this work "properly"
      it needs to handle the chat session multiplexing that happens by
      default in IRC. There are MANY ways this could be achieved.
   """
   Inboxes = ["inbox", "control", "talk", "topic"]
   Outboxes = ["outbox", "signal", "heard" ]
   def __init__(self, nick="kamaeliabot",
                      nickinfo="Kamaelia",
                      defaultChannel="#kamaeliatest"):
      self.__super.__init__()
      self.nick = nick
      self.nickinfo = nickinfo
      self.defaultChannel = defaultChannel
      self.channels = {}

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
      "Handling here is pretty naff really :-)"
      self.login(self.nick, self.nickinfo)
      self.channels[self.defaultChannel] = self.join(self.defaultChannel)
      seen_VERSION = False

      while not self.shutdown():
         data=""
         if self.dataReady("talk"):
            data = self.recv("talk")
            self.channels[self.defaultChannel].say(data)
         elif self.dataReady("topic"):
             newtopic = self.recv("topic")
             self.channels[self.defaultChannel].topic(newtopic)
         elif self.dataReady("inbox"):
            lines = self.recv()
            if "\r" in lines:
                lines.replace("\r","\n")
            lines = lines.split("\n")
            for data in lines:
                if "PRIVMSG" in data:
                    if data[0] == ":":
                        data = data[1:]
                    if ("VERSION" in data) and not seen_VERSION:
                        seen_Version = True
                    else:
                        data = data[data.find(":")+1:]
                        self.send(data, "heard")
                elif "PING" in data:
                    reply = "PONG" + data[data.find("PING")+4:]
                    self.send(reply+"\r\n")

         if data.find(self.nick) != -1:
            if data.find("LEAVE") != -1:
               break

         if not self.anyReady(): # Axon 1.1.3 (See CVS)
            self.pause() # Wait for response :-)
         yield 1
         
      self.channels[self.defaultChannel].leave()
      # print self.nick + "... is leaving\n" # Check with and IRC client instead.

   def shutdown(self):
       while self.dataReady("control"):
           msg = self.recv("control")
           if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
               return True
       return False

class SimpleIRCClient(_Axon.Component.component):
   "Sample integration of the IRCClient into a networked environment"
   Inboxes = {
       "inbox" : "Stuff that's being said on the channel",
       "control" : "Shutdown control/info",
       "topic" : "Change topic on the channel",
   }
   Outboxes = ["outbox", "signal"]
   def __init__(self, host="127.0.0.1",
                      port=6667,
                      nick="kamaeliabot",
                      nickinfo="Kamaelia",
                      defaultChannel="#kamaeliatest",
                      IRC_Handler=IRC_Client):
      self.__super.__init__()
      self.host = host
      self.port = port
      self.nick = nick
      self.nickinfo = nickinfo
      self.defaultChannel = defaultChannel
      self.IRC_Handler = IRC_Handler

   def main(self):
      import random
      port=self.port

      host = self.host

#      client = TCPClient(host,port)
#      clientProtocol = self.IRC_Handler(self.nick, self.nickinfo, self.defaultChannel)


      subsystem = Graphline(
          SELF   = self,
          CLIENT = TCPClient(host,port),
          PROTO  = self.IRC_Handler(self.nick, self.nickinfo, self.defaultChannel),
          linkages = {
              ("CLIENT" , "") : ("CLIENT", ""),
              ("CLIENT" , "") : ("PROTO" , ""),
              ("PROTO"  , "") : ("CLIENT", ""),
              ("PROTO"  , "") : ("PROTO" , ""),
              ("CLIENT" , "outbox") : ("PROTO" , "inbox"),
              ("PROTO"  , "outbox") : ("CLIENT", "inbox"),
              ("PROTO"  , "heard")  : ("SELF", "outbox"),
              ("SELF"  , "inbox") : ("PROTO" , "talk"),
              ("SELF"  , "topic") : ("PROTO" , "topic"),
              ("SELF"  , "control") : ("PROTO" , "control"),
              ("PROTO"  , "signal") : ("CLIENT", "control"),
              ("CLIENT" , "signal") : ("SELF" , "signal"),
          }
      )

#      self.link((client,"outbox"), (clientProtocol,"inbox"))
#      self.link((clientProtocol,"outbox"), (client,"inbox"))
#
#      self.link((clientProtocol, "heard"), (self, "outbox"), passthrough=2)
#      self.link((self, "inbox"), (clientProtocol, "talk"), passthrough=1)
#      self.link((self, "topic"), (clientProtocol, "topic"), passthrough=1)
#      
#      self.link((self, "control"), (clientProtocol, "control"), passthrough=1)
#      self.link((clientProtocol, "signal"), (client, "control"))
#      self.link((client, "signal"), (self, "signal"), passthrough=2)
#
      self.addChildren(subsystem)
      yield _Axon.Ipc.newComponent(*(self.children))
      while 1:
         self.pause()
         yield 1

if __name__ == '__main__':
   from Axon.Scheduler import scheduler
   from Kamaelia.Util.Console import ConsoleReader
   from Kamaelia.UI.Pygame.Ticker import Ticker
   from Kamaelia.Util.PipelineComponent import pipeline

   pipeline(
       ConsoleReader(),
       SimpleIRCClient(host="127.0.0.1", nick="kamaeliabot", defaultChannel="#kamtest"),
       Ticker(render_right = 800,render_bottom = 600),
   ).run()
