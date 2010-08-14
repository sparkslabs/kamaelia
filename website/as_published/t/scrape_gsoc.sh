#!/bin/bash

lynx -dump http://code.google.com/soc/2007/ | \
grep about.html$ | \
awk '{print $2}' | \
while read url; do 
    HOST=`echo "$url" | cut -d/ -f 6;`
    echo $HOST
    curl -o $HOST.html $url
done

mkdir apps
grep link.*appinfo *|\
while read link; do
      HOST=`echo $link |cut -d. -f1`
      APPID=`echo $link |cut -d= -f2 |sed -e 's/"//g'`
      echo $HOST $APPID
      curl -o apps/$APPID.html http://code.google.com/soc/2007/$HOST/appinfo.html?csaid=$APPID
done

mkdir frags
for i in `ls *html`; do egrep -A1000 'class=applist' $i|egrep -v 'class=applist'|egrep -B1000 "<table>"|egrep -v "(<table>|<tr> <td colspan=2>&nbsp;</td> </tr>)">frags/$i; done

cd ..
LHOST = ""

echo > toc.txt; echo "<ul>" >> toc.txt; LHOST=""; grep link.*appinfo *.html|while read link; do HOST=`echo $link |cut -d. -f1`; if [ "$LHOST" != "$HOST" ] ; then if [ "$LHOST" != "" ] ; then echo "</table>"; fi; echo "<li><a href="#$HOST"> $HOST </a>" >> toc.txt; echo "<a name='$HOST' />"; echo "<h2> $HOST </h2>"; echo "<table>"; LHOST=$HOST; fi;APPID=`echo $link |cut -d= -f2 |sed -e 's/"//g'`; cat apps/frags/$APPID.html; done|cat - > pre.txt; echo "</ul>" >> toc.txt; echo "<html><body>" > all.html; cat toc.txt pre.txt >> all.html; echo "</body></table>" >> all.html








