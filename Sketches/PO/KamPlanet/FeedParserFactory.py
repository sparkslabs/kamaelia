#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

import Axon
import feedparser
from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
from Kamaelia.Chassis.Pipeline import Pipeline
from Axon.Ipc import producerFinished, shutdownMicroprocess

class Feedparser(Axon.Component.component):
	def mainBody(self):
		while self.dataReady("inbox"):
			data = self.recv("inbox")
			parseddata = feedparser.parse(data)
			self.send(parseddata, "outbox")

		while self.dataReady("control"):
			data = self.recv("control")
			self.send(data,"signal")
			return 0

		if not self.anyReady():
			self.pause()
		return 1

def makeFeedParser(feedUrl):
	# TODO: Is there any other way to send information to a inbox?
	simple_http_client = SimpleHTTPClient()
	simple_http_client.inboxes['inbox'].append(feedUrl)
	simple_http_client.inboxes['control'].append(producerFinished())
	return Pipeline(
			simple_http_client,
			Feedparser()
		)

class FeedParserFactory(Axon.Component.component):
	Inboxes = {
		"inbox"         : "Information coming from the socket",
		"control"       : "From component...",
		"parsed-feeds"  : "Feedparser drops here the feeds" 
	}

	def __init__(self):
		super(FeedParserFactory, self).__init__()
		self.mustStop = None
		self.pleaseStop = None

	def checkControl(self): #taken from Carousel.py
		while self.dataReady("control"):
			msg = self.recv("control")
			if isinstance(msg,producerFinished):
				self.pleaseStop = msg
			elif isinstance(msg,shutdownMicroprocess):
				self.mustStop = msg
		return self.mustStop, self.pleaseStop

	def handleChildTerminations(self): #taken from Carousel.py
		for child in self.childComponents():
			if child._isStopped():
				self.removeChild(child)

	def mainBody(self):
		# TODO: make two states, just as in Carousel.py, to avoid new parsed-feeds
		# /inbox when pleaseStop != None
		mustStop, pleaseStop = self.checkControl()
		if mustStop:
			self.send(mustStop,"signal")
			return 0

		self.handleChildTerminations()

		while self.dataReady("inbox"):
			feed = self.recv("inbox")
			child = makeFeedParser(feed)
			self.link( (child, 'outbox'), (self, 'parsed-feeds') )
			self.addChildren(child)
			child.activate()
			return 1

		while self.dataReady("parsed-feeds"):
			parseddata = self.recv("parsed-feeds")
			self.send(parseddata,"outbox")
			return 1

		if pleaseStop and len(self.childComponents()) == 0:
			self.send(pleaseStop,"signal")
			return 0

		if not self.anyReady():
			self.pause()
		return 1

