#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-*-*- encoding: utf-8 -*-*-
# 
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
# -------------------------------------------------------------------------
# Licensed to the BBC under a Contributor Agreement: PO

"""
This code has been adapted from the simplebtconsole.py of Nokia Python for S60.

It shouldn't be used but for debugging purposes. Call "start_debugger()" to run a single-thread 
socket server which will provide, *with no password* a Python console to the client.
From this Python console, the user will be able to interact with any structure running at the time.
"""

import sys
import socket
import code
import threading

class RtDebugger(object):
	def __init__(self,sock):
		super(RtDebugger,self).__init__()
		self.socket=sock
	def read(self,n=1):
		return self.socket.recv(n).replace('\r\n','\n')
	def write(self,str):
		return self.socket.send(str.replace('\n','\r\n'))
	def readline(self,n=None):
		buffer=[]
		while 1:
			ch=self.read(1)
			if len(ch) == 0:
				break
			if ch == '\n' or ch == '\r':
				buffer.append('\n')
				self.write('\n')
				break
			if ch == '\177' or ch == '\010':
				self.write('\010 \010')
				del buffer[-1:]
			else:
				self.write(ch)
				buffer.append(ch)
			if n and len(buffer)>=n:
				break
		return ''.join(buffer)
	def raw_input(self,prompt=""):
		self.write(prompt)
		return self.readline()
	def flush(self):
		pass

class Debugger(threading.Thread):
	def __init__(self, port):
		threading.Thread.__init__(self)
		self.port = port
	def run(self):
		sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

		sock.bind(('localhost',self.port))
		sock.listen(5)

		while True:
			s, address = sock.accept()
			print "Conection from %s" % str(address)

			socketio = RtDebugger(s)

			realio = sys.stdout, sys.stdin, sys.stderr
			sys.stdout,sys.stdin,sys.stderr = socketio,socketio,socketio

			try:
				try:
					code.interact()
				finally:
					sys.stdout, sys.stdin, sys.stderr = realio
			except Exception,e:
				print e
		sock.close()

def launch_debugger(port):
	dbg = Debugger(port)
	dbg.setDaemon(True)
	dbg.start()
