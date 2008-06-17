AM_CFLAGS = -I$(top_srcdir)/src
# Library
lib_LTLIBRARIES 	= libvorbissimple.la
libvorbissimple_la_SOURCES 	= vorbissimple.c
libvorbissimple_la_LIBADD 	= $(X_LIBS)
libvorbissimple_la_LDFLAGS = -version-info $(LT_CURRENT):$(LT_REVISION):$(LT_AGE) -pthread
