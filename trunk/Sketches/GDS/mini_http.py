 #!/usr/bin/python

import os, string
from Axon.Component import component, scheduler, linkage
from Kamaelia.Util.PipelineComponent import pipeline
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.KamaeliaIPC import socketShutdown

class LocalFileServer(component):
	"""
	Listens to the inbox for paths. When it hears a path, cats the text of that file to the outbox.
	On recieving a shutdown or producerFinished control signal, passes it on and then shuts down.
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
			if isinstance(msg, producerFinished):
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

class gds(component):
	def __init__(self):
		super(gds, self).__init__()
			
	def main(self):
		self.send("/home/gareths/.bashrc","outbox")
		yield 1
		self.send( producerFinished(self), "signal" )
		yield 2

from Axon.Scheduler import scheduler

if __name__=="__main__":

	pipeline(gds(),
		LocalFileServer(),
		Printer()
		).activate()
		
	scheduler.run.runThreads()