#!/bin/bash

rm -rf tmp
hg clone http://freehg.org/u/ben/kamaelia-aws/
mv kamaelia-aws tmp

(
   cd original
   tar zcvf ../current.tar.gz . --exclude=.hg --exclude .hgignore
)
( 
   cd trunk
   tar zxvf ../current.tar.gz
   svn status 2>&1 |tee status
   grep "^?" status|while read q filename; do svn add $filename; done
   svn ci -m "Mirroring Changes to Kamaelia-AWS"
)
rm current.tar.gz
rm -rf tmp