#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

import Axon
from Axon.Handle import Handle
import Axon.background as background
import time, sys
import Queue

class Reverser(Axon.Component.component):
    def main(self):
        while True:
            if self.dataReady('inbox'):
                item = self.recv('inbox')
                self.send(item[::-1], 'outbox')
            else: self.pause()
            yield 1

SECONDS = 5

def waitForLock(lock):
	initial_time = time.time()
	while time.time() - initial_time < 2:
		if lock.acquire(False):
			return True
		time.sleep(0.01)
	return False

class Foo(object):
	def initialize(self):
#		print "begin initialize..."
		
		if waitForLock(background.background.lock):
#			print "got it, releasing"
			background.background.lock.release()
#			print "new background..."
			self.bg = background.background(zap=True)
#			print "starting..."
			self.bg.start()
#			print "sleeping..."
			#time.sleep(1)
			self.bg.waitUntilSchedulerIsRunning()
		else:
			print "COULDN'T ACQUIRE BACKGROUND LOCK"
			sys.exit(2)
#		print "end initialize..."

	def setUp(self):
#		print "begin setUp..."
		r = Reverser()
		h = Handle(r)
		self.reverser = h.activate()
#		print "end setUp..."

	def test(self):
#		print "begin test..."
		self.reverser.put("hello world", "inbox")
		n = 0
		initial = time.time()
		while True:
			try:
				info = self.reverser.get("outbox")
			except Queue.Empty, e:
				n += 1
				if n % 1000 == 0:
					current = time.time()
					if current - initial > SECONDS:
						print "IT TOOK TOO LONG TO RETRIEVE A MESSAGE: %s seconds" % SECONDS
						sys.exit(1)
			else:
				if info != "dlrow olleh":
					print "UNEXPECTED INFO RETRIEVED: ",info
					sys.exit(3)
				else:
					print "SUCCESS"
				break
#		print "end test..."

	def finish(self):
		background.scheduler.run.stop()
		pass

f = Foo()

N=10

for _ in range(N):
	f.initialize()
	f.setUp()
	f.test()
	f.finish()

