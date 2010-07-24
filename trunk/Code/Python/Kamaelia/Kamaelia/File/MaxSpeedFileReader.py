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
"""\
==================================
Reading a file as fast as possible
==================================

MaxSpeedFileReader reads a file in bytes mode as fast as it can; limited only
by any size limit on the inbox it is sending the data to.

This component is therefore useful for building systems that are self rate
limiting - systems that are just trying to process data as fast as they can and
are limited by the speed of the slowest part of the chain.



Example Usage
-------------

Read "myfile" in in chunks of 1024 bytes. The rate is limited by the rate at
which the consumer component can consume the chunks, since its inbox has a size
limit of 5 items of data::

    consumer = Consumer()
    consumer.inboxes["inbox"].setSize(5)
    
    Pipeline( MaxSpeedFileReader("myfile", chunksize=1024),
              consumer,
            ).run()



More details
------------

Specify a filename and chunksize and MaxSpeedFileReader will read bytes from
the file in the chunksize you specified and send them out of its "outbox"
outbox.

If the destination inbox it is sending chunks to is size limited, then
MaxSpeedFileReader will pause until space becomes available. This is how the
speed at which the file is ingested is regulated - by the rate at which it is
consumed.

When the whole file has been read, this component will terminate and send a
producerFinished() message out of its "signal" outbox.

If a producerFinished message is received on the "control" inbox, this component
will complete sending any data that may be waiting. It will then send the
producerFinished message on out of its "signal" outbox and terminate.

If a shutdownMicroprocess message is received on the "control" inbox, this
component will immediately send it on out of its "signal" outbox and immediately
terminate. It will not complete sending on any pending data.

"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Axon.AxonExceptions import noSpaceInBox

class MaxSpeedFileReader(component):
    """\
    MaxSpeedFileReader(filename[,chunksize]) -> new MaxSpeedFileReader component.

    Reads the contents of a file in bytes mode; sending it out as fast as it can
    in chunks from the "outbox" outbox. The rate of reading is only limited by
    any size limit of the destination inbox to which the data is being sent.
    
    Keyword arguments:

    - filename   -- The filename of the file to read
    - chunksize  -- Optional. The maximum number of bytes in each chunk of data read from the file and sent out of the "outbox" outbox (default=32768)
    """

    def __init__(self, filename, chunksize=32768):
        super(MaxSpeedFileReader,self).__init__()
        self.filename=filename
        self.chunksize=chunksize

    def handleControl(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) and not isinstance(self.shutdownMsg, shutdownMicroprocess):
                self.shutdownMsg = msg
            elif isinstance(msg, shutdownMicroprocess):
                self.shutdownMsg = msg

    def canStop(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, (producerFinished,shutdownMicroprocess))

    def mustStop(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, shutdownMicroprocess)
    
    def waitSend(self,data,boxname):
        while 1:
            try:
                self.send(data,boxname)
                return
            except noSpaceInBox:
                if self.mustStop():
                    raise UserWarning( "STOP" )
                
                self.pause()
                yield 1
                
                if self.mustStop():
                    raise UserWarning( "STOP" )

    def main(self):
        self.shutdownMsg=""

        fh = open(self.filename,"rb")

        try:
            while 1:
                data = fh.read(self.chunksize)
                if data=="":
                    self.shutdownMsg=producerFinished(self)
                    raise UserWarning( "STOP" ) 

                for _ in self.waitSend(data,"outbox"):
                    yield _

                if self.mustStop():
                    raise UserWarning( "STOP" )

        except UserWarning( "STOP") :
            self.send(self.shutdownMsg, "signal")


__kamaelia_components__ = ( MaxSpeedFileReader, )
