
all: clean install

build vorbissimple.c:
	python setup.py build

install: vorbissimple.c
	sudo python setup.py install
	sudo ldconfig

working:
	rm -f foo.raw; ./simple_decoder.py 2>foo.raw ; aplay -f cd foo.raw

broken:
	cp simple_decoder.py another_simple_decoder.py
	./another_simple_decoder.py 2>foo2.raw ; aplay -f cd foo2.raw

clean:
	sudo rm -rf build
	sudo rm -rf dist Vorbissimple.egg-info cython_debug
	# sudo rm -rf /usr/local/lib/python3.12/dist-packages/Vorbissimple-0.0.0-py3.12-linux-x86_64.egg/
	rm -f vorbissimple.c
	rm -f *~
	rm -f foo.*
	rm -f foo2.*
