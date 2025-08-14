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


from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

if 1:
    extensions = [
        Extension("vorbissimple",
                  ["vorbissimple.pyx"],
                  libraries = ["vorbissimple"],
                ),
    ]
else:
    extensions = [
          Extension("vorbissimple",
                    ["vorbissimple.pyx"],
                    libraries=["vorbissimple"],
                    extra_compile_args=["-O0","-g","-fno-omit-frame-pointer","-fsanitize=address,undefined"],
                    extra_link_args=["-fsanitize=address,undefined"]
          )
    ]



setup(
  name = 'Vorbissimple',
  ext_modules=cythonize(extensions, gdb_debug=True),
  cmdclass = {'build_ext': build_ext}
)

# =========================================================================================

if 0:


    from distutils.core import setup
    from distutils.extension import Extension
    # from Pyrex.Distutils import build_ext
    from Cython.Distutils import build_ext

    setup(
      name = 'Vorbissimple',
      ext_modules=[
        Extension("vorbissimple",
                  ["vorbissimple.pyx"],
                  libraries = ["vorbissimple"]
                ),
        ],
      cmdclass = {'build_ext': build_ext}
    )
