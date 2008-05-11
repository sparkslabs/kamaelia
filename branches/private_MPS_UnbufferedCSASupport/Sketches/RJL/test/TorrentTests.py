#!/usr/bin/env python
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

if __name__ == "__main__":
	import sys
	sys.path.append('bittorrent')
	from TorrentMaker import *
	from ChunkDistributor import *
	from Chunkifier import *
	from WholeFileWriter import *
	from Kamaelia.File.Reading import RateControlledFileReader
	from Axon.Scheduler import scheduler 

	from Kamaelia.Util.PipelineComponent import pipeline
	from Kamaelia.Util.ConsoleEcho import consoleEchoer

	import Axon
	from Axon.ThreadedComponent import threadedcomponent
	from Axon.Component import component
	from time import sleep
	from Lagger import Lagger
	
	class ReducedConsoleReader(threadedcomponent):
		def run(self):
			while 1:
				self.outqueues["outbox"].put( raw_input("> ") )
	
	class testComponent(component): 
		def main(self): 
			mylagger = Lagger(0.1)
			mysourcestream = RateControlledFileReader("streamingfile.mpg", "bytes", rate=1280000, chunksize=100000) #ReducedConsoleReader()
			mychunkifier = Chunkifier(5000000)
			mydistributor = ChunkDistributor("chunks/")
			myfilewriter = WholeFileWriter()
			mytorrentmakerthread = TorrentMaker( "http://localhost:6969/announce", "chunks/" )
			mytorrentmaker = pipeline( mytorrentmakerthread )
			myoutputconsole = consoleEchoer()
			"""
				mysourcestream -> mychunkifier -> mydistributor -> myfilewriter -> mytorrentmaker -> myoutputconsole
			"""

			self.link( (mysourcestream, "outbox"), (mychunkifier, "inbox") )
			self.link( (mychunkifier, "outbox"), (mydistributor, "inbox") )

			self.link( (mydistributor, "outbox"), (myfilewriter, "inbox") )
			#self.link( (myfilewriter, "outbox"), (mydistributor, "filecompletion") )
			#self.link( (mydistributor, "torrentmaker"), (mytorrentmaker, "inbox") )
			self.link ( (myfilewriter, "outbox"), (mytorrentmaker, "inbox") )
			self.link( (mytorrentmaker, "outbox"), (myoutputconsole, "inbox") )

			self.addChildren(mylagger, mysourcestream, mychunkifier, 
							mydistributor, myfilewriter, mytorrentmaker, 
							myoutputconsole) 
			yield Axon.Ipc.newComponent(*(self.children))
			while 1:
				self.pause()
				yield 1
	
	harness = testComponent() 
	harness.activate() 
	scheduler.run.runThreads(slowmo=0.1) 
 
