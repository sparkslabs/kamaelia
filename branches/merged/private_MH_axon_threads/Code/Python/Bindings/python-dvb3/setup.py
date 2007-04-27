import os
from distutils.core import setup
from distutils.extension import Extension
from Pyrex.Distutils import build_ext

kernel = "/lib/modules/" + os.uname()[2] + "/build/include"
incs = [kernel]

setup(
    name="python-dvb3", version="0.0.4",
    author="Paul Clifford", author_email="paul@clifford.cx",
    license="BSD",
    description="Python bindings for the Linux DVB v3 API",
    long_description="Python bindings for the Linux DVB v3 API.",
    url = "http://kamaelia.sourceforge.net/",
    py_modules=[
        "dvb3.__init__"
    ],
    ext_modules=[
        Extension("dvb3/frontend", ["dvb3/frontend.pyx"], include_dirs=incs),
        Extension("dvb3/dmx", ["dvb3/dmx.pyx"], include_dirs=incs),
    ],
    cmdclass={"build_ext": build_ext}
)
