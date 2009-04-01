#
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
  name = 'KamaeliaSupport',
  version = "0.0.1",
  description = "Support code for various Kamaelia components",
  author = "Matt",
  author_email = "matth_rd@users.sourceforge.net",
  url = "http://kamaelia.sourceforge.net/",
  packages = [
    "Kamaelia.Support.Optimised",
    "Kamaelia.Support.Optimised.Video",
    ],
  ext_modules=[ 
    Extension("Kamaelia.Support.Optimised.MpegTsDemux",
              ["Kamaelia/Support/Optimised/Kamaelia.Support.Optimised.MpegTsDemux.pyx"],
              libraries = [],
              include_dirs = [],
             ),
    Extension("Kamaelia.Support.Optimised.Video.ComputeMeanAbsDiff",
              ["Kamaelia/Support/Optimised/Video/Kamaelia.Support.Optimised.Video.ComputeMeanAbsDiff.pyx"],
              libraries = [],
              include_dirs = [],
             ),
    Extension("Kamaelia.Support.Optimised.Video.PixFormatConvert",
              ["Kamaelia/Support/Optimised/Video/Kamaelia.Support.Optimised.Video.PixFormatConvert.pyx"],
              libraries = [],
              include_dirs = [],
             ),
    ],
  cmdclass = {'build_ext': build_ext},
  long_description = """\
Various bits of optimised support code for various Kamaelia components.

"""
)
