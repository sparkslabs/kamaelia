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
# Simple Ogg Vorbis audio streaming system
#

import Kamaelia.File.ReadFileAdaptor
from Kamaelia.Chassis.ConnectedServer import SimpleServer

file_to_stream = "../../SupportingMediaFiles/KDE_Startup_2.ogg"

def AdHocFileProtocolHandler(filename):
    class klass(Kamaelia.File.ReadFileAdaptor.ReadFileAdaptor):
        def __init__(self,*argv,**argd):
            super(klass,self).__init__(filename, readmode="bitrate", bitrate=400000)
    return klass

clientServerTestPort=1500

SimpleServer(protocol=AdHocFileProtocolHandler(file_to_stream),
             port=clientServerTestPort).run()
