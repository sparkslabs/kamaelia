#!/bin/bash
# 
# Script to run the Bookmarks.py code in a loop, restarting when it dies. 
# 
# It checks to see if ~/stop_bookmarks exists. If it does it sleeps 10 seconds 
# before checking again. This allows the system to be halted for database
# rolling purposes.
# 

while true; do
    if [ ! -e ~/stop_bookmarks ]; then
        LOGFILE=mainlog-`date +%s`.log
        DEBUGFILE=debug-`date +%s`.log
        echo "=================================================================="
        echo "`date` - Restarting Bookmarks"
        ./Bookmarks.py 2>$DEBUGFILE >$LOGFILE
        sleep 10
    else
        echo "`date` - Not Restarting, because ~/stop_bookmarks exists"
        sleep 10
    fi
done

