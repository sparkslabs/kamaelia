PYTHON=`which python`
DESTDIR=/
PROJECT=kamaelia
VERSION=1.14.32
all:
	@echo "make source - Create source package"
	@echo "make install - Install on local system (only during development)"
	@echo "make deb - Generate a deb package - for local testing"
	@echo "make ppa - Generate a source deb and upload to ppa"
	@echo "make pypi - Make package for pypi and upload"
	@echo "make use	- Use the deb package - for local testing"
	@echo "make purge - remove deb packaeg"
	@echo "make devloop - purge, distclean, deb, use"	
	@echo "make clean - Get rid of scratch and byte files"
	@echo "make distclean - get rid of dist files too"
	@echo "make test - Run any unit tests"

source:
	cp ../../../COPYING .
	cp ../../../AUTHORS .
	$(PYTHON) setup.py sdist $(COMPILE)

install:
	$(PYTHON) setup.py install --root $(DESTDIR) $(COMPILE)

deb:
	cp ../../../COPYING .
	cp ../../../AUTHORS .
	python setup.py sdist
	cd dist && py2dsc $(PROJECT)-* && cd deb_dist/$(PROJECT)-$(VERSION) && debuild -uc -us

ppadeb:
	cp ../../../COPYING .
	cp ../../../AUTHORS .
	python setup.py sdist
	cd dist && py2dsc $(PROJECT)-* && cd deb_dist/$(PROJECT)-$(VERSION) && debuild -S && cd .. && dput ppa:sparkslabs/packages $(PROJECT)_*_source.changes

use:
	sudo dpkg -i dist/deb_dist/python3-$(PROJECT)*deb

purge:
	sudo apt-get purge python3-$(PROJECT)

clean:
	rm -f COPYING
	rm -f AUTHORS
	$(PYTHON) setup.py clean
	rm -rf build/ MANIFEST  
	find . -name '*.pyc' -delete

pypi:
	$(PYTHON) setup.py sdist
	twine upload dist/*

distclean:
	$(PYTHON) setup.py clean
	rm -rf dist
	rm -rf build/ MANIFEST
	find . -name '*.pyc' -delete

devloop: purge distclean deb use
	echo

test:
	behave	
