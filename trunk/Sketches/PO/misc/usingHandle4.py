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
class dummyComponent(Axon.Component.component):
    """A dummy component. Functionality: None. Prevents the scheduler from dying immediately."""
    def main(self):
        while True:
            self.pause()
            yield 1

def waitForLock(lock):
	initial_time = time.time()
	while time.time() - initial_time < 2:
		if lock.acquire(False):
			return True
		time.sleep(0.01)
	return False

class Foo(object):
	dummyComponent = None

	def initialize(self):
#		print "begin initialize..."
		
#		if not self._background_initialized:

		if Foo.dummyComponent is None:
			Foo.dummyComponent = dummyComponent().activate()
			if background.background.lock.acquire(False):
				background.background.lock.release()
				self.bg = background.background()
				self.bg.start()
			# We don't care anymore:
			#else:
			#	print "COULDN'T ACQUIRE BACKGROUND LOCK"
			#	sys.exit(2)
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
		#background.scheduler.run.stop()
		pass

f = Foo()

N=10

for _ in range(N):
	f.setUp()
	f.initialize()
	f.test()
	f.finish()

