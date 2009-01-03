# LINUX
# =====

# The path to an extracted RtAudio source
# ---------------------------------------
path = "/home/joe/sources/rtaudio-4.0.4/"

define_macros = []
libraries = []
sources = []
extra_link_args = []

# Uncomment the following lines for ALSA support
# ----------------------------------------------

define_macros.append(("__LINUX_ALSA__", ''))
libraries.append("asound")

# Uncomment the following lines for JACK support
# ----------------------------------------------

#define_macros.append(("__LINUX_JACK__", ''))
#libraries += ["jack", "asound", "rt"]

# Uncomment the following line for OSS support
# --------------------------------------------

#define_macros.append(("__LINUX_OSS__", ''))

