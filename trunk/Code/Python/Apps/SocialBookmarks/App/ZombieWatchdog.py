#!/usr/bin/python
"""
Zombie monitor - looks to see if the system is "working", but not actually accepting data from various sources, processing etc. 
Kills/restarts the bookmarks code if it's dead.


"""
import os
import sys
import time
import cjson

import MySQLdb
from Kamaelia.Apps.SocialBookmarks.Print import Print

def killBookmarksProcess():
    processline = os.popen('ps 2>/dev/null -aux|grep Bookmarks.py|grep -v grep').read()
    if processline:
        tokens = processline.split()
        user, pid, pcpu, pmem, vsz, rss, tty, stat, start, time, command = tokens[:11]
        args = tokens[11:]
        os.system("kill -9 %s" % pid)
    else:
        Print("Bookmarks.py is not running. This means the shell process wrapping it isn't starting it, or is dead. This program cannot fix that problem.")

def get_database_state():

    db2 = MySQLdb.connect(user=username,passwd=password,db="information_schema",use_unicode=True,charset="utf8")
    cursor = db2.cursor()

    rowcount = cursor.execute('select TABLE_SCHEMA,TABLE_NAME,AUTO_INCREMENT from tables where (TABLE_SCHEMA = "twitter_bookmarks") and AUTO_INCREMENT > 1;')
    if rowcount == 0:
        raise Exception("Database looks broken, leaving alone")

    tuples= cursor.fetchall()

    state = {}

    for table_schema,table,auto_increment in tuples:
        if table in ("analyseddata", "keywords", "rawdata", "wordanalysis"):
            state[table] = auto_increment

    if len(state.keys()) != 4:
        raise Exception("Database looks broken, leaving alone")

    now = time.time()

    state["timestamp"] = time.time()
    return state

def get_historical_status():

    try:
        f = open("historical_status.json")
        raw_data = f.read()
        f.close()
        historical_status = cjson.decode(raw_data)
    except Exception, e:
        # Doesn't really matter what the problem is. It failed, warn, and use a default.
        Print("Failed to read historical_status.json, creating a new one")
        Print("Exception was: ", e)
        historical_status = []

    return historical_status 

def add_current_state(historical_status, state, max_history_len=10):
    historical_status.append(state)
    while len(historical_status) > max_history_len:
        _ = historical_status.pop(0)

def store_historical_status(historical_status):
    serialised_data = cjson.encode(historical_status)
    try:
        f = open("historical_status.json","wb")
        f.write(serialised_data)
        f.close()
    except Exception, e:
        # Doesn't really matter what the problem is. It failed, and there's nothing this code can do about it.
        Print("Failed to WRITE historical_status.json, something is badly broken")
        Print("Exception was: ", e)

def ShouldWeRestartBookmarks(historical_status):
    deltas = {"keywords":[], "wordanalysis":[], "rawdata":[], "analyseddata":[],"timestamp":[]}
    k = 1
    
    if len(historical_status) <2:
        # Not enough information
        return False
    
    while k < len(historical_status):
        deltas["keywords"].append( historical_status[k]["keywords"] - historical_status[k-1]["keywords"] )
        deltas["wordanalysis"].append( historical_status[k]["wordanalysis"] - historical_status[k-1]["wordanalysis"] )
        deltas["rawdata"].append( historical_status[k]["rawdata"] - historical_status[k-1]["rawdata"] )
        deltas["analyseddata"].append( historical_status[k]["analyseddata"] - historical_status[k-1]["analyseddata"] )
        deltas["timestamp"].append( int(historical_status[k]["timestamp"] - historical_status[k-1]["timestamp"] ) )
        k += 1

    import pprint
    pprint.pprint(deltas)

    last_hour_schedule_activity = sum(deltas["keywords"][-6:])
    last_2periods_tweet_collation_activity = sum(deltas["rawdata"][-2:])
    last_2periods_wordanalysis_activity = sum(deltas["wordanalysis"][-2:])
    last_2periods_analyseddata_activity = sum(deltas["analyseddata"][-2:])
    
    all_current_activity = deltas["keywords"][-1],deltas["rawdata"][-1],deltas["wordanalysis"][-1],deltas["analyseddata"][-1]
    if all_current_activity == 0:
        Print("Bookmarks.py is showing no activity at all, of any kind, very likey dead")
        return True
    
    if last_hour_schedule_activity == 0:
        if len(deltas["keywords"])>5:
            Print("Looks like schedule collation in Bookmarks.py has died, needs restart")
            return True

    if last_2periods_tweet_collation_activity == 0:
        if len(deltas["rawdata"])>1:
            Print("Looks like tweet collection activity in Bookmarks.py has died, needs restart")
            return True

    if last_2periods_wordanalysis_activity == 0:
        if len(deltas["wordanalysis"])>1:
            Print("Looks like word analysis of tweets - activity - in Bookmarks.py has died, needs restart")
            return True

    if last_2periods_analyseddata_activity == 0:
        if len(deltas["analyseddata"])>1:
            Print("No tweets analysed in 2 periods. In all likelihood analysis subsystem in Bookmarks.py has died, needs restart")
            return True

    # Warnings
    if deltas["rawdata"][-1] == 0:
        Print("WARNING - no tweets collected in 1 period, might be dead. Waiting 1 period")
    if deltas["wordanalysis"][-1] == 0:
        Print("WARNING - no tweet words analysed in 1 period, might be dead. Waiting 1 period")
    if deltas["analyseddata"][-1] == 0:
        Print("WARNING - no tweets analysed in 1 period, might be dead. Waiting 1 period")

    return False

try:
    homedir = os.path.expanduser("~") # Bootstrap from /root/, but use this to find the rest
    config_file = open(homedir + "/twitter-login.conf")
except IOError, e:
    Print("Failed to load login data - exiting")
    sys.exit(0)

raw_config = config_file.read()
config_file.close()
config = cjson.decode(raw_config)

username = config['dbuser']
password = config['dbpass']
unixuser = config['unixuser']
homedir = os.path.expanduser("~"+unixuser)

state = get_database_state()
historical_status = get_historical_status()
add_current_state(historical_status, state)
store_historical_status(historical_status)

if ShouldWeRestartBookmarks(historical_status):
    Print("OK, We would now restart")
    killBookmarksProcess()
else:
    Print("Yay, the system is working fine")
