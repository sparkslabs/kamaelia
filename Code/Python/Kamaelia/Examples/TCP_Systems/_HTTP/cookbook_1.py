#!/usr/bin/python
# -*- coding: utf-8 -*-
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
"""
This example demonstrates using the Minimal file handler for
serving static web content.

System Requirements
-------------------
This example requires a UNIX operating system.
"""


# Import socket to get at constants for socketOptions
import socket

# Import the server framework, the HTTP protocol handling and the minimal request handler

from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Protocol.HTTP.Handlers.Minimal import MinimalFactory
from Kamaelia.Support.Protocol.HTTP import HTTPProtocol

# Our configuration

homedirectory = "/var/www/html/"
indexfilename = "index.html"

#Here we define our routing.  This tells us that the root of the server will run
#the minimal request handler, a static file server.
routing = [
    ['/', MinimalFactory(indexfilename, homedirectory)]
    ]

# Finally we create the actual server and run it.

ServerCore(protocol=HTTPProtocol(routing),
             port=8082,
             socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  ).run()
