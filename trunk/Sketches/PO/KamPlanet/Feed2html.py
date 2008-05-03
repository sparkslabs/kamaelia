#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

import Axon

class Feed2html(Axon.Component.component):
	Inboxes = {
			'control'      : 'From component', 
			'inbox'        : 'Not used', 
			'feeds-inbox'  : 'Not used', 
			'config-inbox' : 'Not used'
		}
		
	def __init__(self):
		super(Feed2html, self).__init__()

	def mainBody(self):
		while self.dataReady("control"):
			# TODO
			data = self.recv("control")
			print "%s: %s" % (type(self), data)
			self.send(data, "signal")
			return 0

		while self.dataReady("feeds-inbox"):
			data = self.recv("feeds-inbox")
			print "html",data['entry'].updated

		while self.dataReady("config-inbox"):
			data = self.recv("config-inbox")
			self._config = data
			print "html-config", data.name, data.link

		if not self.anyReady():
			self.pause()

		return 1

