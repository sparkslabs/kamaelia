from distutils.core import setup
from distutils.extension import Extension
from Pyrex.Distutils import build_ext

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
