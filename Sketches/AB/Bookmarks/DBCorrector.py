#! /usr/bin/python

import MySQLdb
import cjson
import os
import time
from dateutil.parser import parse
import sys


def dbConnect(dbuser,dbpass):
    db = MySQLdb.connect(user=dbuser,passwd=dbpass,db="twitter_bookmarks",use_unicode=True,charset="utf8")
    cursor = db.cursor()
    return cursor

if __name__ == "__main__":
    # Calculate running total and mean etc

    # Load Config
    try:
        homedir = os.path.expanduser("~")
        file = open(homedir + "/twitter-login.conf")
    except IOError, e:
        print ("Failed to load login data - exiting")
        sys.exit(0)

    raw_config = file.read()
    file.close()

    # Read Config
    config = cjson.decode(raw_config)
    dbuser = config['dbuser']
    dbpass = config['dbpass']

    cursor = dbConnect(dbuser,dbpass)

    while 1:
        
        print "Checking for new raw data..."

        cursor.execute("""SELECT tid,datetime,timestamp FROM rawdata WHERE timestamp = 0 ORDER BY tid LIMIT 5000""")
        data = cursor.fetchall()

        for result in data:
            tid = result[0]
            tweettime = result[1]
            tweetstamp = result[2]
            tweetstamp = time.mktime(parse(tweettime).timetuple())
            
            print tweettime
            print tweetstamp
            
            cursor.execute("""UPDATE rawdata SET timestamp = %s WHERE tid = %s""",(tweetstamp,tid))

        print "Checking for new analysed data..."

        cursor.execute("""SELECT did,datetime,timestamp FROM analyseddata WHERE timestamp = 0 ORDER BY did LIMIT 5000""")
        data = cursor.fetchall()

        for result in data:
            did = result[0]
            tweettime = result[1]
            tweetstamp = result[2]
            tweetstamp = time.mktime(parse(tweettime).timetuple())

            print tweettime
            print tweetstamp

            cursor.execute("""UPDATE analyseddata SET timestamp = %s WHERE did = %s""",(tweetstamp,did))

        print "Checking for new programme data..."

        cursor.execute("""SELECT pid,expectedstart,timestamp FROM programmes WHERE timestamp = 0 ORDER BY pid LIMIT 5000""")
        data = cursor.fetchall()

        for result in data:
            pid = result[0]
            expectedstart = result[1]
            timestamp = result[2]
            timestamp = parse(expectedstart)
            tz = timestamp.tzinfo
            utcoffset = datetime.strptime(str(tz.utcoffset(timestamp)),"%H:%M:%S")
            utcoffset = utcoffset.hour * 60 * 60
            timestamp = time.mktime(timestamp.replace(tzinfo=None).timetuple())

            print expectedstart
            print timestamp
            print utcoffset

            cursor.execute("""UPDATE programmes SET timestamp = %s, utcoffset = %s WHERE pid = %s""",(timestamp,utcoffset,pid))
            
        print "Sleeping for 10 seconds..."
        time.sleep(10)