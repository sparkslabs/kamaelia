import unittest

import sys; sys.path.append("../")
from mini_http import LocalFileServer
from Axon.Component import component, scheduler, linkage
from Kamaelia.Util.PipelineComponent import pipeline
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.KamaeliaIPC import socketShutdown

#### Testy thingies follow #########################################################

class Tester(component):
	def __init__(self, tester):
		super(Tester, self).__init__()
		self.tester = tester

	def main(self):
		done = False
		while not done:
			self.pause()
			yield 1

			if self.dataReady("inbox"):
				data = self.recv("inbox")
				self.tester.assertEqual(data, "line one\nline two \n")

			if self.dataReady("control"):
				msg = self.recv("control")
				if isinstance(msg, producerFinished):
					done = True
					self.send(msg, "signal")

class filePointer(component):
	def __init__(self):
		super(filePointer, self).__init__()
			
	def main(self):
		self.send("input.txt","outbox")
		yield 1
		self.send( producerFinished(self), "signal" )
		yield 2

#############################################################################

class LocalFileServer_Tests(unittest.TestCase):
	def test_Simple(self):
		# initially manual wotsit
		pipeline(filePointer(),
			LocalFileServer(),
			Tester(self)
			).activate()
		
		scheduler.run.runThreads()

if __name__=="__main__":
	unittest.main()