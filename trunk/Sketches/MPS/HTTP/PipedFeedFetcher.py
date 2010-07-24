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

import feedparser
import pprint
import Axon
import base64
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
from Kamaelia.Util.PureTransformer import PureTransformer

def AuthenticatedRequestStream(user, passwd):
    auth = "Basic %s" % base64.encodestring("%s:%s" % (user,passwd))[:-1]
    def AuthRequest(line):
        request = {"url":line, 
                   "extraheaders": {"Authorization": auth},
                  }
        return request
    return AuthRequest

import sys
username = sys.argv[1]
password = sys.argv[2]

Pipeline(
    ConsoleReader(eol=""),
    PureTransformer(AuthenticatedRequestStream(username, password)),
    SimpleHTTPClient(),
    PureTransformer(feedparser.parse),
    PureTransformer(pprint.pformat),
    ConsoleEchoer(),
).run()
