#!/usr/bin/python
# -*- coding: utf-8 -*-
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
"""
Simple Video based fortune cookie server


To watch the video, on a linux box do this:

netcat <server ip> 1500 | plaympeg -2 -

"""

from Kamaelia.Chassis.ConnectedServer import SimpleServer

from Axon.Component import component, scheduler, linkage, newComponent
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
import sys

class HelloServer(component):
	Inboxes=["datain","inbox","control"]
	Outboxes=["outbox"]
	maxid = 0
	def __init__(self,filename="Ulysses", debug=0):
		self.filename=filename
		self.debug = debug
		#self.__class__.maxid = self.__class__.maxid + 1
		#id = str(self.__class__) + "_" + str(self.__class__.maxid)
		super(HelloServer, self).__init__()
#		component.__init__(self, id, inboxes=["datain","inbox"], outboxes=["outbox"])

	def initialiseComponent(self):
		myDataSource = ReadFileAdaptor(filename="/video/sample-100.mpg",
					readmode="bitrate",
					bitrate=375000, chunkrate=24 )
		linkage(myDataSource,self,"outbox","datain", self.postoffice)
		self.addChildren(myDataSource)

		return newComponent( myDataSource )

	def handleDataIn(self):
		if self.dataReady("datain"):
			data = self.recv("datain")
			if self.debug:
				sys.stdout.write(data)
			self.send(data,"outbox")
		return 1

	def handleInbox(self):
		if self.dataReady("inbox"):
			data = self.recv("inbox")
			self.send(data,"outbox")
		return 1

	def mainBody(self):
		self.handleDataIn()
		self.handleInbox()
		return 1

__kamaelia_components__  = ( HelloServer, )


if __name__ == '__main__':

   SimpleServer(protocol=HelloServer, port=5222).activate()
   # HelloServer(debug = 1).activate()
   scheduler.run.runThreads(slowmo=0)
