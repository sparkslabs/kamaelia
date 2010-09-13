#! /usr/bin/python

# Analyses saved data in DB to give something more useful. Saves to output DB ready for display in web interface
# Need word freq analysis, tweet rate analysis etc
# Any looking at natural language engines / subtitles should be done here or in components following this
# This component probably needs the original keywords etc too TODO as it needs to separate both programmes and channels
# When analysing, look for mentions of just first names used with #programme etc, as people are unlikely to describe presenters etc with full names (could actually modify the original search to do this) TODO
# Watch out for repeated tweets - could be user or Twitter error
# Need to ensure one rogue user can't cause a trend - things must be mentioned by several

from datetime import datetime
from datetime import timedelta
import os
import string

import cjson
from dateutil.parser import parse
import matplotlib.pyplot as plt

exclusions = ["a","able","about","across","after","all","almost","also","am",\
                "among","an","and","any","are","as","at","be","because","been","but",\
                "by","can","cannot","could","dear","did","do","does","either","else",\
                "ever","every","for","from","get","got","had","has","have","he","her",\
                "hers","him","his","how","however","i","if","in","into","is","it",\
                "its","just","least","let","like","likely","may","me","might","most",\
                "must","my","neither","no","nor","not","of","off","often","on","only",\
                "or","other","our","own","rather","said","say","says","she","should",\
                "since","so","some","than","that","the","their","them","then","there",\
                "these","they","this","tis","to","too","twas","us","wants","was","we",\
                "were","what","when","where","which","while","who","whom","why","will",\
                "with","would","yet","you","your"]

