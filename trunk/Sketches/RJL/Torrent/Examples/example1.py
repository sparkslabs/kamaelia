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

from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

import sys
sys.path.append("../../")
sys.path.append("../../Util")
sys.path.append("../../HTTP")
sys.path.append("../../Torrent")

from DataSource import DataSource
from OnDemandIntrospector import OnDemandIntrospector

from TorrentClient import TorrentClient, BasicTorrentExplainer
from TorrentMaker import TorrentMaker

if __name__ == '__main__':
    
    # seed a file
    pipeline(
        ConsoleReader(">>> ",""),
        TorrentMaker("http://localhost:6969/announce"),
        TorrentPatron(),
        BasicTorrentExplainer(),
        ConsoleEchoer()
        #TorrentPatron(),
        #BasicTorrentExplainer(),
        #ConsoleEchoer(),    
    ).run()
