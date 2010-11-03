# Oron Peled (Sun Jun 30 2002)
# Taken from libglade.m4

# a macro to get the libs/cflags for libvorbissimple

dnl AM_PATH_LIBVORBISSIMPLE([ACTION-IF-FOUND [, ACTION-IF-NOT-FOUND]])
dnl Test to see if libvorbissimple is installed, and define LIBVORBISSIMPLE_CFLAGS, LIBVORBISSIMPLELIBS
dnl
AC_DEFUN(AM_PATH_LIBVORBISSIMPLE,
[dnl
dnl Get the cflags and libraries from the vorbissimple-config script
dnl
AC_ARG_WITH(vorbissimple-config,
AC_HELP_STRING([--with-vorbissimple-config=LIBVORBISSIMPLE_CONFIG],[Location of vorbissimple-config]),
LIBVORBISSIMPLE_CONFIG="$withval")

AC_PATH_PROG(LIBVORBISSIMPLE_CONFIG, vorbissimple-config, no)
AC_MSG_CHECKING(for libvorbissimple)
if test "$LIBVORBISSIMPLE_CONFIG" = "no"; then
  AC_MSG_RESULT(no)
  ifelse([$2], , :, [$2])
else
  LIBVORBISSIMPLE_CFLAGS=`$LIBVORBISSIMPLE_CONFIG --cflags`
  LIBVORBISSIMPLE_LIBS=`$LIBVORBISSIMPLE_CONFIG --libs`
  AC_MSG_RESULT(yes)
  ifelse([$1], , :, [$1])
fi
AC_SUBST(LIBVORBISSIMPLE_CFLAGS)
AC_SUBST(LIBVORBISSIMPLE_LIBS)
])
