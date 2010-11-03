# Programs.  Don't install testprog.
bin_PROGRAMS 	= simple_decoder
# noinst_PROGRAMS = testprog

simple_decoder_SOURCES  = simple_decoder.c
# testprog_SOURCES = testprog.c

simple_decoder_LDADD 	= libvorbissimple/libvorbissimple.la
# testprog_LDADD 	= libvorbissimple/libvorbissimple.la

include_HEADERS = vorbissimple.h

AM_CFLAGS = ${GTK_CFLAGS}

SUBDIRS=libvorbissimple
