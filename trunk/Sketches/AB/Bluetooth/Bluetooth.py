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
#

from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import producerFinished, shutdownMicroprocess
from bluetooth import *
import sys
import time

class Bluetooth(threadedcomponent):
    '''
    Playing around with Bluetooth (PyBluez) - not currently in a useable state
    '''

    Inboxes = {"inbox":"Receives data back from the file writer",
               "control":""}
    Outboxes = {"outbox":"For sending data to the file writer",
                "signal":""}

    def shutdown(self):
       """Return 0 if a shutdown message is received, else return 1."""
       if self.dataReady("control"):
           msg=self.recv("control")
           if isinstance(msg,producerFinished) or isinstance(msg,shutdownMicroprocess):
               self.send(producerFinished(self),"signal")
               return 0
       return 1

    def discover(self,id=False,name=False):
        devices = discover_devices(lookup_names=True)
        if id:
            for device in devices:
                if device[0] == id:
                    self.send(["OK",device],"outbox")
                    break
            else:
                self.send(["ERROR",id])
        elif name:
            for device in devices:
                if device[1].lower() == name.lower():
                    self.send(["OK",device],"outbox")
                    break
            else:
                self.send(["ERROR",name])
        else:
            self.send(devices,"outbox")

    def senddata(self):
        pass

    def recvdata(self):
        pass

    def advertise(self):
        pass

    def main(self):
        # Accepts requests in the forms:
        # ['DISCOVER'] - returns [(device_id,device_name),(device_id,device_name)]
        # ['FINDBYID',device_id] - returns ["OK",(device_id,device_name)] or ["ERROR",device_id]
        # ['FINDBYNAME',device_name] - returns ["OK",(device_id,device_name)] or ["ERROR",device_name]
        while self.shutdown():
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                data[0] = data[0].upper()
                if data[0] == "DISCOVER":
                    self.discover()
                elif data[0] == "FINDBYID":
                    self.discover(id=data[1])
                elif data[0] == "FINDBYNAME":
                    self.discover(name=data[1])
            time.sleep(0.1)


if __name__=="__main__":
    Bluetooth().run()