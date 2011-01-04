#! /usr/bin/python

import MySQLdb
import cjson
import os
import sys

channels = {"bbcone" : ["bbc one", "/bbcone/programmes/schedules/north_west/today"],
                "bbctwo" : ["bbc two", "/bbctwo/programmes/schedules/england"],
                "bbcthree" : ["bbc three", "/bbcthree/programmes/schedules"],
                "bbcfour" : ["bbc four", "/bbcfour/programmes/schedules"],
                "cbbc" : ["cbbc channel", "/cbbc/programmes/schedules"],
                "cbeebies" : ["cbeebies", "/cbeebies/programmes/schedules"],
                "bbcnews" : ["bbc news", "/bbcnews/programmes/schedules"],
                "radio1" : ["bbc radio 1", "/radio1/programmes/schedules/england"],
                "radio2" : ["bbc radio 2", "/radio2/programmes/schedules"],
                "radio3" : ["bbc radio 3", "/radio3/programmes/schedules"],
                "radio4" : ["bbc radio 4", "/radio4/programmes/schedules/fm"],
                "5live" : ["bbc r5l", "/5live/programmes/schedules"],
                "worldservice" : ["bbc world sv.", "/worldservice/programmes/schedules"],
                "6music" : ["bbc 6 music", "/6music/programmes/schedules"],
                "radio7" : ["bbc radio 7", "/radio7/programmes/schedules"],
                "1xtra" : ["bbc r1x", "/1xtra/programmes/schedules"],
                "bbcparliament" : ["bbc parliament", "/parliament/programmes/schedules"],
                "asiannetwork" : ["bbc asian net.", "/asiannetwork/programmes/schedules"],
                "sportsextra" : ["bbc r5sx", "/5livesportsextra/programmes/schedules"]}

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


    for channel in channels:
        print "Now fixing durations for", channel

        cursor.execute("""SELECT pid,timestamp,duration FROM programmes WHERE channel = %s ORDER BY timestamp""",(channel))
        data = cursor.fetchall()

        lastpid = None

        for result in data:
            currentpid = result[0]
            currenttimestamp = result[1]
            currentduration = result[2]

            if lastpid != None:
                lastduration = currenttimestamp - lasttimestamp
                # Update stuff here
                cursor.execute("""UPDATE programmes SET duration = %s WHERE pid = %s AND timestamp = %s""",(lastduration,lastpid,lasttimestamp))

            lastpid = result[0]
            lasttimestamp = result[1]
            lastduration = result[2]
                