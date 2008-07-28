from distutils.core import setup, Extension
import sipdistutils
import sys

try:
    if sys.platform == "win32":
        execfile("config.win32.py")
    elif sys.platform == "darwin":
        execfile("config.osx.py")
    else:
        # Assume we are in linux
        execfile("config.linux.py")
except IOError:
    sys.exit("Config file not found")

print sources, define_macros, libraries, extra_link_args

sources += ["RtAudio.sip", "NumpyInterface.cpp", path + "RtAudio.cpp"]

setup(
  name = 'RtAudio',
  version = '1.0',
  ext_modules=[
    Extension("RtAudio", sources = sources,
              include_dirs=[".", path, path + "asio"],
              define_macros = define_macros,
              libraries = libraries,
              extra_link_args = extra_link_args,
              ),

    ],

  cmdclass = {'build_ext': sipdistutils.build_ext}

)
