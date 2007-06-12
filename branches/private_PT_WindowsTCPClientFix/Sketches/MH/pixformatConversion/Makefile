all: pixConvert.o
	gcc -pthread -shared pixConvert.o -o pixConvert.so
	
pixConvert.o: pixConvert.c convert.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -O2 -fmessage-length=0 -Wall -D_FORTIFY_SOURCE=2 -g -fPIC -I/usr/include/python2.4 -c pixConvert.c -o pixConvert.o

pixConvert.c: pixConvert.pyx convert.c
	pyrexc pixConvert.pyx

clean:
	rm pixConvert.o pixConvert.so pixConvert.c
