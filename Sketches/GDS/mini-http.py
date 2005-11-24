 #!/usr/bin/env/python
import os, string
from Axon.Component import component, scheduler, linkage
from Kamaelia.Util.PipelineComponent import pipeline

class LocalFileServer(component):
	"""
	Listens to the inbox for paths. When it hears a path, cats the text of that file to the outbox.
	On recieving a shutdown control signal, passes it on and then shuts down.
	"""
	
	Inboxes=["inbox","control"]
	Outboxes=["outbox","signal"]
	
	def __init__(self):
		super(LocalFileServer, self).__init__()
		
	def mainBody(self):
		if self.dataReady("control"):
			msg = self.recv("control")
			if isinstance(msg, socketShutdown):
				self.send(msg, "signal")
				return 0
		
		if self.dataReady("inbox"):
			path = self.recv("inbox")
			f = open(path, "r")
			self.send(f.read(), "outbox")
			f.close()
		
		return 1
		
#### Testy thingies follow

class Printer(component):
	def __init__(self):
		super(Printer, self).__init__()

	def main(self):
		done = False
		while not done:
			self.pause()
			yield 1

			if self.dataReady("inbox"):
				data = self.recv("inbox")
				print data

			if self.dataReady("control"):
				msg = self.recv("control")
				if isinstance(msg, producerFinished):
					done = True
					self.send(msg, "signal")
#    print "BYEBYE"


class gds(component):
	def __init__(self):
		super(gds, self).__init__()
			
	def main(self):
		yield 1
		self.send("~/.bashrc","outbox")
		yield 1
		self.send(socketShutdown(), "signal")

if __name__=="__main__":
	
	print "First bit\n"
	m = 
	
	pipeline(gds(),
		LocalFileServer(),
		Printer()
		).activate()