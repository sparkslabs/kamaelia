all: ComputeMeanAbsDiff.o
	gcc -pthread -shared ComputeMeanAbsDiff.o -o ComputeMeanAbsDiff.so
	
ComputeMeanAbsDiff.o: ComputeMeanAbsDiff.c
	gcc -pthread -fno-strict-aliasing -DNDEBUG -O2 -fmessage-length=0 -Wall -D_FORTIFY_SOURCE=2 -g -fPIC -I/usr/include/python2.4 -c ComputeMeanAbsDiff.c -o ComputeMeanAbsDiff.o

ComputeMeanAbsDiff.c: ComputeMeanAbsDiff.pyx
	pyrexc ComputeMeanAbsDiff.pyx

clean:
	rm ComputeMeanAbsDiff.o ComputeMeanAbsDiff.so ComputeMeanAbsDiff.c
