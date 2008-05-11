#!/usr/bin/python
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""
Early test to see how viable generators were (on a fairly low end machine)

Simple program to text microprocesses and speed of context switching

This turns out to be a very fast method of introducing parallelism in a
highly lightweight, readable and scalable manner.

Results:
Num processes	#Switches/sec	Memory
3		23000		Low
100		23000		Low
1000		23000		2-3Mb
50000		22000		50Mb

ie about 1Mb per thousand microprocesses.

The idea of usage would be this:

	* You create a class that contains a "main" method, inheriting
	  from microprocess.
	* You then create instances of that class which you then give a
	  thread of control
	* You pass these threads of control to a "runner" which then runs
	  the threads, and handles IPC between the two.

"""

from __future__ import generators

class linear(list):
	"""Purpose of this class is to simply add clean functions to add/remove
	the first item in a list in order for it to also be used as a FIFO. By
	inheriting, we gain a list that has more in common with a Perl list"""
	def shift(self):
		r = self[0]
		del self[0:1]
		return r
	def unshift(self,value):
		self[0:1] = [value, self[0]]

class microprocess:
	"""Microprocess is an object for all sub processes to inherit from.
	   For a class to be runnable in this system, it simply needs to inherit
	   from this. It needs to be given a thread of control after this.

	   Attributes associated with a microprocess are:
			* microprocess id (mpid) - an internally assigned integer
			* name - if provided
			* inbox - this currently a linear - designed to be used as a FIFO.

		Microprocesses also have 2 statuses:
			* Runnable - the process gets cycles if this is true.
			* Stopped - the process has its thread of control removed if this is true

	   The mpid or name can be used in IPC, and a microprocess can ask
	   the system to awaken it when things things happen it's interested in.
	   We may extend this to it being awakened when it is sent messages. (maybe)

	 There is one class variable:
	 	maxid

	This is used to keep track of the last highest mpid. At present mpids are not reused,
	they might be in future.
	"""
	maxid = 0
	def __init__(self,name=""):
		"""A microprocess can be given a name - this is for IPC reasons
		between microprocesses. If you override this function, don't forget
		to run this function ala:
		   microprocess.__init(self)

		Internal attributes:
			* init - not used yet - flag to show whether initialised or not.
			* id - system assigned numeric mpid, based on class variable "maxid".
			* runnable - Flag to indicate whether this microprocess is runnable.
			   the idea is that processes can go to sleep and be awakened.
			* stopped - Flag to indicate the microprocess has come to a halt. It's thread
			   of control should be removed at the next available opportunity.
			* name - A user assigned name for this process.
			* inbox - This is a linear() type that contains new messages from other
			   microprocesses. Messages should be taken out of the inbox using
			   the "shift" method of the inbox. (probably change.) Not sure if just want
			   one inbox, or more than one at present. I'm suspecting we may actually
			   want more than one, and for them to be named.
			* outbox - A Linear type that contains new messages to be sent to other
			   microprocesses. Messages are added to the outbox using an append
			   method. Not entirely sure if a good idea at present :-)
		"""
		microprocess.maxid = microprocess.maxid  +1
		self.init  = 1
		self.id = microprocess.maxid
		self.runnable =1
		self.stopped = 0
		self.name=name
		self.inbox = linear()
	def setthread(self, thr):
		"""Internal function - don't override.

		This function is used by the microthread system to
		since it's useful for the microprocess to know it's microthread & vice versa.
		Currently this isn't used, but could be.
		"""
		self.thread = thr
	def isStopped(self):
		"""Internal function - don't override.

		This is used to determine whether this microprocess is halted or not.
		If the microprocess is halted it stops and it's thread of control exits."""
		return self.stopped == 1
	def isRunnable(self):
		"""Internal function - don't override.

		This is used to determine whether or not to run this microprocess or not. If
		the thread isn't runnable, it doesn't get run :-)"""
		return self.runnable == 1
	def stop(self):
		"This method halts a microprocess"
		self.stopped = 1
	def pause(self):
		"This method pauses a microprocess"
		self.runnable = 0
	def main(self):
		"""Entry point for all microprocesses, you should override this method in
		your subclass. The first thing you should do though is yield control back
		to the system however ala:
			"yield 1"
		"""
		yield 1
		return

class ipc:
	"""Abstract base class for Interprocess Communications.
	"""

class notify(ipc):
	"IPC class designed for sending messages to other microthreads."
	def __init__(self, caller, who, ipctype, payload):
		"""who - The name of the microprocess to send this message to
		ipctype - Defines a type for this message. (None defined yet)
		payload - The data to send as a message to the class. This payload is
			just one object, but can be any form of object.
		"""
		self.ipctype = ipctype
		self.object = payload
		self.who = who
		self.caller = caller

class wouldblock(ipc):
	"""This is defined as an IPC message to the external system that this
	microprocess would block if called. Currently this has no effect on the
	system.
	"""
	def __init__(self,caller):
		self.caller = caller

class runner:
	"""This class essentially acts as the system's task scheduler/thread
	of control handler. Generally you would only have one instance of
	this class and run it once. Having more than one wouldn't be an issue,
	however since a runner doesn't release the thread of control once it's
	started then having more than one is pretty pointless.

	Expected usage:
		threadfactory = uthread()
		r = runner()
		for i in range(5):
			p = myProcess(i)
			t = threadfactory.activate(p)
			r.addsthread(t)
		r.runThreads()

	ie You create your microprocesses and their threads of control,
	and add the threads of control to your runner. At that point
	you can then run your threads. At present their is no way to add
	extra threads of control to a running system. (Needs adding really)
	"""
	def __init__(self):
		"""Nothing special, creates a runner object, and assigns one
		Internal attributes:
		"""
		self.threads = []
	def addsthread(self, thr):
		self.thr = thr
		self.threads.append(thr)
	def runThreads(self):
		threads = self.threads
		context = 0
		# This next "try" is to catch control-C type situations. It was designed
		# so that I could benchmark # of context switches per second.
	 	try:
			while(1):
				newthreads = []
				for thr in threads:
					context = context +1
					try:
						thr.next()
						newthreads.append(thr)
					except StopIteration:
						pass
					threads=newthreads
		except:
			return context

class uthread:
	def activate(self,someobject):
		someobject.setthread = (self)
		pc = someobject.main()
		while(1):
			# Continually try to run the code, and then release control
			if someobject.isRunnable() :
				# If the object is runnable, we run the object
				v = pc.next()
				yield v
			else:
				# Microprocess is not running, has it stopped completely?
				if someobject.isStopped():
					# Microprocess has stopped
					yield None
					return
				else:
					# Microprocess simply paused
					yield "Paused"

class myProcess(microprocess):
	def main(self):
		yield wouldblock(self)
		while(1):
			#print self.name, ":", "hello World"
			yield notify(self,None, 10, "this")

if __name__ == '__main__':
	import time
	threadfactory = uthread()
	r = runner()
	for i in range(5):
		p = myProcess(i)
		t = threadfactory.activate(p)
		r.addsthread(t)

	t = time.time()
	context = r.runThreads()
	tt = time.time()
	diff = tt -t
	persec = context/diff
	print "START", t
	print "FINISH",time.time()
	print "DIFF", diff
	print "Context Switches", context
	print "per second", persec
