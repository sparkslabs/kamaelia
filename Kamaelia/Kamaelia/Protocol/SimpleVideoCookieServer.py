#!/usr/bin/env python2.3
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
