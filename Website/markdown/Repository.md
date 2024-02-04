---
pagename: Repository
last-modified-date: 2008-10-06
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
# Kamaelia Git Repository

All our code is developed and held in a git repository, hosted on
github. Since Kamaelia is in a maintenance mode at present, ongoing
fixes and development is via the <https://github.com/sparkslabs/kamaelia>
repo for now.

To contribute back changes, please fork the project there and checkout a
local copy, make your changes and open a [Pull Request](https://github.com/sparkslabs/kamaelia/pulls) using the usual
github processes.

You can also open [issues](https://github.com/sparkslabs/kamaelia/issues)
there to discuss the codebase and improvements.

Please note: This site is currently (January 2024) very out of
date and suffering bitrot. Fixes for this are in progress and 
[currently tracked via an issue to cover this specifically.](https://github.com/sparkslabs/kamaelia/issues/7)

**Checking out a working copy**

Either:

-   ` git clone https://github.com/sparkslabs/kamaelia.git `
-   ` git clone git@github.com:sparkslabs/kamaelia.git `

**Installing Axon**

    cd Code/Python/Axon
    python setup.py build
    sudo python setup.py install

**Installing Kamaelia**

    cd Code/Python/Kamaelia
    python setup.py build
    sudo python setup.py install
