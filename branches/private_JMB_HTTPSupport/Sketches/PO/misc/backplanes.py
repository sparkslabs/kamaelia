#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

import Axon

from Axon.Ipc import producerFinished
from Kamaelia.Util.Backplane import PublishTo, SubscribeTo, Backplane
from Kamaelia.Chassis.Pipeline import Pipeline

class Producer(Axon.Component.component):
	def __init__(self, **argv):
		super(Producer, self).__init__(**argv)

	def main(self):
		for i in range(10):
			self.send("hello %s" % i, "outbox")
			yield 1

		self.send(producerFinished(self), "signal")

class Consumer(Axon.Component.component):
	def __init__(self, **argv):
		super(Consumer, self).__init__(**argv)

	def main(self):
		n = 0
		while True:
			if self.dataReady("inbox"):
				data = self.recv("inbox")
				n += 1
				print "Received: %s" % data
				yield 1

			if self.dataReady("control"):
				data = self.recv("control")
				print "Control: %s" % data
				self.send(producerFinished(self), "signal")
				return

			#if not self.anyReady():
			#	self.pause()
			yield 1

backplane = Backplane("SAMPLE")
backplane.activate()

producer  = Producer()
consumer  = Consumer()
published = PublishTo("SAMPLE")
subscribe = SubscribeTo("SAMPLE")

pipe1 = Pipeline( 
	producer,
	published,
)
pipe1.activate()

pipe2 = Pipeline(
	subscribe,
	consumer
)

consumer2 = Consumer()
consumer2.activate()

pipe1.link((pipe1,'signal'),(pipe2,'control'))
pipe2.link((pipe2,'signal'),(backplane,'control'))
backplane.link((backplane,'signal'),(consumer2,'control'))

import threading
class A(threading.Thread):
	def run(self):
		someStopped = False
		injected    = False
		while 1:
			print "<whatever>"

			someRunning = False
			for i in (producer, consumer, published, subscribe, pipe1, pipe2, backplane):
				print i._isStopped(), i
				if i._isStopped():
					someStopped = True
				else:
					someRunning = True
			print "</whatever>"
			if not someRunning:
				print "No process running"
				return
			import time
			time.sleep(1)
			#if someStopped and not injected:
			#	print "Injecting"
			#	print "Injecting"
			#	print "Injecting"
			#	pipe2._deliver(producerFinished())
			#	injected = True
			#	time.sleep(1)
a = A()
a.setDaemon(1)
a.start()

pipe2.run()


