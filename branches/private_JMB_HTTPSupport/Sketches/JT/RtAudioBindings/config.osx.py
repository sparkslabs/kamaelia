# WINDOWS
# =======

# The path to an extracted RtAudio source (with trailing slash)
# -------------------------------------------------------------
path = "/home/joe/sources/rtaudio-4.0.4/"

define_macros = []
libraries = []
sources = []
extra_link_args = []

# Uncomment the following lines for CoreAudio support
# -----------------------------------------------------

define_macros.append(("__MACOSX_CORE__", ''))
extra_link_args += ["-framework", "CoreAudio", "-framework", "CoreFoundation"]

