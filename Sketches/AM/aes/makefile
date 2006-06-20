objs = aescrypt.o aeskey.o aestab.o aesxam.o aesint.o keygen.c
CC = gcc
aes:$(objs)
	$(CC) -c -fPIC aescrypt.c aeskey.c aestab.c aesxam.c aesint.c keygen.c
	$(CC) -shared aescrypt.o aeskey.o aestab.o aesxam.o aesint.o keygen.o -o aes.so
	rm -f *.o
