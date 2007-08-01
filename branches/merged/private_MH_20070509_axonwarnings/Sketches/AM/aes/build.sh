pyrexc aesmod.pyx
gcc -c -fPIC -I /usr/include/python2.4/ aesmod.c
gcc -shared aesmod.o -o aesmod.so ./aes.so 
