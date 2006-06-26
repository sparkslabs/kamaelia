OBJS = xxtea_test.o 
CC = gcc
INC_PATH = ../include
LIB_PATH = ../lib/
xxt_test:$(OBJS)
	$(CC) -o xxtea_test xxtea_test.o $(LIB_PATH)libxxtea.so
xxtea_test.o:xxtea_test.c
	$(CC)  -c -I $(INC_PATH) xxtea_test.c
clean:
	rm *.o
	rm xxtea_test
	rm xxtea_test.enc xxtea_test.dec

