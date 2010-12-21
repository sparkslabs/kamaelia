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
from distutils.extension import Extension
from Pyrex.Distutils import build_ext

setup(
  name = 'Dirac',
  version = "0.0.2",
  description = "Dirac 0.6.0 bindings for python",
  author = "Michael",
  author_email = "ms_@users.sourceforge.net",
  url = "http://kamaelia.sourceforge.net/",
  ext_modules=[ 
    Extension("dirac_parser",
              ["dirac_parser.pyx"],
              libraries = ["dirac_decoder"],
              include_dirs = ["/usr/local/include/dirac"],
             ),
    Extension("dirac_encoder",
              ["dirac_encoder.pyx"],
              libraries = ["dirac_encoder"],
              include_dirs = ["/usr/local/include/dirac"],
             ),
    ],
  cmdclass = {'build_ext': build_ext},
  long_description = """Initial set of python bindings for Dirac 0.6.0 release. 
This API is subject to change. Requires Pyrex, Dirac, and Dirac
headers are expected to live in /usr/local/include/dirac
For information on dirac, see http://dirac.sf.net/
"""
)
