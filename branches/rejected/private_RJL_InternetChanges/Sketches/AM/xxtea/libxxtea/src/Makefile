OBJS=xxtea.o keygen.o
CC = gcc
INC_PATH = ../include
LIB_PATH = ../lib
CFLAGS = -fPIC
INSTALL_PATH = /usr/lib
xxt:$(OBJS)
	$(CC) -shared xxtea.o keygen.o -o $(LIB_PATH)/libxxtea.so
xxtea.o:xxtea.c
	$(CC) $(CFLAGS) -I $(INC_PATH) -c xxtea.c
keygen.o:keygen.c
	$(CC) $(CFLAGS) -I $(INC_PATH) -c keygen.c
clean:
	rm *.o
	rm ../lib/libxxtea.so
install:xxt
	cp $(LIB_PATH)/libxxtea.so $(INSTALL_PATH)

