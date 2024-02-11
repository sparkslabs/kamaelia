
NONGENERABLE=non-generable

all:
	@echo "clean - remove build directories"
	@echo "build - build the new site based markdown, and non-generable content"
	@echo "serve - serve the build directory locally"
	@echo "publish - show diffs against stage"

clean:
	rm -rf build
	rm -rf auto-site
	rm -rf to-deploy

build:
	./mkAutoSite.py
	mkdir to-deploy
	rsync -avz $(NONGENERABLE)/ to-deploy/
	rsync -avz auto-site/ to-deploy/

serve:
	cd to-deploy ; python3 -m http.server

publish:
	rsync -avz --delete-during to-deploy/ kamaelia.org:website/
