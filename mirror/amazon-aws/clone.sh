#!/bin/bash

rm -rf original
hg clone http://freehg.org/u/ben/kamaelia-aws/
mv kamaelia-aws original

(
   cd original
   echo "grabbing"
   pwd
   tar zcvf ../current.tar.gz . --exclude=.hg --exclude .hgignore
)
( 
   cd trunk
   echo "ungrabbing"
   pwd
   tar zxvf ../current.tar.gz
   svn status 2>&1 |egrep -v my_checkout_status_file| tee my_checkout_status_file
   grep "^?" my_checkout_status_file|grep -v my_checkout_status_file |while read q filename; do svn add $filename; done
   svn ci -m "Mirroring Changes to Kamaelia-AWS"
   rm -rf my_checkout_status_file
)

rm -rf current.tar.gz
rm -rf tmp
rm -rf original
