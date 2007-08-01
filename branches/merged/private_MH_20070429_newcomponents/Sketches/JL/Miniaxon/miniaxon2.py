class microprocess(object):
	def __init__(self):
		super(microprocess,self).__init__(self)
	
	def main(self):
		yield 1

class weird_microprocess(microprocess):
	def __init__(self, n):
		super(microprocess,self).__init__(self)
	
	def main(self):
		count = n
		while count > 0:
			yield count
			print count
			count = count - 1
			

class scheduler(microprocess):
	def __init__(self):
		super(scheduler, self).__init__()
		self.active = [];
		self.newqueue = [];

	def main(self):
		i = 0
		while i < 100:
			i = i + 1
			print i
			for current in self.active:
				yield 1
				try:
					result = current.next()
				except StopIteration:
					pass
				if result is not -1:
					self.newqueue.append(current)
			self.active = self.newqueue
			self.newqueue = [];

	def activateMicroprocess(self, someprocess):
		activated = someprocess.main()
		self.newqueue.append(activated)

class component(microprocess):
	def __init__(self):
		super(component, self).__init__()
		self.boxes = {'inbox':[], 'outbox':[]}

	def send (self, value, boxname):
		self.boxes[boxname].append(value);

	def recv(self, boxname):
		data = self.boxes[boxname][0]
		del self.boxes[boxname][0]
		return data

	def dataReady(self, boxname):
		return len(self.boxes[boxname])

class postman(microprocess):
	def __init__(self, source, sourcebox, sink, sinkbox):
		super(postman, self).__init__()
		self.source = source
		self.sourcebox = sourcebox
		self.sink = sink
		self.sinkbox = sinkbox
	
	def main(self):
		while True:
			yield 1
			if self.source.dataReady(self.sourcebox):
				data = self.source.recv(self.sourcebox)
				self.sink.send(data, self.sinkbox)
					
def run():
	p = Producer("Hello World")
	c = Consumer()
	postie = postman(p, "outbox", c, "inbox")
	myscheduler.activateMicroprocess(p)
	myscheduler.activateMicroprocess(c)
	myscheduler.activateMicroprocess(postie)
	

		

