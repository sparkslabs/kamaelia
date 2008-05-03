#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

import Axon
from Axon.Ipc import producerFinished

# TODO: maybe ConfigFileParser shouldn't handle GeneralConfig
# There could be a FeedConfigFileParser which would parse a file full of feeds
# And a GeneralConfigFileParser which would parse a file with general configuration 
# (and would use Backplanes)

class GeneralConfig(object):
	def __init__(self,  name, link):
		self.name = name
		self.link = link

class ConfigFileParser(Axon.Component.component):
	Outboxes = {
		"outbox"           : "Not used",
		"signal"           : "From component...",
		"feeds-outbox"     : "Feeds",
		"config-outbox"    : "General configuration",
		"counter-outbox"   : "Will announce how many feeds were found through this channel"
	}

	def __init__(self):
		super(ConfigFileParser, self).__init__()
		# TODO: First version, I should parse a configuration file or sth :-)
		# Right now all the config has been hardcoded
		self.__ptr = 0
		self._feeds = [
			'http://pablo.ordunya.com/weblog/feed/',
			'http://pablo.ordunya.com/weblog/feed/',
			'http://pablo.ordunya.com/weblog/feed/',
			'http://pablo.ordunya.com/weblog/feed/',
		]
		self._counter      = 0
		self._counter_sent = False
		self._config       = GeneralConfig("Kamaelia Planet", "http://somewhere/")
		self._config_sent  = False

	def mainBody(self):
		if len(self._feeds) <= self._counter:
			if not self._counter_sent:
				self.send(len(self._feeds), 'counter-outbox')
				self._counter_sent = True
				return 1
			if not self._config_sent:
				self.send(self._config,  'config-outbox')
				self._config_sent = True
				return 1
			self.send(producerFinished(), "signal")
			return 0

		if len(self._feeds) > self.__ptr:
			feed = self._feeds[self.__ptr]
			self.__ptr = self.__ptr + 1
			self.send(feed,"feeds-outbox")
			self._counter = self._counter + 1
			return 1
		
		if not self.anyReady():
			self.pause()

		return 1

