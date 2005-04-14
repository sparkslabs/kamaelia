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

class channel(object):
   # Note: This used to be used with a socket, it's now using a component
   # instead, with no change.
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
   def __init__(self, nick="kamaeliabot",
                      nickinfo="Kamaelia IRC",
                      defaultChannel="#kamtest"):
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

      while 1:
         data=""
         if self.dataReady():
            data = self.recv()
            self.channels[self.defaultChannel].say("Woo: " + str(data[:80]))
         if data.find(self.nick) != -1:
            if data.find("LEAVE") != -1:
               break
         self.pause() # Wait for response :-)
         yield 1
      self.channels[self.defaultChannel] .leave()

class SimpleIRCClient(_Axon.Component.component):
   def __init__(self, host="127.0.0.1", 
                      port="6667", 
                      nick="kamaeliabot",
                      nickinfo="Kamaelia IRC",
                      defaultChannel="#kamtest",
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
      port=6667

      client = TCPClient("127.0.0.1",port)
      clientProtocol = self.IRC_Handler(self.nick, self.nickinfo, self.defaultChannel)

      self.link((client,"outbox"), (clientProtocol,"inbox"))
      self.link((clientProtocol,"outbox"), (client,"inbox"))

      self.addChildren(clientProtocol, client)
      yield _Axon.Ipc.newComponent(*(self.children))
      while 1:
         self.pause()
         yield 1

if __name__ == '__main__':
   from Axon.Scheduler import scheduler
   t = SimpleIRCClient().activate()
   t.activate()
   scheduler.run.runThreads(slowmo=0)

"""
   if data.find ( 'PING' ) != -1: # Handle network PINGs
      irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )

   if data.find ( 'PRIVMSG' ) != -1:
      ":Nick!user@host PRIVMSG destination :Message"
      nick = data.split ( '!' ) [ 0 ].replace ( ':', '' )
      message = ':'.join ( data.split ( ':' ) [ 2: ] )
      print nick + ':', message
"""