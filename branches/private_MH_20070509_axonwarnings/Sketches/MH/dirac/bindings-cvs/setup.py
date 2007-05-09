#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
from distutils.core import setup
from distutils.extension import Extension
from Pyrex.Distutils import build_ext

setup(
  name = 'Dirac',
  version = "0.0.1",
  description = "Dirac bindings for python",
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
  long_description = """Initial set of python bindings for Dirac. 
This API is subject to change. Requires Pyrex, Dirac, and Dirac
headers are expected to live in /usr/local/include/dirac
For information on dirac, see http://dirac.sf.net/
"""
)
