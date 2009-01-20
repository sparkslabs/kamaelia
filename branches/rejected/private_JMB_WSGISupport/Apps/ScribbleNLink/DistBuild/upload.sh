#!/bin/sh



version=`grep version setup.py.src|sed -e 's/^.*= "//; s/",.*//'`
echo "Uploading $version"

scp ../dist/* michaels@132.185.142.2:/srv/www/sites/edit.kamaelia.org/docs/release/
