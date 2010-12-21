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
  name = 'MpegTsDemux',
  version = "0.0.1",
  description = "Fast demultiplexer for MPEG Transport Stream packets",
  author = "Matt",
  author_email = "matth_rd@users.sourceforge.net",
  url = "http://kamaelia.sourceforge.net/",
  ext_modules=[ 
    Extension("MpegTsDemux",
              ["MpegTsDemux.pyx"],
              libraries = [],
              include_dirs = [],
             ),
    ],
  cmdclass = {'build_ext': build_ext},
  long_description = """\
A fast software based demultiplexer for MPEG Transport Stream packets.
Written in pyrex using c datatypes to get the speed. 
"""
)
