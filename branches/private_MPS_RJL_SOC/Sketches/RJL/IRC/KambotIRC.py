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

This component interacts with an IRC client via its inbox and outbox.

This component does not terminate.
"""

import sys
import datetime
import time
from Axon.Component import component
import string
from IRCLoggingBot import IRCBot

class Kambot(component):
	"""\
	Kambot() -> new IRCBot 
	"""
	Inboxes = { "inbox"   : "IRC messages heard",
				"control" : "UNUSED"
			  }
	Outboxes = { "outbox" : "commands to the IRCBot",
				 "signal" : "UNUSED",
				 "log"   : "lines to log",
			   }
	
	FindResponses = (
		( ( "no module named dirac_parser", ), "Try installing http://prdownloads.sourceforge.net/dirac/dirac-0.5.4.tar.gz?download" ),
		( ( "life", "the universe", "everything", ), "What do you get if you multiply 6 by 9?" ),
		( ( ("hi", "hey", "greetings", "hello", ), ("kambot", "{msgforme}")), "Hello." ),
		( ( "ecky", ), "Ptang!" ),
		( ( ("ibble", "piffle" ), ("kambot", "{msgforme}" )), "Fish."),
		( ( "pie", ), "Mmm pie..." ),
		( ( "!!!" , ), "Multiple exclamation marks... are a sure sign of a diseased mind." )
	)

	#DirectResponses = { "goodnight" : "goodnight!", "good night" : "goodnight!", "night" : "goodnight!", "nite" : "goodnight!" }

	def writeLog(self, src):
		t = datetime.datetime.now()
		epochsecs = time.mktime(t.timetuple())
		msg = ("%d" % epochsecs) + " " + string.join(src, " ") + "\n"
		self.send(msg, "log")

	def __init__(self, nick):
		super(Kambot, self).__init__()
		self.nick = nick
		self.logging = True

	def changeNick(self, newnick):
		self.nick = newnick
		self.send("NICK %s\r\n" % newnick, "outbox")

	def joinChannel(self):
		self.send( "JOIN %s\r\n" % self.channel, "outbox")
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
		while 1:
			yield 1
			
			if self.dataReady("inbox"):
				event = self.recv("inbox")

				if event[0] == "PRIVMSG":
					msg = event[3]
					messageforme = False

					if msg[0:len(self.nick)].lower() == self.nick.lower():
						msg = string.lstrip(msg[len(self.nick):])
						messageforme = True

					if msg[0:11].lower() == "logging off" or msg[0:15].lower() == "disable logging":
						if not self.logging:
							self.say(event[2], "Logging was already off")
						else:
							self.say(event[2], "Logging is now off")
							self.changeNick("[kambot-deaf]")
							msg = ( "LOGGINGOFF", event[1], "" )
							self.writeLog(msg)
							self.logging = False
					elif msg[0:10].lower() == "logging on" or msg[0:14].lower() == "enable logging":
						if self.logging:
							self.say(event[2], "Logging was already on")
						else:
							self.say(event[2], "Logging is now on")
							self.changeNick("[kambot-logging]")
							msg = ( "LOGGINGON", event[1], "" )
							self.writeLog(msg)
							self.logging = True
					else:
						matched = False
						for matchresponse in self.FindResponses:
							thismatches = True
							for lookfor in matchresponse[0]: # have to match each of these
								if type(lookfor) == type("a string"):
									if lookfor == "{msgforme}" and messageforme:
										print "Single message for me match"
									elif msg.lower().find(lookfor) != -1:
										print "Single matched " + lookfor
									else:
										thismatches = False
								else:
									thissubmatches = False
									for sublookfor in lookfor: # have to match one of these
										if sublookfor == "{msgforme}" and messageforme:
											print "Message for me match"
											thissubmatches = True
											break
										elif msg.lower().find(sublookfor) != -1:
											print "Matched " + sublookfor
											thissubmatches = True
											break
									if not thissubmatches:
										thismatches = False
										break

							if thismatches:
								matched = True
								self.say(event[2], matchresponse[1])	
								break
						
						if msg[0:6] == "[say] ":
							self.say("#kamaelia", msg[6:]) #fix this to use channel
						if not matched and messageforme:
							self.say(event[2], msg + "?")

						if msg[0:5].lower() != "[off]" and self.logging:
							self.writeLog(event)

				elif event[0] == "PART":
					self.writeLog(event)
				elif event[0] == "JOIN":
					self.writeLog(event)

if __name__=="__main__":
	from Kamaelia.Internet.TCPClient import TCPClient
	from Kamaelia.Util.Console import ConsoleReader
	from Kamaelia.Util.PipelineComponent import pipeline
	from Axon.Scheduler import scheduler
	from Lagger import Lagger
	from IRCLoggingBot import IRCBot
	import Axon
	from Kamaelia.File.Writing import SimpleFileWriter

	class TestHarness(component):
		def __init__(self):
			super(TestHarness, self).__init__()

		def main(self):
			self.lagger = Lagger()
			self.irc = IRCBot("[kambot-logging]","","#kamaelia","kamaeliabot")
			self.kambot = Kambot("[kambot-logging]")
			self.client = TCPClient("irc.freenode.net", 6667, 1)
			self.writer = SimpleFileWriter("latest.txt")

			# IRC <-> Kambot
			self.link((self.irc, "heard"), (self.kambot, "inbox"))
			self.link((self.kambot, "outbox"), (self.irc, "command"))

			# Kambot -> file writer
			self.link((self.kambot, "log"), (self.writer, "inbox"))

			# TCP <-> IRC
			self.link((self.irc, "outbox"), (self.client, "inbox"))
			self.link((self.client, "outbox"), (self.irc, "inbox"))

			self.addChildren(self.lagger, self.irc, self.kambot, self.client, self.writer)
			yield Axon.Ipc.newComponent(*(self.children))
			while 1:
				self.pause()
				yield 1

	t = TestHarness()
	t.activate()
	scheduler.run.runThreads(slowmo=0)
	
