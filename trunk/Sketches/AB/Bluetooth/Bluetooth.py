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
import bluetooth
#import sys
import time
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer, ConsoleReader
from Kamaelia.Util.PureTransformer import PureTransformer

class Bluetooth(threadedcomponent):
    '''
    Playing around with Bluetooth (PyBluez) - not currently in a useable state
    '''

    Inboxes = {"inbox":"Receives instructions / data to send",
               "control":""}
    Outboxes = {"outbox":"Sends out responses / data received",
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
        devices = bluetooth.discover_devices(lookup_names=True)
        if len(devices) > 0:
            services = bluetooth.find_service()
        if id:
            for device in devices:
                if device[0] == id:
                    localservices = list()
                    for service in services:
                        if service['host'] == device[0]:
                            localservices.append(service)
                    self.send(["OK",device,localservices],"outbox")
                    break
            else:
                self.send(["ERROR",id])
        elif name:
            for device in devices:
                if device[1] == name:
                    localservices = list()
                    for service in services:
                        if service['host'] == device[0]:
                            localservices.append(service)
                    self.send(["OK",device,localservices],"outbox")
                    break
            else:
                self.send(["ERROR",name])
        else:
            if len(devices) == 0:
                self.send(["ERROR","No Devices Found"],"outbox")
            else:
                self.send([devices,services],"outbox")

    def senddata(self):
        pass

    def recvdata(self):
        pass

    def advertise(self):
        pass

    def main(self):
        # Accepts requests in the forms:
        # ['DISCOVER'] - returns [[(device_id,device_name),(device_id,device_name)],[servicedict,servicedict]] or ["ERROR"]
        # ['FINDBYID',device_id] - returns ["OK",(device_id,device_name),[servicedict,servicedict]] or ["ERROR",device_id]
        # ['FINDBYNAME',device_name] - returns ["OK",(device_id,device_name),[servicedict,servicedict]] or ["ERROR",device_name]
        while self.shutdown():
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                cmd = data[0].upper()
                try:
                    if cmd == "DISCOVER":
                        self.discover()
                    elif cmd == "FINDBYID":
                        self.discover(id=data[1])
                    elif cmd == "FINDBYNAME":
                        self.discover(name=data[1])
                except IndexError:
                    self.send(["ERROR","Missing Argument"],"outbox")
            
            time.sleep(0.1)


if __name__=="__main__":
    Pipeline(ConsoleReader(),PureTransformer(lambda x: x.replace("\n","")),PureTransformer(lambda x: x.split(",")),Bluetooth(),ConsoleEchoer()).run()