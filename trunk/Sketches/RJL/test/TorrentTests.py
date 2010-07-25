#!/usr/bin/env python
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
 
