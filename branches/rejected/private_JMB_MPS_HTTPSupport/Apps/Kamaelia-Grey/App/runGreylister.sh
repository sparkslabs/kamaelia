#!/bin/sh

( ( 
while true; do 
   # echo "--- STARTING SERVER ---"|tee -a greylist.log
   # date | tee -a greylist.log
   /usr/local/bin/greylisting.py 2>&1 >/dev/null
   sleep 5
done 
) & ) &