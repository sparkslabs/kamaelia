#!/usr/bin/env python
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

import sys

if len(sys.argv) >= 2:
    if "install" in sys.argv:
        try:
            import os
            for dir in sys.path:
                if dir == "": continue
                if os.path.exists(dir+"/Axon/Axon.py"):
                    print("You have an older version of Axon installed that has an")
                    print("internal incompatibility with current codebase.  I am removing")
                    print("Axon/Axon.py to fix this issue.  This should not affect any code")
                    print("that uses Axon.")
                    print("")
                    print("I am moving it to Axon/Old_Axon.py")
                    try:
                        # Remove any old and busted version of Axon.py
                        os.rename(dir+"/Axon/Axon.py", dir+"/Axon/Old_Axon.py")
                    except:
                        # If that fails for any reason, we either don't have permission, or Axon wasn't installed.
                        pass
                
        except:
            # Axon wasn't installed beforehand, so there won't be a problem
            pass

setup(name = "Axon",
      version = "1.7.0",
      description = "Axon - Asynchronous Isolated Generator Component System",
      author = "Kamaelia Contributors.",
      author_email = "sparks.m@gmail.com",
      url = "http://www.kamaelia.org/",
      license ="Apache Software License",
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
