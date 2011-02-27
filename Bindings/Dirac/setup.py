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
# Please note that whilst these bindings are available under the Apache 2
# license, any usage or build of these bindings must inherit from the dirac
# bindings, and you'll be bound by your choice of the MPL/GPL/LGPL.  Since
# the LGPL boils down to something similar to the apache 2 license, this is
# unlikely to be an issue for you.
#
# In particular these bindings are able to be Apache 2 licensed because they
# dynamically link to the LGPL'd dirac code, and as a result don't modify
# the dirac code or include the dirac code directly in any way.
#


from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    name = 'Dirac',
    version = "1.0.2-0", # Bump revision to match dirac version that work for. 4th digit is local version number
    description = "Dirac 1.0.2 bindings for python",
    author = "Michael Sparks, Matt Hammond",
    author_email = "ms_@users.sourceforge.net",
    url = "http://www.kamaelia.org/Home.html",
    py_modules=[
                "dirac.__init__"
    ],
    ext_modules=[ 
                  Extension("dirac.dirac_parser",  ["dirac/dirac_parser.pyx"],  libraries = ["dirac_decoder"], include_dirs = ["/usr/include/dirac"] ),
                  Extension("dirac.dirac_encoder", ["dirac/dirac_encoder.pyx"], libraries = ["dirac_encoder"], include_dirs = ["/usr/include/dirac"] ),
      ],
    cmdclass = {'build_ext': build_ext},
    long_description = """Initial set of python bindings for Dirac 1.0.2 release. 
This API is subject to change. Requires Cython, Dirac, and Dirac
headers are expected to live in /usr/include/dirac
For information on dirac, see http://www.diracvideo.org/

This particular version is created with regard to Dirac and Cython as included
in Ubuntu 10.10
"""
)
