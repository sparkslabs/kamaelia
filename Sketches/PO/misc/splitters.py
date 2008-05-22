#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

import Axon
from Axon.Ipc import producerFinished
from Kamaelia.Util.Splitter import PlugSplitter, Plug
from Kamaelia.Chassis.Pipeline import Pipeline

class Producer(Axon.Component.component):
	def __init__(self, **argv):
		super(Producer, self).__init__(**argv)

	def main(self):
		for i in range(10):
			msg = "hello %s" % i
			print "Sending msg <%s>" % msg
			self.send("hello %s" % i, "outbox")
			yield 1

		self.send(producerFinished(self), "signal")

class Consumer(Axon.Component.component):
	def __init__(self, name, **argv):
		super(Consumer, self).__init__(**argv)
		self.name = name

	def main(self):
		n = 0
		while True:
			while self.dataReady("inbox"):
				data = self.recv("inbox")
				n += 1
				print "Received: %s: %s" % (self.name, data)

			while self.dataReady("control"):
				data = self.recv("control")
				print "Control: %s: %s" % (self.name, data)
				self.send(producerFinished(self), "signal")
				return

			if not self.anyReady():
				self.pause()
			yield 1

class Forwarder(Axon.Component.component):
	Inboxes = {
		"inbox"             : "Received messages are forwarder to outbox",
		"secondary-inbox"   : "Received messages are forwarder to outbox",
		"control"           : "Received messages are forwarder to signal",
		"secondary-control" : "Received messages are forwarder to signal",
	}
	def __init__(self, name, **argv):
		super(Forwarder, self).__init__(**argv)
		self.name = name

	def main(self):
		while True:
			while self.dataReady("inbox"):
				data = self.recv("inbox")
				print "From inbox in forwarder %s: %s" % (self.name, data)
				self.send(data,"outbox")

			while self.dataReady("secondary-inbox"):
				data = self.recv("secondary-inbox")
				print "From secondary-inbox in forwarder: %s: %s" % (self.name, data)
				self.send(data,"outbox")

			while self.dataReady("control"):
				data = self.recv("control")
				print "From control in forwarder: %s: %s" % (self.name, data)
				self.send(data, "signal")
				return

			while self.dataReady("secondary-control"):
				data = self.recv("secondary-control")
				print "From control in secondary-control: %s: %s" % (self.name, data)
				self.send(data, "signal")
				return

			if not self.anyReady():
				self.pause()
			yield 1

if 0:
	mysplitter = PlugSplitter( Producer() )
	mysplitter.activate()

	Plug(mysplitter, Consumer("consumerA") ).activate()
	Plug(mysplitter, Consumer("consumerB") ).activate()

	mysplitter.run()

if 0:
	producer = Producer()
	mysplitter = PlugSplitter()
	pipe = Pipeline(producer, mysplitter)

	Plug(mysplitter, Consumer("consumerA") ).activate()
	Plug(mysplitter, Consumer("consumerB") ).activate()

	pipe.run()

if 1:
	mysplitter = PlugSplitter()
	pipe = Pipeline( Producer(), mysplitter )

	forwarder1  = Forwarder("forwarder")
	plug1       = Plug(mysplitter,forwarder1)
	plug1.activate()

	forwarder1b = Forwarder("forwarder1b")
	plug1.link((plug1,'outbox'),(forwarder1b,'secondary-inbox'))
	plug1.link((plug1,'signal'),(forwarder1b,'secondary-control'))
	consumer1   = Consumer("consumer1")
	Pipeline( 
			forwarder1b, 
			consumer1
	).activate()

	forwarder2 = Forwarder("forwarder2")
	plug2 = Plug(mysplitter, forwarder2)
	plug2.activate()

	forwarder2b = Forwarder("forwarder2b")
	plug2.link((plug2,'outbox'),(forwarder2b,'secondary-inbox'))
	plug2.link((plug2,'signal'),(forwarder2b,'secondary-control'))
	consumer2 = Consumer("consumer2")
	Pipeline( 
			forwarder2b,
			consumer2
	).activate()

#	import introspector
#	introspector.activate()

	pipe.run()

