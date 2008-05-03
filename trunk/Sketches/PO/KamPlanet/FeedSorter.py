#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess

def _check_l10n(x,y):
	for i in x,y:
		if i.updated_parsed is None:
			raise Exception("feedparser could not parse date format: %s; l10n problems? \
				Take a look at feedparser._parse_date_hungarian and feedparser.registerDateHandler" % i.updated
			) # TODO: Exception is just too generic

def _cmp_entries(x,y):
	""" Given two FeedParserDicts, compare them taking into account their updated_parsed fields """
	_check_l10n(x[1],y[1])
	for pos, val in enumerate(x[1].updated_parsed):
		result = cmp(val, y[1].updated_parsed[pos])
		if result != 0:
			return result * -1
	return 0

class FeedSorter(Axon.Component.component):
	Inboxes = {
		"inbox"         : "Information coming from the socket",
		"control"       : "From component...",
		"counter-inbox" : "Will receive the number of feeds through this channel"
	}
	Outboxes = {
		"outbox"     : "Information being sent to the socket",
		"signal"     : "From component..."
	}
	def __init__(self):
		super(FeedSorter, self).__init__()
		self._ordered_entries = []
		self._counter         = None
		self._counted         = 0
		self._max_posts       = 10 #TODO: configure me
		self._pleaseSleep     = False

	def mainBody(self):
		while self.dataReady("control"):
			data = self.recv("control")
			if isinstance(data, shutdownMicroprocess):
				self.send(data, "signal")
				return 0
			# TODO: Even if the producer finished, I want to wait 
			# until self._counted == self.counter
			# Is there any other way to handle this situation?

		while self.dataReady("inbox"):
			data = self.recv("inbox")
			self._ordered_entries.extend([ (data.feed, i) for i in data.entries ])
			self._ordered_entries.sort(_cmp_entries)
			self._ordered_entries = self._ordered_entries[:self._max_posts]
			self._counted += 1

		while self.dataReady("counter-inbox"):
			data = self.recv("counter-inbox")
			self._counter = data
		
		if self._counter is not None and self._counted >= self._counter:
			for entry in self._ordered_entries:
				self.send(entry, 'outbox')
			self.send(producerFinished(), 'signal')
			return 0

		if not self.anyReady():
			self.pause()
		return 1

