# WINDOWS
# =======

# The path to an extracted RtAudio source (with trailing slash)
# -------------------------------------------------------------
path = "/home/joe/sources/rtaudio-4.0.4/"

define_macros = []
libraries = []
sources = []
extra_link_args = []

# Uncomment the following lines for DirectSound support
# -----------------------------------------------------

define_macros.append(("__WINDOWS_DS__", ''))
libraries += ["dsound.lib", "winmm.lib"]

# Uncomment the following lines for ASIO support
# ----------------------------------------------

#define_macros.append(("__WINDOWS_ASIO__", ''))
#sources += [path + "asio/asio.cpp",
#            path + "asio/asiodrivers.cpp",
#            path + "asio/asiolist.cpp",
#            path + "asio/iasiothiscallresolver.cpp']


