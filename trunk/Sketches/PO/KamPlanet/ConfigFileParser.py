#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

import Axon
from Axon.Ipc import producerFinished

class ConfigFileParser(Axon.Component.component):
	Outboxes = {
		"outbox"           : "Information being sent to the socket",
		"signal"           : "From component...",
		"counter-outbox"   : "Will announce how many feeds were found through this channel"
	}

	def __init__(self):
		super(ConfigFileParser, self).__init__()
		# TODO: First version, I should parse a configuration file or sth :-)
		self.__ptr = 0
		self._feeds = [
			'http://pablo.ordunya.com/weblog/feed/',
			'http://pablo.ordunya.com/weblog/feed/',
			'http://pablo.ordunya.com/weblog/feed/',
			'http://pablo.ordunya.com/weblog/feed/',
		]
		self._counter      = 0
		self._counter_sent = False

	def mainBody(self):
		if len(self._feeds) <= self._counter:
			if not self._counter_sent:
				self.send(len(self._feeds), 'counter-outbox')
				self._counter_sent = True
				return 1
			self.send(producerFinished(), "signal")
			return 0

		if len(self._feeds) > self.__ptr:
			feed = self._feeds[self.__ptr]
			self.__ptr = self.__ptr + 1
			self.send(feed,"outbox")
			self._counter = self._counter + 1
			return 1
		
		if not self.anyReady():
			self.pause()

		return 1

