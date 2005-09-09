
all: dirac_parser.so

dirac_parser.so: dirac_parser.o
	gcc -shared dirac_parser.o -ldirac_decoder -o dirac_parser.so
	
dirac_parser.o: dirac_parser.c
	gcc -c -fPIC -I/usr/include/python -I/usr/local/include -I/usr/local/include/dirac dirac_parser.c
	
dirac_parser.c: dirac_parser.pyx
	python /usr/bin/pyrexc dirac_parser.pyx


clean:
	rm dirac_parser.so dirac_parser.o dirac_parser.c
