#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

PRINTER = 0
COMPONENT = 0
CONSUMER_PRODUCER = 0
MULTICAST_SENDER = 0

class microprocess(object):
	def __init__(self):
		super(microprocess, self).__init__()
	def main(self):
		yield 1


class scheduler(microprocess):
	def __init__(self):
		super(scheduler, self).__init__()
		self.active   = []
		self.newqueue = []

	def main(self):
		for i in xrange(100):
			yield 1
			for current in self.active:
				try:
					result = current.next()
				except StopIteration, si:
					pass
				else:
					if result != -1:
						self.newqueue.append(current)
			self.active   = self.newqueue
			self.newqueue = []

	def activateMicroprocess(self, someprocess):
		generator = someprocess.main()
		self.newqueue.append(generator)

if PRINTER:
	class printer(microprocess):
		def __init__(self, tag):
			super(printer, self).__init__()
			self.tag = tag
		def main(self):
			while 1:
				yield 1 # Must be a generator
				print self.tag

	X = printer("Hello World")

	Y = printer("Game Over") # Another well known 2 word phrase :-)

	myscheduler = scheduler()
	myscheduler.activateMicroprocess(X)
	myscheduler.activateMicroprocess(Y)
	for _ in myscheduler.main():
		pass

class component(microprocess):
	Boxes = {
			'inbox'  : 'comment',
			'outbox' : 'comment'
	}
	def __init__(self):
		super(component, self).__init__()

		self.boxes = {}

		for box in self.Boxes:
			self.boxes[box] = []

	def send(self, value, boxname):
		self.boxes[boxname].append(value)

	def recv(self, boxname):
		return self.boxes[boxname].pop(0)

	def dataReady(self, boxname):
		return len(self.boxes[boxname])

if COMPONENT:
	c = component()
	assert c.dataReady('outbox') == 0
	c.send('A','outbox')
	c.send('B','outbox')
	c.send('C','outbox')
	assert c.dataReady('outbox') == 3
	assert c.recv('outbox') == 'A'
	assert c.dataReady('outbox') == 2
	assert c.recv('outbox') == 'B'
	assert c.dataReady('outbox') == 1
	assert c.recv('outbox') == 'C'
	assert c.dataReady('outbox') == 0

class postman(microprocess):
	def __init__(self, source, sourcebox, sink, sinkbox):
		super(postman, self).__init__()
		self.source    = source
		self.sourcebox = sourcebox
		self.sink      = sink
		self.sinkbox   = sinkbox

	def main(self):
		while 1:
			yield 1
			if self.source.dataReady(self.sourcebox) > 0:
				data = self.source.recv(self.sourcebox)
				self.sink.send(data, self.sinkbox)

class Producer(component):
	def __init__(self, message):
		super(Producer,self).__init__()
		self.message = message
	def main(self):
		while 1:
			yield 1
			self.send(self.message, "outbox")
            
class Consumer(component):
	def main(self):
		count = 0
		while 1:
			yield 1
			count += 1 # This is to show our data is changing :-)
			if self.dataReady("inbox"):
				data = self.recv("inbox")
				print data, count
        
if CONSUMER_PRODUCER:
	p = Producer("Hello World")
	c = Consumer()
	postie = postman(p, "outbox", c, "inbox")

	myscheduler = scheduler()
	myscheduler.activateMicroprocess(p)
	myscheduler.activateMicroprocess(c)
	myscheduler.activateMicroprocess(postie)

	for _ in myscheduler.main():
		pass

if MULTICAST_SENDER:
	import socket

	class Multicast_sender(component):
		def __init__(self, local_addr, local_port, remote_addr, remote_port):
			super(Multicast_sender, self).__init__()
			self.local_addr = local_addr
			self.local_port = local_port
			self.remote_addr = remote_addr
			self.remote_port = remote_port

		def main(self):
			sock = socket.socket(
				socket.AF_INET, 
				socket.SOCK_DGRAM,
				socket.IPPROTO_UDP
			)
			sock.bind((self.local_addr,self.local_port))
			sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 10)
			while 1:
				if self.dataReady("inbox"):
					data = self.recv("inbox") #It didn't say "inbox"
					l = sock.sendto(data, (self.remote_addr,self.remote_port) );
				yield 1

	class FileReader(component):
		def __init__(self, filename):
			super(FileReader, self).__init__() #It said FileReadAdapter
			self.file = open(filename, "rb",0)
		def main(self):
			yield 1
			for line in self.file.xreadlines():
				self.send(line, "outbox")
				yield 1

	reader = FileReader("fortune.txt")
	sender = Multicast_sender("0.0.0.0", 0, "224.168.2.9", 1600)
	postie = postman(reader, "outbox", sender, "inbox")

	myscheduler = scheduler()
	myscheduler.activateMicroprocess(reader)
	myscheduler.activateMicroprocess(sender)
	myscheduler.activateMicroprocess(postie)

	for _ in myscheduler.main():
		pass

