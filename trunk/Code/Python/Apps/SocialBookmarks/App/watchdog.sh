#!/bin/bash
# 
# Watchman script to run the Zombie Watchdog repeatedly. 
# 
# This should ideally also have hooks in it to detect if *this* script is
# running, so that this script can be re-run from cron.
# 

while true; do
    clear
    date
    echo; ./ZombieWatchdog.py
    echo
    sleep 600
    echo
done

