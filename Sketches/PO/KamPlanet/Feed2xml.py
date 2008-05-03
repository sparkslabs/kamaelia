#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

import Axon

class Feed2xml(Axon.Component.component):
	def __init__(self):
		super(Feed2xml, self).__init__()

	def mainBody(self):
		while self.dataReady("control"):
			# TODO
			data = self.recv("control")
			print "%s: %s" % (type(self), data)
			self.send(data, "signal")
			return 0

		while self.dataReady("inbox"):
			data = self.recv("inbox")
			print "xml", data[1].updated

		if not self.anyReady():
			self.pause()

		return 1

