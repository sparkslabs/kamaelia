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

from Kamaelia.Util.DataSource import DataSource
from Kamaelia.Protocol.HTTP.HTTPClient import SingleShotHTTPClient, SimpleHTTPClient
from HTTPClient import SingleShotHTTPClient, SimpleHTTPClient
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.XML.SimpleXMLParser import SimpleXMLParser
from HTTPDataParser import HTTPDataParser

Pipeline(
    DataSource(["http://jibbering.com/foaf.rdf"]),
    SimpleHTTPClient(),
    #SingleShotHTTPClient("http://www.w3.org/2007/08/pyRdfa/extract?uri=http://apassant.net/about/#alex"),
    #SimpleXMLParser(),
    HTTPDataParser(),
    ConsoleEchoer()
).run()
