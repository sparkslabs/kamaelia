#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-*-*- encoding: utf-8 -*-*-
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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


