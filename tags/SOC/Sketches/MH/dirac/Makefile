
all: dirac_parser.so dirac_encoder.so

dirac_parser.so: dirac_parser.o
	gcc -shared dirac_parser.o -ldirac_decoder -o dirac_parser.so
	
dirac_parser.o: dirac_parser.c
	gcc -c -fPIC -I/usr/include/python -I/usr/local/include -I/usr/local/include/dirac dirac_parser.c
	
dirac_parser.c: dirac_parser.pyx
	python /usr/bin/pyrexc dirac_parser.pyx



dirac_encoder.so: dirac_encoder.o
	gcc -shared dirac_encoder.o -ldirac_encoder -o dirac_encoder.so

dirac_encoder.o: dirac_encoder.c
	gcc -c -fPIC -I/usr/include/python -I/usr/local/include -I/usr/local/include/dirac dirac_encoder.c

dirac_encoder.c: dirac_encoder.pyx
	python /usr/bin/pyrexc dirac_encoder.pyx



clean:
	rm dirac_parser.so dirac_parser.o dirac_parser.c
	rm dirac_encoder.c
