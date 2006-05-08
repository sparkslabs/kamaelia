#!/usr/bin/env python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
#	 All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#	 http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#	 not this notice.
# (2) Reproduced in the COPYING file, and at:
#	 http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
#
"""
=======================
IRC Logging Bot
=======================

This component interacts with an IRC server via its inbox and outbox. It should be connected to a TCP client component

This component does not terminate.
"""

import sys
import datetime
import time
from Axon.Component import component
import string

class IRCBot(component):
	"""\
	IRCBot() -> new IRCBot 
	"""
	Inboxes = { "inbox"   : "messages received over TCP",
				"command" : "simple instructions for the bot",
				"control" : "UNUSED"
			  }
	Outboxes = { "outbox" : "messages to send over TCP",
				 "signal" : "UNUSED",
				 "heard"   : "private/channel messages received by the bot",
			   }
	
	#FindResponses = (
	#	("no module named dirac_parser", "Try installing http://prdownloads.sourceforge.net/dirac/dirac-0.5.4.tar.gz?download" ),
	#)
	#DirectResponses = { "goodnight" : "goodnight!", "good night" : "goodnight!", "night" : "goodnight!", "nite" : "goodnight!" }

	ERR_NOSUCHNICK           = 401
	ERR_NOSUCHSERVER         = 402	
	ERR_NOSUCHCHANNEL        = 403
	ERR_CANNOTSENDTOCHAN     = 404
	ERR_TOOMANYCHANNELS      = 405
	ERR_WASNOSUCHNICK        = 406
	ERR_TOOMANYTARGETS       = 407
	#more to come

	def writeHeard(self, src):
		t = datetime.datetime.now()
		epochsecs = time.mktime(t.timetuple())
		msg = ("%d" % epochsecs) + " " + string.join(src, " ") + "\n"
		self.send(msg, "heard")

	def __init__(self, nick, password, channel, username):
		super(IRCBot, self).__init__()
		self.nick = nick
		self.password = password
		self.channel = channel
		self.username = username

	def changeNick(self, newnick):
		self.nick = newnick
		self.send("NICK %s\r\n" % newnick, "outbox")

	def joinChannel(self):
		self.send( 'JOIN %s\r\n' % self.channel, "outbox")
	def say(self, recipient, message):
		self.send("PRIVMSG %s :%s\r\n" % (recipient, message), "outbox")
	def leaveChannel(self, channel):
		self.send("PART %s\r\n" % channel, "outbox")
	def changeTopic(self, channel, topic):
		self.send("TOPIC %s :%s\r\n" % (channel, topic), "outbox")

	def login(self):
		self.send("NICK %s\r\n" % self.nick, "outbox")
		if self.password:
			self.send("PASS %s\r\n" % self.password)
		if not self.username:
			self.username = self.nick
		self.send ("USER %s %s %s :%s\r\n" % (self.username,self.nick,self.nick, "Kamaelia IRC Bot"), "outbox")
		self.logging = True

	def main(self):
		"""Main loop"""
		self.login()
		self.joinChannel()
		readbuffer = ""

		while 1:
			yield 1
			
			if self.dataReady("command"):
				command = self.recv("command")
				if command[0] == "JOIN": # join a channel
					self.send("JOIN %s\r\n" % command[1], "outbox")
				elif command[0] == "PRIVMSG": # send a message to an individual or a channel
					self.send("PRIVMSG %s :%s\r\n" % (command[1], command[2]), "outbox")

			if self.dataReady("inbox"):
				readbuffer += self.recv("inbox")
				lines = string.split(readbuffer, "\n")
				readbuffer = lines.pop() #the remainder after final \n

				for line in lines:
					print line
					line = string.rstrip(line)
					splitline = string.split(line)
					linesender = ""
					if splitline[0][0] == ":":
						linesender = string.split(splitline[0][1:],"!")[0]
						splitline.pop(0)

					if splitline[0] == "NOTICE": #ignorable
						pass
					elif splitline[0] == "PING":
						# should alter this to consider if no second part given
						msgsend = "PONG %s\r\n" % splitline[1]
						self.send(msgsend, "outbox")
					elif splitline[0] == "PRIVMSG":
						msg = string.join(splitline[2:], " ")[1:]
						
						messageforme = False

						
						if msg[0:len(self.nick)].lower() == self.nick.lower():
							msg = string.lstrip(msg[len(self.nick):])
							messageforme = True

						if msg[0:11].lower() == "logging off":
							if not self.logging:
								self.say(splitline[1], "Logging was already off")
							else:
								self.say(splitline[1], "Logging is off")
								self.changeNick("[kambot-deaf]")
								msg = ( "LOGGINGOFF", linesender, "" )
								self.writeHeard(msg)
								self.logging = False
						elif msg[0:10].lower() == "logging on":
							if self.logging:
								self.say(splitline[1], "Logging was already on")
							else:
								self.say(splitline[1], "Logging is on")
								self.changeNick("[kambot-logging]")
								msg = ( "LOGGINGON", linesender, "" )
								self.writeHeard(msg)
								self.logging = False
						else:
							if msg.lower().find("no module named dirac_parser") != -1:
								self.say(splitline[1], "http://prdownloads.sourceforge.net/dirac/dirac-0.5.4.tar.gz?download")		
							elif messageforme:
								self.say(splitline[1], msg + "?")

							if msg[0:5].lower() != "[off]" and self.logging:
								msg = ( "PRIVMSG", linesender, msg )
								self.writeHeard(msg)

					elif splitline[0] == "PART":
						msg = ( "PART", linesender, splitline[1] )
						self.writeHeard(msg)

if __name__=="__main__":
	from Kamaelia.Internet.TCPClient import TCPClient
	from Kamaelia.Util.Console import ConsoleReader
	from Kamaelia.Util.PipelineComponent import pipeline
	from Axon.Scheduler import scheduler
	from Lagger import Lagger
	import Axon
	from Kamaelia.File.Writing import SimpleFileWriter

	class TestHarness(component):
		def __init__(self):
			super(TestHarness, self).__init__()

		def main(self):
			self.lagger = Lagger()
			self.bot = IRCBot("[kambot-logging]","","#kamaelia","kamaeliabot")
			self.client = TCPClient("irc.freenode.net", 6667, 1)
			self.writer = SimpleFileWriter("latest.txt")

			self.link((self.bot, "heard"), (self.writer, "inbox"))
			self.link((self.bot, "outbox"), (self.client, "inbox"))
			self.link((self.client, "outbox"), (self.bot, "inbox"))
			self.addChildren(self.lagger, self.bot, self.client, self.writer)
			yield Axon.Ipc.newComponent(*(self.children))
			while 1:
				self.pause()
				yield 1

	t = TestHarness()
	t.activate()
	scheduler.run.runThreads(slowmo=0)
	
