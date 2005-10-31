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

class channel(object):
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

class IRC_Client(_Axon.Component.component):
   Inboxes = ["inbox", "control", "talk"]
   Outboxes = ["outbox", "signal", "heard" ]
   def __init__(self, nick="michaels",
                      nickinfo="Kamaelia",
                      defaultChannel="#oscon"):
      self.__super.__init__()
      self.nick = nick
      self.nickinfo = nickinfo
      self.defaultChannel = defaultChannel
      self.channels = {}

   def login(self, nick, nickinfo):
      self.send ( 'NICK %s\r\n' % nick )
      self.send ( 'USER %s %s %s :%s\r\n' % (nick,nick,nick, nickinfo))

   def join(self, someChannel):
      chan = channel(self,someChannel)
      chan.join()
      return chan

   def main(self):
      "Handling here is pretty naff really :-)"
      self.login(self.nick, self.nickinfo)
      self.channels[self.defaultChannel] = self.join(self.defaultChannel)
      seen_VERSION = False
      while 1:
         data=""
         if self.dataReady("talk"):
            data = self.recv("talk")
            self.channels[self.defaultChannel].say(data)
         elif self.dataReady("inbox"):
            data = self.recv()
            if "PRIVMSG" in data:
                if data[0] == ":":
                    data = data[1:]
                if ("VERSION" in data) and not seen_VERSION:
                    seen_Version = True
                else:
                    data = data[data.find(":")+1:]
                    self.send(data, "heard")

         if data.find(self.nick) != -1:
            if data.find("LEAVE") != -1:
               break
         self.pause() # Wait for response :-)
         yield 1
      self.channels[self.defaultChannel] .leave()

class SimpleIRCClient(_Axon.Component.component):
   Inboxes = {
       "inbox" : "Stuff that's being said on the channel",
       "control" : "Shutdown control/info",
       "talk" : "Something to say on the channel",
   }
   Outboxes = ["outbox", "signal", "heard" ] 
   def __init__(self, host="127.0.0.1", 
                      port=6667, 
                      nick="michaels",
                      nickinfo="Kamaelia",
                      defaultChannel="#oscon",
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

      client = TCPClient(host,port)
      clientProtocol = self.IRC_Handler(self.nick, self.nickinfo, self.defaultChannel)

#      self.link((client,"outbox"), (clientProtocol,"inbox"))
#      self.link((clientProtocol,"outbox"), (client,"inbox"))
#      self.link((clientProtocol, "heard"), (self, "heard"), passthrough=2)
#      self.link((self, "talk"), (clientProtocol, "talk"), passthrough=1)

      self.link((client,"outbox"), (clientProtocol,"inbox"))
      self.link((clientProtocol,"outbox"), (client,"inbox"))

      self.link((clientProtocol, "heard"), (self, "outbox"), passthrough=2)
      self.link((self, "inbox"), (clientProtocol, "talk"), passthrough=1)

      self.addChildren(clientProtocol, client)
      yield _Axon.Ipc.newComponent(*(self.children))
      while 1:
         self.pause()
         yield 1

#
# Logically this should be equivalent to the above, but causes a bug in Graphline to manifest
# itself. Specific backtrace:
# Traceback (most recent call last):
#   File "./IRCClient.py", line 171, in ?
#     CONNECTION = SimpleIRCClient(host="127.0.0.1", defaultChannel="#oscon"),
#   File "./IRCClient.py", line 155, in SimpleIRCClient
#     linkages = {
#   File "/usr/lib/python2.4/site-packages/Kamaelia/Util/Graphline.py", line 44, in __init__
#     self.addExternalPostboxes()
#   File "/usr/lib/python2.4/site-packages/Kamaelia/Util/Graphline.py", line 68, in
#  addExternalPostboxes
#     self.Outboxes[toBox] = fromComponent.Outboxes[sourceBox]
# TypeError: list indices must be integers
#
def __SimpleIRCClient(host="127.0.0.1", 
                      port=6667, 
                      nick="michaels",
                      nickinfo="Kamaelia",
                      defaultChannel="#oscon",
                      IRC_Handler=IRC_Client):

    Graphline(
        CLIENT = TCPClient(host,port),
        PROTOCOL = IRC_Handler(nick, nickinfo, defaultChannel),
        linkages = {
            ("CLIENT", "outbox") : ("PROTOCOL", "inbox"),
            ("PROTOCOL", "outbox") : ("CLIENT", "inbox"),
            ("PROTOCOL", "heard") : ("self", "heard"),
            ("self", "talk") : ("PROTOCOL", "talk"),
        }
    )


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
