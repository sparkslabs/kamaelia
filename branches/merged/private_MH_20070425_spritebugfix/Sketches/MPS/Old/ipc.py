#!/usr/bin/python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
#
# Earliest version of the component system with it's basic ideas.
#
#

class postman(dict):
	def __init__(self):
		self.linkages = []
	def register(self, name, component):
		self[name] = component
	def registerlinkage(self, thelinkage):
		self.linkages.append(thelinkage)
	def showqueuelengths(self):
		for componentname in self.keys():
			print "Component ", componentname, ": "
			for inbox in self[componentname].inboxes.keys():
				print "         inbox.", inbox, " : ", len(self[componentname].inboxes[inbox])
			for outbox in self[componentname].outboxes.keys():
				print "         outbox.", outbox, " : ", len(self[componentname].outboxes[outbox])
	def findrecipient(self,source, sourcebox):
		i = len(self.linkages)
		link = None;
		while i:
			link = self.linkages[i-1]
			if (link.source == source and link.sourcebox == sourcebox):
				(sink, sinkbox) = (link.sink, link.sinkbox)
				return (sink, sinkbox)
			i = i -1
		raise "None"
	def domessagedelivery(self):
		for componentname in self.keys():
			print "scanning outboxes of component ",componentname
			for outbox in self[componentname].outboxes.keys():
				if len(self[componentname].outboxes[outbox]) >0:
					try:
						(sink,sinkbox) = self.findrecipient(self[componentname], outbox)
						print "taking message from ", componentname, "outbox", outbox, " delivering to ", sink.name, " inbox ", sinkbox
						message = self[componentname].collect(outbox)
						sink.deliver(message,sinkbox)
					except:
						pass

class linkage:
	def __init__(self, source, sink, sourcebox="outbox", sinkbox="inbox",postoffice=None):
		self.source = source
		self.sink = sink
		self.sourcebox = sourcebox
		self.sinkbox = sinkbox
		if not (postoffice ==None):
			postoffice.registerlinkage(self)
	def show(self):
		print "source = ", self.source.name, "\t-\tsource box = ", self.sourcebox
		print "sink   = ", self.sink.name, "\t-\tsink box   = ", self.sinkbox

class component:
	def __init__(self,name,inboxes=["inbox"], outboxes=["outbox"],postoffice=None):
		""" name == name of component, inboxes == input queues, outboxes == output queues"""
		self.name = name
		self.inboxes = {}
		self.outboxes = {}
		for boxname in inboxes:
			self.inboxes[boxname] = []
		for boxname in outboxes:
			self.outboxes[boxname] = []
		self.postoffice = postman()
		if not (postoffice == None):
			postoffice.register(name,self)
		return self
	def recv(self,boxname="inbox"):
		""" Used by a component to recieve a message from the outside world.
		All comms goes via a named box/input queue"""
		result = self.inboxes[boxname][0]
		del self.inboxes[boxname][0]
		return result
	def send(self,message, boxname="outbox"):
		""" Used by a component to send a message to the outside world.
		All comms goes via a named box/output queue"""
		self.outboxes[boxname].append(message)
	def collect(self, boxname="outbox"):
		""" Used by a postman to collect messages to the outside world from
		a particular outbox of this component."""
		result = self.outboxes[boxname][0]
		del self.outboxes[boxname][0]
		return result
	def deliver(self,message,boxname="inbox"):
		""" Used by a postman to deliver messages from the outside world to
		a particular inbox of this component."""
		self.inboxes[boxname].append(message)

class Producer(component):
	def __init__(self):
		self = component.__init__(self, "Producer", [], ["result"])
	def doSomething(self):
		self.send("hello", "result")

class Consumer(component):
	def __init__(self):
		self.count = 0
		self = component.__init__(self, "Consumer", ["source"], ["result"])
	def doSomething(self):
		self.recv("source")
		self.count = self.count +1
		self.send(self.count, "result")


class testsystem(component):
	def __init__(self):
		self.producer = Producer()
		self.consumer = Consumer()
		self = component.__init__(self, "system", ["_output"], ["output"])
		self.postoffice.register("Producer", self.producer)
		self.postoffice.register("Consumer", self.consumer)
		self.postoffice.register("System", self)
		linkage(self.producer, self.consumer, "result", "source", self.postoffice)
		linkage(self.consumer,self,"result","_output", self.postoffice)
	def bibble(self,thing):
		if thing == "producer":
			self.producer.doSomething()
		if thing == "consumer":
			self.consumer.doSomething()
	def status(self):
		self.postoffice.showqueuelengths()
	def doSomething(self):
		level0.bibble("producer")
		self.postoffice.domessagedelivery()
		level0.bibble("consumer")
		if len(self.inboxes["_output"]) > 0:
			print "Result recieved from consumer!"
			result = self.recv("_output")
			print "Result is : ", result

level0=testsystem()
level0.status()
level0.doSomething()
level0.status()

class message:
	def __init__(self, recipient, payload, sender=None):
		self.recipient = recipient
		self.payload = payload
		self.sender = sender

