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

from distutils.core import setup

setup(
    name = "Kamaelia.Community.RJL",
    version = "0.1.0",
    description = "Kamaelia - Multimedia & Server Development Kit",
    author = "Ryan Lothian",
    author_email = "celestialryan@users.sourceforge.net",
    url = "http://kamaelia.sourceforge.net/",
    packages = [
        "Kamaelia",
        "Kamaelia.Community",
        "Kamaelia.Community.RJL",
        "Kamaelia.Community.RJL.Kamaelia",
        "Kamaelia.Community.RJL.Kamaelia.Protocol",
        "Kamaelia.Community.RJL.Kamaelia.Protocol.Torrent",        
        "Kamaelia.Community.RJL.Kamaelia.Protocol.HTTP",
        "Kamaelia.Community.RJL.Kamaelia.Protocol.HTTP.Handlers",
        "Kamaelia.Community.RJL.Kamaelia.Util",
        "Kamaelia.Community.RJL.Kamaelia.IPC",
        "Kamaelia.Community.RJL.Kamaelia.File"
    ],
    long_description = """
"""
)
