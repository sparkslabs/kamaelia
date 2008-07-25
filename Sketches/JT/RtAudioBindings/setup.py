from distutils.core import setup, Extension
import sipdistutils

setup(
  name = 'RtAudio',
  versione = '1.0',
  ext_modules=[
    Extension("RtAudio", ["RtAudio.sip", "RtAudio.cpp"], include_dirs=["."]),
    ],

  cmdclass = {'build_ext': sipdistutils.build_ext}

)
