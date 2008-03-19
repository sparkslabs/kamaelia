#!/bin/sh

( ( 
while true; do 
   /usr/local/bin/kamaelia_logger.py 2>&1 >/dev/null
   sleep 5
done 
) & ) &