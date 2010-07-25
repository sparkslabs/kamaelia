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

setup(name = "Axon",
      version = "1.5.1",
      description = "Axon - Asynchronous Isolated Generator Component System",
      author = "Michael",
      author_email = "ms_@users.sourceforge.net",
      url = "http://kamaelia.sourceforge.net/",
      license = "Copyright (c)2004 BBC & Kamaelia Contributors, All Rights Reserved. Use allowed under MPL 1.1, GPL 2.0, LGPL 2.1",
      packages = [
                  "Axon", ### START
                  "Axon.experimental", ### LAST
                  ],
      long_description = """
Axon is a software component system. In Axon, components are active and
reactive, independent processing nodes responding to a CSP-like environment.
Systems are composed by creating communications channels (linkages) between
components.
"""
      )