if __name__ == "__main__":

    # Details below SHOULD be sourced from earlier components really
    pid = "b00tr1df" # Dragons' Den
    timediffmins = -3 # Broadcast of prog started 3 mins late compared to NTP
    timediffsecs = 0
    #keywords = ['bbcone', '#EastEnders', 'Bryan Kirkwood', 'Simon Ashdown', 'Lee Salisbury', 'Richard Monroe bbcone', 'Richard Monroe EastEnders', 'Andrew Hall', 'Dot Branning bbcone', 'Dot Branning EastEnders', 'June Brown', 'Sam Mitchell bbcone', 'Sam Mitchell EastEnders', 'Danniella Westbrook', 'Tamwar Masood bbcone', 'Tamwar Masood EastEnders', 'Himesh Patel', 'Jay Brown bbcone', 'Jay Brown EastEnders', 'Jamie Borthwick', 'Mo Harris bbcone', 'Mo Harris EastEnders', 'Laila Morse', 'Morgan Jackson-King bbcone', 'Morgan Jackson-King EastEnders', 'Devon Higgs', 'Billy Mitchell bbcone', 'Billy Mitchell EastEnders', 'Perry Fenwick', 'Peggy Mitchell bbcone', 'Peggy Mitchell EastEnders', 'Barbara Windsor', 'Masood Ahmed bbcone', 'Masood Ahmed EastEnders', 'Nitin Ganatra', 'Celebrant bbcone', 'Celebrant EastEnders', 'Debbie Norman', 'Tiffany Butcher bbcone', 'Tiffany Butcher EastEnders', 'Maisie Smith', 'Zainab Masood bbcone', 'Zainab Masood EastEnders', 'Nina Wadia', 'Shirley Carter bbcone', 'Shirley Carter EastEnders', 'Linda Henry', 'Whitney Dean bbcone', 'Whitney Dean EastEnders', 'Shona McGarty', 'Ryan Malloy bbcone', 'Ryan Malloy EastEnders', 'Neil McDermott', 'Liam Butcher bbcone', 'Liam Butcher EastEnders', 'James Forde', 'Darren Miller bbcone', 'Darren Miller EastEnders', 'Charlie G Hawkins', 'Jodie Gold bbcone', 'Jodie Gold EastEnders', 'Kylie Babbington', 'Pat Evans bbcone', 'Pat Evans EastEnders', 'Pam St Clement', 'Charlie Slater bbcone', 'Charlie Slater EastEnders', 'Derek Martin', 'Roxy Mitchell bbcone', 'Roxy Mitchell EastEnders', 'Rita Simons', 'Syed Masood bbcone', 'Syed Masood EastEnders', 'Marc Elliott', 'Phil Mitchell bbcone', 'Phil Mitchell EastEnders', 'Steve McFadden', 'Ricky Butcher bbcone', 'Ricky Butcher EastEnders', 'Sid Owen', 'Bianca Butcher bbcone', 'Bianca Butcher EastEnders', 'Patsy Palmer', 'Janine Malloy bbcone', 'Janine Malloy EastEnders', 'Charlie Brooks', 'Vanessa Gold bbcone', 'Vanessa Gold EastEnders', 'Zoe Lucker', 'Jean Slater bbcone', 'Jean Slater EastEnders', 'Gillian Wright', 'Stacey Branning bbcone', 'Stacey Branning EastEnders', 'LaceyATurner', 'Lacey Turner', 'Max Branning bbcone', 'Max Branning EastEnders', 'Jake Wood']
    #keywords = ['bbcone', '#TheOneShow', 'Jason_Manford', 'Jason Manford', 'QuincyDJones', 'Quincy Jones', 'John Sargeant', 'Lucy Siegle', 'RealAlexJones', 'Alex Jones', 'Joe Crowley']
    #keywords = ['bbcone', '#theoneshow', '#theoneshow', 'RealAlexJones', 'Alex Jones', 'Xanneroo', 'Alexander Armstrong', 'realrossnoble', 'Ross Noble']
    #keywords = ['bbctwo', '#DragonsDen', 'Putul Verma', 'Evan Davis', 'EvanHD', 'Duncan Bannatyne', 'DuncanBannatyne', 'James Caan', 'Peter Jones', 'dragonjones', 'Deborah Meaden', 'Theo Paphitis', 'Sam Lewens']
    #keywords = ['bbcone', '#banggoesthetheory', 'Dallas Campbell', 'Yan Wong', 'Jem Stansfield', 'Dermot Caulfield', 'Liz Bonnin', 'Ed Booth']
    #keywords = ['bbcone', '#waterlooroad', 'Liz Lake', 'Roger Goldby', 'Jane Hudson', 'Francesca Montoya bbcone', 'Francesca Montoya Waterloo Road', 'Francesca bbcone', 'Francesca Waterloo Road', 'Karen David', 'Josh Stevenson bbcone', 'Josh Stevenson Waterloo Road', 'Josh bbcone', 'Josh Waterloo Road', 'William Rush', 'Nurse bbcone', 'Nurse Waterloo Road', 'Laura Crossley', 'Connor Lewis bbcone', 'Connor Lewis Waterloo Road', 'Connor bbcone', 'Connor Waterloo Road', 'Luke Tittensor', 'Janeece Bryant bbcone', 'Janeece Bryant Waterloo Road', 'Janeece bbcone', 'Janeece Waterloo Road', 'Chelsee Healey', 'Sarah Evans bbcone', 'Sarah Evans Waterloo Road', 'Sarah bbcone', 'Sarah Waterloo Road', 'Jodie Cromer', 'Claire Evans bbcone', 'Claire Evans Waterloo Road', 'Claire bbcone', 'Claire Waterloo Road', 'Jennifer Hennessy', 'Jess Fisher bbcone', 'Jess Fisher Waterloo Road', 'Jess bbcone', 'Jess Waterloo Road', 'Linzey Cocker', 'Tom Clarkson bbcone', 'Tom Clarkson Waterloo Road', 'Tom bbcone', 'Tom Waterloo Road', 'Jason Done', 'Ronan Burley bbcone', 'Ronan Burley Waterloo Road', 'Ronan bbcone', 'Ronan Waterloo Road', 'Ben-Ryan Davies', 'Vicki MacDonald bbcone', 'Vicki MacDonald Waterloo Road', 'Vicki bbcone', 'Vicki Waterloo Road', 'Rebecca Ryan', 'Karen Fisher bbcone', 'Karen Fisher Waterloo Road', 'Karen bbcone', 'Karen Waterloo Road', 'Amanda Burton', 'Grantly Budgen bbcone', 'Grantly Budgen Waterloo Road', 'Grantly bbcone', 'Grantly Waterloo Road', 'Philip Martin Brown', 'Amy Porter bbcone', 'Amy Porter Waterloo Road', 'Amy bbcone', 'Amy Waterloo Road', 'Ayesha Gwilt', 'Jonah Kirby bbcone', 'Jonah Kirby Waterloo Road', 'Jonah bbcone', 'Jonah Waterloo Road', 'Lucien Laviscount', 'Sambuca Kelly bbcone', 'Sambuca Kelly Waterloo Road', 'Sambuca bbcone', 'Sambuca Waterloo Road', 'Holly Kenny', 'Finn Sharkey bbcone', 'Finn Sharkey Waterloo Road', 'Finn bbcone', 'Finn Waterloo Road', 'Jack McMullen', 'Ruby Fry bbcone', 'Ruby Fry Waterloo Road', 'Ruby bbcone', 'Ruby Waterloo Road', 'Elizabeth Berrington', 'Maria Lucas bbcone', 'Maria Lucas Waterloo Road', 'Maria bbcone', 'Maria Waterloo Road', 'Susan Cookson', 'Christopher Mead bbcone', 'Christopher Mead Waterloo Road', 'Christopher bbcone', 'Christopher Waterloo Road', 'William Ash', 'Lauren Andrews bbcone', 'Lauren Andrews Waterloo Road', 'Lauren bbcone', 'Lauren Waterloo Road', 'Darcy Isa', 'Harry Fisher bbcone', 'Harry Fisher Waterloo Road', 'Harry bbcone', 'Harry Waterloo Road', 'Ceallach Spellman', 'Charlie Fisher bbcone', 'Charlie Fisher Waterloo Road', 'Charlie bbcone', 'Charlie Waterloo Road', 'Ian Puleston-Davies']
    #keywords = ['bbcone', '#crimewatch', 'Tracy Manners', 'Matthew Amroliwala', 'Lorraine Evans', 'Rav Wilding', 'Richard Turley', 'Gavin Ahern', 'Kirsty Young', 'Deborah McCarthy', 'Joe Mather']
    #keywords = ['bbcone', '#thenationallotterymidweekdraws', '#thenationallotterymidweekdraws', 'scott_mills', 'Scott Mills', 'Nick Harris', 'Andy Atkinson']
    #keywords = ['bbcone', '#theoneshow', '#oneshow', 'Bradley James', 'Jason_Manford', 'Jason Manford', 'Colin Morgan', 'RealAlexJones', 'Alex Jones', 'Jilly Cooper']
    keywords = ['bbcone', '#eastenders', 'Bryan Kirkwood', 'Lee Salisbury', 'Simon Ashdown', 'Ian Beale bbcone', 'Ian Beale EastEnders', 'Ian bbcone', 'Ian EastEnders', 'AdamWoodyatt', 'Adam Woodyatt', 'Ronnie Mitchell bbcone', 'Ronnie Mitchell EastEnders', 'Ronnie bbcone', 'Ronnie EastEnders', 'Samantha Womack', 'Dot Branning bbcone', 'Dot Branning EastEnders', 'Dot bbcone', 'Dot EastEnders', 'June Brown', 'Nurse Denton bbcone', 'Nurse Denton EastEnders', 'Nurse bbcone', 'Nurse EastEnders', 'Elicia Daly', 'Pat Evans bbcone', 'Pat Evans EastEnders', 'Pat bbcone', 'Pat EastEnders', 'Pam St Clement', 'Jay Brown bbcone', 'Jay Brown EastEnders', 'Jay bbcone', 'Jay EastEnders', 'Jamie Borthwick', 'Billy Mitchell bbcone', 'Billy Mitchell EastEnders', 'Billy bbcone', 'Billy EastEnders', 'Perry Fenwick', 'Whitney Dean bbcone', 'Whitney Dean EastEnders', 'Whitney bbcone', 'Whitney EastEnders', 'Shona McGarty', 'Roxy Mitchell bbcone', 'Roxy Mitchell EastEnders', 'Roxy bbcone', 'Roxy EastEnders', 'Rita Simons', 'Stacey Branning bbcone', 'Stacey Branning EastEnders', 'Stacey bbcone', 'Stacey EastEnders', 'LaceyATurner', 'Lacey Turner', 'Darren Miller bbcone', 'Darren Miller EastEnders', 'Darren bbcone', 'Darren EastEnders', 'Charlie G Hawkins', 'Janine Malloy bbcone', 'Janine Malloy EastEnders', 'Janine bbcone', 'Janine EastEnders', 'Charlie Brooks', 'Sam Mitchell bbcone', 'Sam Mitchell EastEnders', 'Sam bbcone', 'Sam EastEnders', 'Danniella Westbrook', 'Phil Mitchell bbcone', 'Phil Mitchell EastEnders', 'Phil bbcone', 'Phil EastEnders', 'Steve McFadden', 'DC Andrew Newton bbcone', 'DC Andrew Newton EastEnders', 'DC bbcone', 'DC EastEnders', 'Luke Harris', 'Zainab Masood bbcone', 'Zainab Masood EastEnders', 'Zainab bbcone', 'Zainab EastEnders', 'Nina Wadia', 'Ryan Malloy bbcone', 'Ryan Malloy EastEnders', 'Ryan bbcone', 'Ryan EastEnders', 'Neil McDermott', 'Peggy Mitchell bbcone', 'Peggy Mitchell EastEnders', 'Peggy bbcone', 'Peggy EastEnders', 'Barbara Windsor', 'Patrick Trueman bbcone', 'Patrick Trueman EastEnders', 'Patrick bbcone', 'Patrick EastEnders', 'Rudolph Walker']
    link = "http://bbc.co.uk/i/" + pid + "/?t="#  + "16m51s" # Replace XXmXXs with mins and secs through the prog

    try:
        homedir = os.path.expanduser("~")
        file = open(homedir + "/twitstream-eastenders-2.txt",'r')
        open = True
    except IOError, e:
        print ("Opening of file failed")
        open = False

    if open:
        # Word freq analysis in 1 min chunks?
        textarray = list()
        for line in file.readlines():
            if line != "\n":
                try:
                    line = cjson.decode(line)
                    textarray.append(line)
                except cjson.DecodeError, e:
                    pass


        # Tweets per minute:
        offset = 0
        counts = dict()
        for tweet in textarray:
            #print tweet
            firsttweettime = datetime(2010,9,10,19,0,0)
            nexttweettime = firsttweettime + timedelta(seconds=(offset*60)+60)
            tweettime = parse(tweet['created_at'])
            tweettime = tweettime.replace(tzinfo=None)
            #print str(firsttweettime) + " " + str(tweettime) + " " + str(nexttweettime)
            if not (tweettime < nexttweettime):
                offset += 1

            if counts.has_key(str(nexttweettime - timedelta(seconds=60))):
                counts[str(nexttweettime - timedelta(seconds=60))] += 1
            else:
                counts[str(nexttweettime - timedelta(seconds=60))] = 1

        counts = counts.items()
        counts.sort()
        print counts

        items = [(v,k) for k, v in counts]
        items.sort()
        maxval = float(items[len(items)-1][0])
        normaliser = float(100.0/maxval)

        # Produce graph
        xcoords = list()
        ycoords = list()
        minutes = 0
        for tweettime,count in counts:
            tweettime = datetime.strptime(tweettime,"%Y-%m-%d %H:%M:%S")
            # This will fail at some point
            if minutes > int(tweettime.strftime("%M")):
                minutes = 60 + int(tweettime.strftime("%M"))
            else:
                minutes = int(tweettime.strftime("%M"))
            #tweettime = tweettime.strftime("%H:%M")
            xcoords.append(minutes)
            if float(normaliser*count) > 80:
                print "BOOKMARK!: " + link + str(minutes-1-timediffmins) + "m0s"
            ycoords.append(float(normaliser*count))
            #minutes += 1
        plt.figure(1)
        plt.subplot(311)
        plt.plot(xcoords,ycoords)
        plt.ylabel('Tweet Count (Overall)')
        plt.title('Normalised ' + string.capwords(string.replace(keywords[1],"#","")) + ' Twitter Activity ' + tweettime.strftime("%d/%m/%Y"))

        # Other analysis
        tweets = list()
        words = list()
        for tweet in textarray:
            tweettime = parse(tweet['created_at'])
            #print str(tweettime) + ": " + tweet['text']
            #if tweet['id'] < 23176966250:
            tweets.append([tweet['id'], tweet['text']])
            #print [tweet['id'], tweet['text']]
            for word in tweet['text'].split():
                for items in """!"#$%&()*+,-./:;<=>?@~[\\]?_'`{|}?""":
                    word = string.replace(word,items,"")
                if word != "":
                    words.append(string.lower(word))
                #if string.lower(word) == "classic":
                #    print "CLASSIC: " + str([tweet['created_at'], tweet['id'], tweet['text']])
                #if string.lower(word) == "duncanbannatyne":
                #    print "DUNCANBANNATYNE: " + str([tweet['created_at'], tweet['id'], tweet['text']])
                #if string.lower(word) == "dragonjones":
                #    print "DRAGONJONES: " + str([tweet['created_at'], tweet['id'], tweet['text']])
                #if string.lower(word) == "phil":
                #    print "PHIL: " + str([tweet['created_at'], tweet['id'], tweet['text']])
                #if string.lower(word) == "rt":
                #    print "RT: " + str([tweet['created_at'], tweet['id'], tweet['text']])

        filteredwords = list()
        for word in words:
            if word not in exclusions:
                filteredwords.append(word)
            # Use 'filteredwords' from here
        counts = {}
        for word in filteredwords:
            try:
                counts[word] = counts[word] + 1
            except KeyError:
                counts[word] = 1
        items = [(v,k) for k, v in counts.items()]
        items.sort(reverse=True)
        

        #print items
        itemcount = 0
        index = 0
        unusualwords = list()
        while itemcount < 7:
            keyword = items[index][1]
            nouse = False
            for word in keywords:
                if (string.find(string.lower(word),string.lower(keyword)) != -1) or (string.lower(keyword) == "rt"):
                    nouse = True
                    break
            if nouse == False:
                unusualwords.append(keyword)
                itemcount += 1
            index += 1
            if index == len(items):
                break

        print unusualwords
        ax1 = plt.subplot(312)
        for word in unusualwords:
            unusualprocessed = dict()
            for tweet in textarray:
                for tweetword in tweet['text'].split():
                    for items in """!"#$%&()*+,-./:;<=>?@~[\\]?_'`{|}?""":
                        tweetword = string.replace(tweetword,items,"")
                    if string.lower(tweetword) == string.lower(word):
                        # Found an occurrence of an unusual word in a tweet
                        # Mark the time!
                        tweettime = parse(tweet['created_at'])
                        tweettime = tweettime.replace(tzinfo=None)
                        tweettime = tweettime.replace(second=0)
                        if unusualprocessed.has_key(str(tweettime)):
                            unusualprocessed[str(tweettime)] += 1
                        else:
                            unusualprocessed[str(tweettime)] = 1
                        break
            unusualprocessed = unusualprocessed.items()
            unusualprocessed.sort()
            print unusualprocessed

            newitems = [(v,k) for k, v in unusualprocessed]
            newitems.sort()
            maxval = float(newitems[len(newitems)-1][0])
            normaliser = float(100.0/maxval)

            # Produce graph
            xcoords = list()
            ycoords = list()
            minutes = 0
            for tweettime,count in unusualprocessed:
                tweettime = datetime.strptime(tweettime,"%Y-%m-%d %H:%M:%S")
                #tweettime = tweettime.strftime("%H:%M")
                # This will fail at some point
                if minutes > int(tweettime.strftime("%M")):
                    minutes = 60 + int(tweettime.strftime("%M"))
                else:
                    minutes = int(tweettime.strftime("%M"))
                xcoords.append(minutes)
                ycoords.append(float(normaliser*count))
            
            ax1.plot(xcoords,ycoords, label=word)
        handles, labels = ax1.get_legend_handles_labels()
        ax1.legend(handles,labels,loc=2,bbox_to_anchor=(1,1))
        plt.ylabel('Tweet Count (Unknown Keywords)')


        items = [(v,k) for k, v in counts.items()]
        items.sort(reverse=True)

        itemcount = 0
        index = 0
        usualwords = list()
        while itemcount < 7:
            keyword = items[index][1]
            nouse = True
            for word in keywords:
                if (string.lower(keyword) in string.lower(word)) and (string.lower(keyword) != "rt"):
                #if string.find(string.lower(word),string.lower(keyword)) >= 1:
                    nouse = False
                    break
            if nouse == False:
                usualwords.append(keyword)
                itemcount += 1
            index += 1
            if index == len(items):
                break

        print usualwords
        ax2 = plt.subplot(313)
        for word in usualwords:
            usualprocessed = dict()
            for tweet in textarray:
                for tweetword in tweet['text'].split():
                    for items in """!"#$%&()*+,-./:;<=>?@~[\\]?_'`{|}?""":
                        tweetword = string.replace(tweetword,items,"")
                    if string.lower(tweetword) == string.lower(word):
                        # Found an occurrence of an unusual word in a tweet
                        # Mark the time!
                        tweettime = parse(tweet['created_at'])
                        tweettime = tweettime.replace(tzinfo=None)
                        tweettime = tweettime.replace(second=0)
                        if usualprocessed.has_key(str(tweettime)):
                            usualprocessed[str(tweettime)] += 1
                        else:
                            usualprocessed[str(tweettime)] = 1
                        break
            usualprocessed = usualprocessed.items()
            usualprocessed.sort()
            print usualprocessed

            newitems = [(v,k) for k, v in usualprocessed]
            newitems.sort()
            maxval = float(newitems[len(newitems)-1][0])
            normaliser = float(100.0/maxval)

            # Produce graph
            xcoords = list()
            ycoords = list()
            minutes = 0
            for tweettime,count in usualprocessed:
                tweettime = datetime.strptime(tweettime,"%Y-%m-%d %H:%M:%S")
                #tweettime = tweettime.strftime("%H:%M")
                # This will fail at some point
                if minutes > int(tweettime.strftime("%M")):
                    minutes = 60 + int(tweettime.strftime("%M"))
                else:
                    minutes = int(tweettime.strftime("%M"))
                xcoords.append(minutes)
                ycoords.append(float(normaliser*count))

            ax2.plot(xcoords,ycoords,label=word)
        handles, labels = ax2.get_legend_handles_labels()
        ax2.legend(handles,labels,loc=2,bbox_to_anchor=(1,1))
        plt.ylabel('Tweet Count (Known Keywords)')


        plt.show()


        #for tweet in textarray:
        #    tweettime = parse(tweet['created_at'])


