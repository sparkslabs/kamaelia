#!/usr/bin/python

import os
import sys
import time
import cjson

import MySQLdb
from Kamaelia.Apps.SocialBookmarks.Print import Print

def MySQL_Running():
    processline = os.popen('ps 2>/dev/null -aux|grep mysqld|grep -v grep').read()
    if processline:
        return True
    else:
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

os.system("touch "+ homedir +"/stop_bookmarks")

time.sleep(1)

processline = os.popen('ps 2>/dev/null -aux|grep Bookmarks.py|grep -v grep').read()

if processline:
    print "Still running, trying again - from outside"
    tokens = processline.split()
    user, pid, pcpu, pmem, vsz, rss, tty, stat, start, time, command = tokens[:11]
    args = tokens[11:]
    os.system("kill -9 %s" % pid)

processline = os.popen('ps 2>/dev/null -aux|grep Bookmarks.py|grep -v grep').read()
if processline:
    raise Exception("Was unable to kill Bookmarks.py for rolling from inside or outside")
    
killTries = 0

while MySQL_Running():
    killTries += 1
    if killTries > 60:
        raise Exception("Was unable to kill mysql within 60 seconds of trying...")
    os.system("stop mysql")
    time.sleep(1)

#
# MySQL is now stopped, we can now mess with the database with impugnity
#

now = time.gmtime()
year = now.tm_year;
month = now.tm_mon;
day = now.tm_mday;
today = "%04d%02d%02d" % (year, month, day)

# Assumes mysql is in this location.
# This actually depends on local installation, but is true for *THIS* system

os.rename("/var/lib/mysql/twitter_bookmarks" , "/var/lib/mysql/twitter_bookmarks_" +today)
os.rename("/var/lib/mysql/twitter_bookmarks_next", "/var/lib/mysql/twitter_bookmarks")
os.system("rsync -avz  /var/lib/mysql/twitter_bookmarks_empty/ /var/lib/mysql/twitter_bookmarks_next/")

# CHECK THAT MYSQL HAS ACTUALLY STARTED THIS WILL FAIL HARD OTHERWISE.

startTries = 0

while not MySQL_Running():
    startTries += 1
    if startTries > 60:
        raise Exception("Was unable to RESTART mysql within 60 seconds of trying...")
    os.system("start mysql")
    time.sleep(1)

#
# Grab all the auto_increment values from the current mirror
#
db = MySQLdb.connect(user=username,passwd=password,db="information_schema",use_unicode=True,charset="utf8")
cursor = db.cursor()
rowcount = cursor.execute('select TABLE_NAME,AUTO_INCREMENT from tables where table_schema="twitter_bookmarks" and AUTO_INCREMENT >0;')
if rowcount == 0:
    raise Exception("Failed to grab auto increment information from the old schema for updating new schema")

tuples= cursor.fetchall()

#
# ... and update the new to match...
#
db2 = MySQLdb.connect(user=username,passwd=password,db="twitter_bookmarks_next",use_unicode=True,charset="utf8")
cursor = db2.cursor()
for tablename, max in tuples:
    print tablename,max
    cursor.execute("ALTER TABLE %s AUTO_INCREMENT = %d;" % (tablename,max))

time.sleep(1)

os.system("rm "+ homedir + "/stop_bookmarks")



