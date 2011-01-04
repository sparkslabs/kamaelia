#! /usr/bin/python

import MySQLdb
import cjson
import os
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

    records = 5000

    while records > 0:
        cursor.execute("""SELECT tid,pid,timestamp FROM rawdata WHERE programme_position = 0 ORDER BY timestamp LIMIT 5000""")
        data = cursor.fetchall()
        records = len(data)
        print "Found", str(records), "records"

        for result in data:
            tid = result[0]
            pid = result[1]
            timestamp = result[2]

            cursor.execute("""SELECT timestamp,timediff FROM programmes WHERE pid = %s""",(pid))
            data2 = cursor.fetchone()

            progtimestamp = data2[0]
            progtimediff = data2[1]

            progposition = timestamp - progtimestamp + progtimediff

            cursor.execute("""UPDATE rawdata SET programme_position = %s WHERE tid = %s""",(progposition,tid))
