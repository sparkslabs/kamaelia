dnl
dnl Configure.ac for vorbissimple
dnl

dnl Process this file with autoconf to produce a configure script.
AC_INIT(vorbissimple, 0.0.1)
AC_CONFIG_SRCDIR(src/simple_decoder.c)
AM_INIT_AUTOMAKE([no-define])

dnl
dnl Require autoconf version 2.57
dnl
AC_PREREQ(2.57)

dnl The libtool version numbers (LT_*); Don't even think about faking this!
dnl
dnl immediately before every release do:
dnl ===================================
dnl if (the interface is totally unchanged from previous release)
dnl    LT_REVISION ++;
dnl else { /* interfaces have been added, removed or changed */
dnl    LT_REVISION = 0;
dnl    LT_CURRENT ++;
dnl    if (any interfaces have been _added_ since last release)
dnl       AGE ++;
dnl    if (any interfaces have been _removed_ or _incompatibly changed_)
dnl       AGE = 0;
dnl }
LT_CURRENT=4
LT_AGE=2
LT_REVISION=7


#######################################
dnl
dnl see if we have a mkdir that supports -p'.
dnl
AC_PATH_PROGS(MKDIR, mkdir, mkdir)
AC_MSG_CHECKING(if $MKDIR supports -p)
rm -rf conftest
$MKDIR -p conftest/a 2>/dev/null
if test $? = 0 ; then
	rmdir conftest/a 2>/dev/null
	if test $? = 0  ; then
		:
	else
		MKDIR_P=0
	fi

	rmdir conftest 2>/dev/null
	if test $? = 0 ; then
		MKDIR_P="$MKDIR -p"
	else
		MKDIR_P=0
	fi
else
	MKDIR_P=0
fi

if test X"$MKDIR_P" = X0 ; then
	AC_MSG_RESULT(no)
	MKDIR_P="`echo ${prefix}/lib/rpm/mkinstalldirs`"
else
	AC_MSG_RESULT(yes)
fi
dnl
dnl substitute this into config.h, so the C source picks it up.
dnl
AC_DEFINE_UNQUOTED(MKDIR_P, "${MKDIR_P}")
AC_SUBST(MKDIR_P)
########################################


AC_SUBST(LT_CURRENT)
AC_SUBST(LT_AGE)
AC_SUBST(LT_REVISION)

AM_MAINTAINER_MODE

dnl Checks for programs.
AC_PROG_CC
AC_PROG_INSTALL
AC_PROG_LN_S
AM_PROG_LIBTOOL
#### AC_PATH_XTRA
# We need two libtools, one that builds both shared and static, and
# one that builds only static.  This is because the resulting libtool
# does not allow us to choose which to build at runtime.
sed -e 's/^build_old_libs=yes/build_old_libs=no/' libtool > libtool-disable-static
chmod +x libtool-disable-static

LIBS="$LIBS $X_PRE_LIBS $X_LIBS $X_EXTRA_LIBS"
CFLAGS="$CFLAGS $X_CFLAGS -Wall"
M4DATADIR="$datadir/aclocal"
AC_SUBST(M4DATADIR)

dnl Checks for libraries.
#AC_CHECK_LIB(vorbis, vorbis_info_init,,
#	     AC_MSG_ERROR([*** libvorbis appears to be missing ***]))
### AC_CHECK_LIB(m, cos,
###                     [LIBS="$LIBS -lm"
###                      AC_DEFINE(HAVE_LIBM,1,[Define this if you have libm installed])
###                      ac_have_libm="yes"],
###	     AC_MSG_ERROR([*** cos does not appear to exist in libm, vorbis might not work! ***]))
AC_SEARCH_LIBS(cos, m, [LIBS="$LIBS -lm"], [
    AC_MSG_WARN([cos() not found in math library, vorbis installation may not work])
])

AC_CHECK_LIB(vorbis, vorbis_info_init,
                     [LIBS="$LIBS -lvorbis"
                      AC_DEFINE(HAVE_VORBIS,1,[Define this if you have libvorbis installed])
                      ac_have_vorbis="yes"],
	     AC_MSG_ERROR([*** libvorbis appears to be missing ***]))
#AC_CHECK_LIB(ogg, ogg_sync_buffer,,
#	     AC_MSG_ERROR([*** libogg appears to be missing ***]))
AC_CHECK_LIB(ogg, ogg_sync_buffer,
                     [LIBS="$LIBS -logg"
                      AC_DEFINE(HAVE_OGG,1,[Define this if you have libogg installed])
                      ac_have_ogg="yes"],
	     AC_MSG_ERROR([*** libogg appears to be missing ***]))

dnl Check for header files.
AC_HEADER_STDC
AC_CHECK_HEADERS(unistd.h)
#AC_CHECK_HEADER(pthread.h,,
#		AC_MSG_ERROR([*** POSIX thread support not installed ***]))

dnl Checks for typedefs, structures, and compiler characteristics.

dnl Checks for library functions.
AC_FUNC_VPRINTF

# nicked from the irmix project...
##AC_ARG_ENABLE([xinerama],
##              AC_HELP_STRING([--disable-xinerama],
##			     [disable use of Xinerama extension]),
##              [disable_xinerama="yes"],
##	      [disable_xinerama="no"])

#if test x$disable_xinerama = "xno"
#then
#        AC_CHECK_LIB(Xinerama_pic,
#                     XineramaQueryExtension,
#                     [X_LIBS="$X_LIBS -lXinerama_pic"
#                      AC_DEFINE(HAVE_XINERAMA,1,[Define this if you have libXinerama installed])
#                      ac_have_xinerama="yes"],
#                      AC_CHECK_LIB(Xinerama,
#                                   XineramaQueryExtension,
#                                   [X_LIBS="$X_LIBS -lXinerama"
#                                    AC_DEFINE(HAVE_XINERAMA,1,[Define this if you have libXinerama installed])
#                                    ac_have_xinerama="yes"],,
#                                    [$X_LIBS $X_PRE_LIBS -lXext $X_EXTRA_LIBS]),
#                     [$X_LIBS $X_PRE_LIBS -lXext $X_EXTRA_LIBS])
#fi




dnl Define VORBISSIMPLE_VERSION
AC_DEFINE_UNQUOTED(VORBISSIMPLE_VERSION, "${VERSION}")

EXTRA_DIST=

dnl Produce Output files
AC_CONFIG_FILES([
Makefile
src/Makefile
src/libvorbissimple/Makefile
macros/Makefile
script/Makefile
script/vorbissimple-config
])
AC_CONFIG_COMMANDS([default],[[chmod +x script/vorbissimple-config]],[[]])
AC_OUTPUT
